# Mapa de OpenSpecs — ARASAAC Social MCP Platform

## Convención

Cada OpenSpec se ubica en:

```text
openspec/changes/<id>/
  proposal.md
  design.md
  tasks.md
  spec.md
```

## Releases

### Release 0 — Foundation

| ID | Nombre | Objetivo | Bloquea |
|---|---|---|---|
| 0001 | project-foundation | Repo, convenciones, tooling, Docker base | Todo |
| 0002 | arasaac-license-governance | Licencia, atribución, políticas | Generación/export |
| 0006 | material-domain-model | Modelo de materiales y trazabilidad | Generadores |
| 0019 | testing-quality-gates | CI, tests, DoD | Todo |
| 0020 | docker-compose-deployment | Despliegue local | MVP |

### Release 1 — MVP Validable

| ID | Nombre | Objetivo | Depende de |
|---|---|---|---|
| 0003 | arasaac-connector | Conectar API ARASAAC y normalizar | 0001, 0002 |
| 0004 | mcp-server-core | Servidor MCP local | 0001 |
| 0005 | pictogram-search-tools | search/get/suggest | 0003, 0004 |
| 0007 | visual-agenda-generator | Agenda visual | 0005, 0006 |
| 0008 | communication-board-generator | Tablero comunicación | 0005, 0006 |
| 0012 | export-engine | HTML/PDF + créditos | 0002, 0006 |
| 0013 | web-app-shell-aa | Web AA base | 0001 |
| 0014 | guided-creation-flow | flujo guiado | 0013, 0007, 0008 |
| 0015 | preview-editor | vista previa editable | 0014 |
| 0016 | review-workflow | revisión humana | 0006, 0015 |
| 0017 | audit-observability | auditoría mínima | 0006 |

### Release 2 — Producto piloto

| ID | Nombre | Objetivo |
|---|---|---|
| 0009 | accessible-document-generator | lectura fácil + pictos |
| 0010 | social-story-generator | historias sociales |
| 0011 | signage-generator | señalética |
| 0018 | preferences-without-pii | preferencias entidad/plantilla/perfil no personal |
| 0022 | semantic-search-future | ranking semántico con pgvector |
| 0024 | arasaac-validation-dossier | dossier de bendición ARASAAC |

### Release 3 — Escalado

| ID | Nombre | Objetivo |
|---|---|---|
| 0021 | keycloak-future-auth | autenticación/roles |
| 0023 | multientity-future | multi-entidad simple y camino multi-tenant |

---

## Precedencias críticas

```text
0001 -> 0002 -> 0003 -> 0005 -> 0007/0008 -> 0012 -> 0016
0001 -> 0013 -> 0014 -> 0015 -> 0016
0006 -> 0007/0008/0009/0010/0011 -> 0017
0019 atraviesa todas las specs
```
