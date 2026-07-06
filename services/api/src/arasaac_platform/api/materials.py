import os
from functools import lru_cache
from typing import Annotated, Literal
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException

from arasaac_platform.domain.materials import AuditAction, AuditEvent
from arasaac_platform.domain.workflow import InvalidMaterialTransition
from arasaac_platform.observability.metrics import export_counter, review_counter
from arasaac_platform.repositories import Repository, create_repository
from arasaac_platform.repositories.memory import MaterialNotFound
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
)
from arasaac_platform.services.export import (
    ExportBlockedError,
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

router = APIRouter(prefix="/api/materials", tags=["materials"])


@lru_cache(maxsize=1)
def get_repository() -> Repository:
    return create_repository(os.getenv("DATABASE_URL"))


RepositoryDependency = Annotated[Repository, Depends(get_repository)]


@router.post("/agendas", response_model=MaterialResult, status_code=201)
def agendas(request: CreateAgendaInput, store: RepositoryDependency) -> MaterialResult:
    return MaterialResult(material=create_agenda(request, store))


@router.post("/boards", response_model=MaterialResult, status_code=201)
def boards(request: CreateBoardInput, store: RepositoryDependency) -> MaterialResult:
    return MaterialResult(material=create_board(request, store))


@router.post("/documents", response_model=MaterialResult, status_code=201)
def documents(
    request: CreateDocumentInput,
    store: RepositoryDependency,
) -> MaterialResult:
    return MaterialResult(material=create_document(request, store))


@router.post("/stories", response_model=MaterialResult, status_code=201)
def stories(request: CreateStoryInput, store: RepositoryDependency) -> MaterialResult:
    return MaterialResult(material=create_story(request, store))


@router.post("/signage", response_model=MaterialResult, status_code=201)
def signage(request: CreateSignageInput, store: RepositoryDependency) -> MaterialResult:
    return MaterialResult(material=create_signage(request, store))


@router.get("", response_model=MaterialListResult)
def list_materials(store: RepositoryDependency) -> MaterialListResult:
    return MaterialListResult(materials=store.list_materials())


@router.get("/{material_id}", response_model=MaterialResult)
def get_material(material_id: UUID, store: RepositoryDependency) -> MaterialResult:
    try:
        return MaterialResult(material=store.get(material_id))
    except MaterialNotFound as exc:
        raise HTTPException(status_code=404, detail="Material no encontrado.") from exc


@router.post("/{material_id}/submit", response_model=MaterialResult)
def submit_material(material_id: UUID, store: RepositoryDependency) -> MaterialResult:
    try:
        return MaterialResult(material=submit(material_id, store))
    except MaterialNotFound as exc:
        raise HTTPException(status_code=404, detail="Material no encontrado.") from exc
    except InvalidMaterialTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/{material_id}/review", response_model=MaterialResult)
def review_material(
    material_id: UUID,
    request: ReviewMaterialInput,
    store: RepositoryDependency,
) -> MaterialResult:
    try:
        material = review(material_id, request, store)
        review_counter[str(request.outcome)] += 1
        return MaterialResult(material=material)
    except MaterialNotFound as exc:
        raise HTTPException(status_code=404, detail="Material no encontrado.") from exc
    except InvalidMaterialTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/{material_id}/audit", response_model=AuditEventsResult)
def audit(material_id: UUID, store: RepositoryDependency) -> AuditEventsResult:
    try:
        store.get(material_id)
    except MaterialNotFound as exc:
        raise HTTPException(status_code=404, detail="Material no encontrado.") from exc
    return AuditEventsResult(events=store.events_for(material_id))


@router.get("/{material_id}/export", response_model=ExportResult)
async def export_material(
    material_id: UUID,
    store: RepositoryDependency,
    format: Literal["html", "pdf", "docx", "pptx", "zip"] = "html",
) -> ExportResult:
    try:
        material = store.get(material_id)
        if format == "html":
            content = export_html(material)
            media_type = "text/html"
        elif format == "pdf":
            content = await export_pdf(material)
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
