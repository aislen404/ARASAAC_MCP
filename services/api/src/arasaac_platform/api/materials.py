import os
import re
from functools import lru_cache
from typing import Annotated, Literal
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException

from arasaac_platform.arasaac.client import ArasaacClient
from arasaac_platform.domain.materials import AuditAction, AuditEvent
from arasaac_platform.domain.slug_generator import generate_workspace_slug
from arasaac_platform.domain.workspaces import Workspace, WorkspaceSummary
from arasaac_platform.domain.workflow import InvalidMaterialTransition
from arasaac_platform.observability.metrics import export_counter, review_counter
from arasaac_platform.repositories import Repository, create_repository
from arasaac_platform.repositories.memory import MaterialNotFound, WorkspaceNotFound
from arasaac_platform.schemas.materials import (
    AuditEventsResult,
    CreateAgendaInput,
    CreateBoardInput,
    CreateDocumentInput,
    CreateSignageInput,
    CreateStoryInput,
    ExportManifest,
    ExportResult,
    MaterialListResult,
    MaterialResult,
    ReviewMaterialInput,
    WorkspaceCreateInput,
    WorkspaceResult,
    WorkspaceUpdateInput,
)
from arasaac_platform.schemas.validation import ValidationReport
from arasaac_platform.services.export import (
    ExportBlockedError,
    ImageFetcher,
    encode_export,
    export_docx,
    export_html,
    export_pdf,
    export_pptx,
    export_zip_package,
)
from arasaac_platform.services.materials import (
    create_agenda,
    create_board,
    create_document,
    create_signage,
    create_story,
    review,
    submit,
)
from arasaac_platform.services.validation import (
    ValidationContext,
    run_validators,
    validation_summary_counts,
)

router = APIRouter(tags=["materials", "workspaces"])

PROPER_NAME_RE = re.compile(r"\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b")


@lru_cache(maxsize=1)
def get_repository() -> Repository:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL es obligatoria en runtime.")
    return create_repository(database_url)


RepositoryDependency = Annotated[Repository, Depends(get_repository)]


def get_image_fetcher() -> ImageFetcher | None:
    """Default ARASAAC image fetcher (None keeps export_pdf's official fetcher).

    Overridable in tests via ``app.dependency_overrides`` to avoid live network calls
    to ARASAAC when exercising the export flow end-to-end.
    """
    return None


ImageFetcherDependency = Annotated[ImageFetcher | None, Depends(get_image_fetcher)]


def _workspace_summary(workspace: Workspace) -> WorkspaceSummary:
    return WorkspaceSummary(
        workspace_id=workspace.workspace_id,
        slug=workspace.slug,
        display_name=workspace.display_name,
    )


def _get_workspace_or_404(slug: str, store: Repository) -> Workspace:
    try:
        return store.get_workspace_by_slug(slug)
    except WorkspaceNotFound as exc:
        raise HTTPException(status_code=404, detail="Workspace no encontrado.") from exc


def _get_material_in_workspace_or_404(material_id: UUID, workspace: Workspace, store: Repository):
    try:
        material = store.get(material_id)
    except MaterialNotFound as exc:
        raise HTTPException(status_code=404, detail="Material no encontrado.") from exc
    if material.workspace_id != workspace.workspace_id:
        raise HTTPException(status_code=404, detail="Material no encontrado.")
    return material


def _record_material_access(workspace: Workspace, material_id: UUID, store: Repository) -> None:
    store.append_event(
        AuditEvent(
            workspace_id=workspace.workspace_id,
            material_id=material_id,
            action=AuditAction.MATERIAL_ACCESSED,
            detail="Acceso a material por workspace.",
        )
    )


def _validate_display_name(display_name: str | None) -> None:
    if display_name is None:
        return
    if PROPER_NAME_RE.search(display_name):
        raise HTTPException(status_code=422, detail="display_name contiene posibles datos personales.")


@router.post("/api/workspaces", response_model=WorkspaceResult, status_code=201)
def create_workspace(request: WorkspaceCreateInput, store: RepositoryDependency) -> WorkspaceResult:
    _validate_display_name(request.display_name)
    workspace = Workspace(
        slug=generate_workspace_slug(store.workspace_slug_exists),
        display_name=request.display_name,
    )
    store.save_workspace(workspace)
    store.append_event(
        AuditEvent(
            workspace_id=workspace.workspace_id,
            material_id=None,
            action=AuditAction.WORKSPACE_CREATED,
            detail="Workspace creado.",
        )
    )
    return WorkspaceResult(workspace=workspace)


@router.get("/api/workspaces/{slug}", response_model=WorkspaceResult)
def get_workspace(slug: str, store: RepositoryDependency) -> WorkspaceResult:
    return WorkspaceResult(workspace=_get_workspace_or_404(slug, store))


@router.patch("/api/workspaces/{slug}", response_model=WorkspaceResult)
def update_workspace(
    slug: str,
    request: WorkspaceUpdateInput,
    store: RepositoryDependency,
) -> WorkspaceResult:
    workspace = _get_workspace_or_404(slug, store)
    _validate_display_name(request.display_name)
    updated = workspace.model_copy(update={"display_name": request.display_name})
    store.save_workspace(updated)
    return WorkspaceResult(workspace=updated)


@router.post("/api/workspaces/{slug}/materials/agendas", response_model=MaterialResult, status_code=201)
def agendas(slug: str, request: CreateAgendaInput, store: RepositoryDependency) -> MaterialResult:
    workspace = _get_workspace_or_404(slug, store)
    material = create_agenda(request, workspace, store)
    return MaterialResult(material=material, workspace=_workspace_summary(workspace))


@router.post("/api/workspaces/{slug}/materials/boards", response_model=MaterialResult, status_code=201)
def boards(slug: str, request: CreateBoardInput, store: RepositoryDependency) -> MaterialResult:
    workspace = _get_workspace_or_404(slug, store)
    material = create_board(request, workspace, store)
    return MaterialResult(material=material, workspace=_workspace_summary(workspace))


@router.post("/api/workspaces/{slug}/materials/documents", response_model=MaterialResult, status_code=201)
def documents(
    slug: str,
    request: CreateDocumentInput,
    store: RepositoryDependency,
) -> MaterialResult:
    workspace = _get_workspace_or_404(slug, store)
    material = create_document(request, workspace, store)
    return MaterialResult(material=material, workspace=_workspace_summary(workspace))


@router.post("/api/workspaces/{slug}/materials/stories", response_model=MaterialResult, status_code=201)
def stories(slug: str, request: CreateStoryInput, store: RepositoryDependency) -> MaterialResult:
    workspace = _get_workspace_or_404(slug, store)
    material = create_story(request, workspace, store)
    return MaterialResult(material=material, workspace=_workspace_summary(workspace))


@router.post("/api/workspaces/{slug}/materials/signage", response_model=MaterialResult, status_code=201)
def signage(slug: str, request: CreateSignageInput, store: RepositoryDependency) -> MaterialResult:
    workspace = _get_workspace_or_404(slug, store)
    material = create_signage(request, workspace, store)
    return MaterialResult(material=material, workspace=_workspace_summary(workspace))


@router.get("/api/workspaces/{slug}/materials", response_model=MaterialListResult)
def list_materials(
    slug: str,
    store: RepositoryDependency,
    status: str | None = None,
    q: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> MaterialListResult:
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=422, detail="limit debe estar entre 1 y 100.")
    if offset < 0:
        raise HTTPException(status_code=422, detail="offset debe ser mayor o igual que 0.")
    workspace = _get_workspace_or_404(slug, store)
    statuses = tuple(part.strip() for part in status.split(",") if part.strip()) if status else None
    materials, total = store.list_materials(
        workspace_id=workspace.workspace_id,
        statuses=statuses,
        query=q,
        limit=limit,
        offset=offset,
    )
    return MaterialListResult(
        materials=materials,
        total=total,
        limit=limit,
        offset=offset,
        workspace=_workspace_summary(workspace),
    )


@router.get("/api/workspaces/{slug}/materials/{material_id}", response_model=MaterialResult)
def get_material(slug: str, material_id: UUID, store: RepositoryDependency) -> MaterialResult:
    workspace = _get_workspace_or_404(slug, store)
    material = _get_material_in_workspace_or_404(material_id, workspace, store)
    _record_material_access(workspace, material_id, store)
    return MaterialResult(material=material, workspace=_workspace_summary(workspace))


@router.post("/api/workspaces/{slug}/materials/{material_id}/submit", response_model=MaterialResult)
def submit_material(slug: str, material_id: UUID, store: RepositoryDependency) -> MaterialResult:
    workspace = _get_workspace_or_404(slug, store)
    try:
        _get_material_in_workspace_or_404(material_id, workspace, store)
        return MaterialResult(material=submit(material_id, store))
    except MaterialNotFound as exc:
        raise HTTPException(status_code=404, detail="Material no encontrado.") from exc
    except InvalidMaterialTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/api/workspaces/{slug}/materials/{material_id}/review", response_model=MaterialResult)
def review_material(
    slug: str,
    material_id: UUID,
    request: ReviewMaterialInput,
    store: RepositoryDependency,
) -> MaterialResult:
    workspace = _get_workspace_or_404(slug, store)
    try:
        _get_material_in_workspace_or_404(material_id, workspace, store)
        material = review(material_id, request, store)
        review_counter[str(request.outcome)] += 1
        return MaterialResult(material=material, workspace=_workspace_summary(workspace))
    except MaterialNotFound as exc:
        raise HTTPException(status_code=404, detail="Material no encontrado.") from exc
    except InvalidMaterialTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/api/workspaces/{slug}/materials/{material_id}/audit", response_model=AuditEventsResult)
def audit(slug: str, material_id: UUID, store: RepositoryDependency) -> AuditEventsResult:
    workspace = _get_workspace_or_404(slug, store)
    _get_material_in_workspace_or_404(material_id, workspace, store)
    return AuditEventsResult(events=store.events_for(material_id, workspace_id=workspace.workspace_id))


@router.post("/api/workspaces/{slug}/materials/{material_id}/validate", response_model=ValidationReport)
async def validate_material(
    slug: str,
    material_id: UUID,
    store: RepositoryDependency,
) -> ValidationReport:
    workspace = _get_workspace_or_404(slug, store)
    material = _get_material_in_workspace_or_404(material_id, workspace, store)
    _record_material_access(workspace, material_id, store)

    report = await run_validators(
        material,
        ValidationContext(
            arasaac_client=ArasaacClient(timeout_seconds=3.0),
            allow_online_lookup=bool(os.getenv("ARASAAC_ONLINE_LOOKUP")),
            online_lookup_timeout_seconds=3.0,
        ),
    )
    counts = validation_summary_counts(report)
    store.append_event(
        AuditEvent(
            workspace_id=workspace.workspace_id,
            material_id=material_id,
            action=AuditAction.VALIDATED,
            detail=(
                "Validación ejecutada. "
                f"blocker={counts['blocker']} warning={counts['warning']} ok={counts['ok']}."
            ),
        )
    )
    return report


@router.get("/api/workspaces/{slug}/materials/{material_id}/export", response_model=ExportResult)
async def export_material(
    slug: str,
    material_id: UUID,
    store: RepositoryDependency,
    fetch_image: ImageFetcherDependency,
    format: Literal["html", "pdf", "docx", "pptx", "zip"] = "html",
) -> ExportResult:
    workspace = _get_workspace_or_404(slug, store)
    try:
        material = _get_material_in_workspace_or_404(material_id, workspace, store)
        if format == "html":
            content = export_html(material)
            media_type = "text/html"
        elif format == "pdf":
            content = await export_pdf(material, fetch_image=fetch_image)
            media_type = "application/pdf"
        elif format == "docx":
            content = export_docx(material)
            media_type = (
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        elif format == "pptx":
            content = export_pptx(material)
            media_type = (
                "application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        else:
            content = export_zip_package(material)
            media_type = "application/zip"
        export_counter[format] += 1
        store.append_event(
            AuditEvent(
                workspace_id=workspace.workspace_id,
                material_id=material_id,
                action=AuditAction.EXPORTED,
                detail=f"Exportación {format}.",
            )
        )
        return ExportResult(
            filename=f"{material_id}.{format}",
            media_type=media_type,
            content_base64=encode_export(content),
            manifest=ExportManifest(
                material_id=str(material.material_id),
                version=material.version,
                attribution=material.attribution_text,
                pictograms=material.pictograms,
                human_review_approved=True,
            ),
        )
    except MaterialNotFound as exc:
        raise HTTPException(status_code=404, detail="Material no encontrado.") from exc
    except (ExportBlockedError, httpx.HTTPError) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/api/workspaces/{slug}/materials/{material_id}/export/manifest", response_model=ExportManifest)
def export_material_manifest(
    slug: str,
    material_id: UUID,
    store: RepositoryDependency,
) -> ExportManifest:
    workspace = _get_workspace_or_404(slug, store)
    material = _get_material_in_workspace_or_404(material_id, workspace, store)
    _record_material_access(workspace, material_id, store)
    if material.status != "approved":
        raise HTTPException(status_code=409, detail="El manifiesto solo está disponible para materiales aprobados.")
    return ExportManifest(
        material_id=str(material.material_id),
        version=material.version,
        attribution=material.attribution_text,
        pictograms=material.pictograms,
        human_review_approved=True,
    )
