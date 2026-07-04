import os
from typing import Annotated, Literal
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException

from arasaac_platform.domain.materials import AuditAction, AuditEvent
from arasaac_platform.domain.workflow import InvalidMaterialTransition
from arasaac_platform.repositories import Repository, create_repository
from arasaac_platform.repositories.memory import MaterialNotFound
from arasaac_platform.schemas.materials import (
    AuditEventsResult,
    CreateAgendaInput,
    CreateBoardInput,
    ExportResult,
    ExportManifest,
    MaterialListResult,
    MaterialResult,
    ReviewMaterialInput,
)
from arasaac_platform.services.export import (
    ExportBlockedError,
    encode_export,
    export_html,
    export_pdf,
)
from arasaac_platform.services.materials import (
    create_agenda,
    create_board,
    review,
    submit,
)


router = APIRouter(prefix="/api/materials", tags=["materials"])
repository = create_repository(os.getenv("DATABASE_URL"))


def get_repository() -> Repository:
    return repository


RepositoryDependency = Annotated[Repository, Depends(get_repository)]


@router.post("/agendas", response_model=MaterialResult, status_code=201)
def agendas(request: CreateAgendaInput, store: RepositoryDependency) -> MaterialResult:
    return MaterialResult(material=create_agenda(request, store))


@router.post("/boards", response_model=MaterialResult, status_code=201)
def boards(request: CreateBoardInput, store: RepositoryDependency) -> MaterialResult:
    return MaterialResult(material=create_board(request, store))


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
        return MaterialResult(material=review(material_id, request, store))
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
    format: Literal["html", "pdf"] = "html",
) -> ExportResult:
    try:
        material = store.get(material_id)
        if format == "html":
            content = export_html(material)
            media_type = "text/html"
        else:
            content = await export_pdf(material)
            media_type = "application/pdf"
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
