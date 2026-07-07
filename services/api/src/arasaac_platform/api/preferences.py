from uuid import uuid4

from fastapi import APIRouter

from arasaac_platform.schemas.preferences import (
    EntityTemplate,
    EntityTemplateInput,
    EntityTemplateList,
)

router = APIRouter(prefix="/api/preferences", tags=["preferences"])

_templates: list[EntityTemplate] = []


@router.get("/templates", response_model=EntityTemplateList)
def list_templates() -> EntityTemplateList:
    return EntityTemplateList(templates=list(_templates))


@router.post("/templates", response_model=EntityTemplate, status_code=201)
def create_template(request: EntityTemplateInput) -> EntityTemplate:
    template = EntityTemplate(template_id=str(uuid4()), **request.model_dump())
    _templates.append(template)
    return template
