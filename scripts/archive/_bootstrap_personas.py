#!/usr/bin/env python3
"""Bootstrap único de .agents/personas/*.persona.md desde catalog/personas.yaml.

Se ejecuta UNA vez para materializar las 25 personas. Tras esto los archivos son
canónicos y este script queda como referencia histórica. NO se re-ejecuta
automáticamente (usa sync_agent_packs.py para regenerar packs IDE).
"""
from __future__ import annotations

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / ".agents/catalog/personas.yaml"
OUT = ROOT / ".agents/personas"

# Definición de checklist por persona: preguntas + bloqueos + criterios.
PERSONA_CONTENT: dict[str, dict[str, list[str]]] = {
    "product-owner-social": {
        "questions": [
            "¿La necesidad viene de una entidad social real (CEE, fundación, familia, CERMI)?",
            "¿Está priorizada en el backlog o es petición ad-hoc?",
            "¿Qué usuario específico se beneficia y cómo?",
            "¿Encaja con la misión no comercial del proyecto?",
        ],
        "blockers": [
            "La feature responde a interés comercial y no social.",
            "No hay entidad ni persona-usuaria identificada.",
            "Duplica una change en curso.",
        ],
        "checklist": [
            "El valor social está redactado en 1-2 líneas comprensibles.",
            "Hay al menos 1 caso de uso concreto.",
            "Se ha priorizado frente a alternativas.",
        ],
    },
    "ngo-cee-domain": {
        "questions": [
            "¿La solución encaja en la operativa real de una CEE / fundación / CERMI?",
            "¿Qué rol la usará (coordinador/a, profesional, familia, voluntariado)?",
            "¿Requiere formación previa que no vamos a dar?",
            "¿Se puede usar con recursos limitados (impresión BN, sin internet)?",
        ],
        "blockers": [
            "El workflow presupone recursos técnicos que la entidad no tiene.",
            "El material generado no es utilizable sin adaptación.",
        ],
        "checklist": [
            "El flujo se ha validado mentalmente con un caso concreto.",
            "Se contemplan formatos exportables imprimibles.",
            "Hay documentación pensada para el rol destinatario.",
        ],
    },
    "caasaac-methodology": {
        "questions": [
            "¿Respeta los principios básicos de CAA/SAAC (balance categorías gramaticales, coherencia visual)?",
            "¿La densidad de pictogramas es apropiada para el perfil?",
            "¿El sistema soporta ampliación léxica futura?",
            "¿El material es coherente con sistemas Fitzgerald u otros usados por profesionales?",
        ],
        "blockers": [
            "Tablero solo con sustantivos (sin verbos, sociales, preguntas).",
            "Uso decorativo de pictogramas que resta claridad comunicativa.",
        ],
        "checklist": [
            "Balance verbo/sustantivo/adjetivo/social/pregunta razonable.",
            "Pictogramas siempre acompañados de texto.",
            "Estructura predecible por categoría.",
        ],
    },
    "a11y-cognitive": {
        "questions": [
            "¿La carga cognitiva es proporcional al usuario (nº elementos, distractores)?",
            "¿El lenguaje es llano y directo?",
            "¿Los pasos siguen orden lógico y esperable?",
            "¿Hay refuerzos visuales redundantes (no solo texto)?",
        ],
        "blockers": [
            "Más de 12 elementos por página en materiales para dificultad cognitiva.",
            "Instrucciones con negaciones dobles o subordinadas anidadas.",
        ],
        "checklist": [
            "Frases < 20 palabras (mejor < 15 en lectura fácil).",
            "Una idea por bloque.",
            "Iconos + texto (no icono solo).",
        ],
    },
    "arasaac-liaison": {
        "questions": [
            "¿La feature preserva la relación institucional con ARASAAC?",
            "¿La atribución sigue visible en todos los exports?",
            "¿Se comunica el uso institucional (dossier) si aplica?",
            "¿Se respeta la marca ARASAAC (no usarla como propia)?",
        ],
        "blockers": [
            "Atribución oculta, en metadata invisible o borrable.",
            "Uso comercial encubierto.",
            "Modificación de pictogramas.",
        ],
        "checklist": [
            "Créditos en pie/última página/sección visible.",
            "Manifest JSON con URL de origen.",
            "Sin claim de autoría propia sobre los pictogramas.",
        ],
    },
    "license-legal": {
        "questions": [
            "¿Se respeta CC BY-NC-SA (atribución, no comercial, share-alike)?",
            "¿La atribución cumple los 4 elementos: autor, obra, licencia, cambios?",
            "¿No hay imágenes generadas por IA imitando el estilo ARASAAC?",
            "¿Los pictogramas se usan sin modificación?",
        ],
        "blockers": [
            "Uso comercial (venta, publicidad, upsell).",
            "Atribución ausente o incompleta.",
            "Pictogramas modificados (recolor, recorte, filtro).",
        ],
        "checklist": [
            "Manifest JSON completo por material exportado.",
            "Créditos visibles en el documento.",
            "Sin licencias contradictorias en el ZIP/paquete.",
        ],
    },
    "privacy-ethics": {
        "questions": [
            "¿El material está libre de PII (nombres, DNI, foto identificable, dirección)?",
            "¿Los logs, tests y fixtures están libres de datos personales?",
            "¿Hay vinculación material↔persona concreta (prohibido en MVP)?",
            "¿El sistema respeta el principio de minimización de datos?",
        ],
        "blockers": [
            "Cualquier PII en título/descripción/tags/contenido.",
            "Metadata EXIF con identificadores.",
            "Vinculación explícita 'agenda de Pedro' en MVP.",
        ],
        "checklist": [
            "Intake valida ausencia de PII antes de guardar.",
            "Logs sin PII (usar IDs, no nombres).",
            "Fixtures de test con datos sintéticos.",
        ],
    },
    "security": {
        "questions": [
            "¿Las tools MCP tienen schema estricto (extra=forbid)?",
            "¿Está en la allowlist?",
            "¿Sin ejecución arbitraria (subprocess, eval, os.system)?",
            "¿Los inputs se validan antes de tocar filesystem/red?",
            "¿Los secretos están fuera de logs y del repo?",
        ],
        "blockers": [
            "Tool MCP sin schema o con extra fields.",
            "Handler que ejecuta comandos derivados del input.",
            "Secreto commiteado o loggeado.",
        ],
        "checklist": [
            "Contract tests cubren happy path + inputs inválidos.",
            "Rate limiting o auth donde procede.",
            "Audit log de tool calls sensibles.",
        ],
    },
    "solution-architect": {
        "questions": [
            "¿La solución encaja en la arquitectura actual (FastAPI + Next.js + Postgres + MCP)?",
            "¿Requiere ADR (Architecture Decision Record)?",
            "¿Introduce acoplamiento cross-package no deseado?",
            "¿La deuda técnica se documenta?",
        ],
        "blockers": [
            "Nueva dependencia mayor sin ADR.",
            "Duplicación de responsabilidades entre packages.",
        ],
        "checklist": [
            "`design.md` muestra encaje.",
            "ADR en `docs/architecture/` si hay decisión relevante.",
            "Interfaces estables entre packages.",
        ],
    },
    "mcp-architect": {
        "questions": [
            "¿La tool/resource/prompt tiene propósito único y claro?",
            "¿Los schemas son estrictos y versionables?",
            "¿Los outputs son predecibles y contract-tested?",
            "¿Se documenta el uso en `docs/architecture/mcp-dual-surface.md`?",
        ],
        "blockers": [
            "Tool 'genérica' que hace demasiadas cosas.",
            "Sin contract test.",
            "Cambio breaking sin versionado.",
        ],
        "checklist": [
            "Nombre kebab-case descriptivo.",
            "Schema con `examples` para el descriptor MCP.",
            "Handler puro (side-effects declarados).",
        ],
    },
    "backend": {
        "questions": [
            "¿Los contratos están en Pydantic v2 y viven en `packages/contracts`?",
            "¿Los tests cubren happy path + edge cases + errores?",
            "¿La lógica de dominio está separada de la infraestructura (Postgres, Redis)?",
            "¿Sin SQL inline (usar SQLModel/query builder)?",
        ],
        "blockers": [
            "Endpoint sin schema Pydantic.",
            "Lógica de negocio dentro del router FastAPI.",
            "Migración Alembic sin revisar.",
        ],
        "checklist": [
            "Ruff + mypy verdes.",
            "Tests de integración con Postgres real (testcontainers o docker-compose).",
            "Documentación OpenAPI generada.",
        ],
    },
    "frontend": {
        "questions": [
            "¿Los componentes tienen contract test / visual regression?",
            "¿Se respeta el design system (Serena convergence)?",
            "¿La UI es honesta con el estado del backend (loading/error/empty)?",
            "¿Sin `localStorage`/`sessionStorage` como fuente única de verdad?",
        ],
        "blockers": [
            "Componente sin snapshot / visual test.",
            "Estado inconsistente entre cliente y servidor.",
            "Nueva dependencia UI sin ADR.",
        ],
        "checklist": [
            "ESLint + tsc verdes.",
            "Test unitario con Vitest/RTL.",
            "Playwright visual regression si es página completa.",
        ],
    },
    "data-connector": {
        "questions": [
            "¿La integración con ARASAAC API respeta rate limit y timeouts?",
            "¿Se cachea metadata + binario con TTL apropiado?",
            "¿Se guarda toda la metadata de licencia y atribución?",
            "¿Se maneja error (5xx, timeout, 404) con retry razonable?",
        ],
        "blockers": [
            "Cache sin metadata de licencia.",
            "Fetch sin timeout ni retry.",
        ],
        "checklist": [
            "Skill `arasaac-fetch` aplicada.",
            "Fixtures/mocks para tests offline.",
            "Métricas de hit/miss ratio.",
        ],
    },
    "semantic-search": {
        "questions": [
            "¿El índice pgvector se actualiza con la cache ARASAAC?",
            "¿Los embeddings se generan con modelo declarado y versionado?",
            "¿La búsqueda devuelve pictogramas reales (no alucinados)?",
            "¿El coste de indexación es aceptable?",
        ],
        "blockers": [
            "Búsqueda que devuelve IDs inexistentes.",
            "Modelo de embedding no reproducible.",
        ],
        "checklist": [
            "Índice reindexable con script.",
            "Tests de recall/precisión con dataset conocido.",
        ],
    },
    "export-document": {
        "questions": [
            "¿El export incluye atribución visible + manifest?",
            "¿Los pictogramas se insertan sin modificación?",
            "¿La plantilla se puede renderizar offline?",
            "¿PDF/DOCX tienen estructura semántica (etiquetado)?",
        ],
        "blockers": [
            "Export sin manifest.",
            "Atribución solo en metadata.",
            "Recoloreado/rescalado de pictogramas.",
        ],
        "checklist": [
            "Skill `export-with-manifest` aplicada.",
            "Snapshot tests de plantillas.",
            "PDF etiquetado (accesible).",
        ],
    },
    "devops": {
        "questions": [
            "¿El cambio pasa CI local con `docker-compose up`?",
            "¿Las variables sensibles están en `.env.example` documentadas y NO en el repo?",
            "¿El workflow CI cubre lint + typecheck + tests + packs sync?",
            "¿Los healthchecks funcionan?",
        ],
        "blockers": [
            "Secreto en el repo.",
            "CI verde con tests apagados.",
            "Compose que no arranca en clean checkout.",
        ],
        "checklist": [
            "Documentado en `docs/deployment/`.",
            "Imágenes docker con tag versionado (no solo `latest`).",
            "Backup/restore documentado.",
        ],
    },
    "qa": {
        "questions": [
            "¿Todos los escenarios de `spec.md` tienen test o smoke check?",
            "¿Se cubren happy path + errores + edge cases?",
            "¿Los tests son deterministas (sin flakiness)?",
            "¿Hay regresiones ocultas?",
        ],
        "blockers": [
            "Escenario de spec sin test.",
            "Test flaky pendiente por > 1 semana.",
        ],
        "checklist": [
            "Tests corren en CI en < 15 min.",
            "Reporte de coverage disponible.",
        ],
    },
    "accessibility-qa": {
        "questions": [
            "¿Axe pasa sin critical/serious?",
            "¿Navegable con teclado + lector de pantalla?",
            "¿Contraste AA en modo claro Y oscuro?",
            "¿Iconos siempre acompañados de texto/label?",
        ],
        "blockers": [
            "Axe con violaciones críticas silenciadas.",
            "Modal sin trap focus.",
            "Focus invisible.",
        ],
        "checklist": [
            "Skill `a11y-audit` aplicada.",
            "Test manual con teclado.",
            "Screenshot de estados accesibles.",
        ],
    },
    "test-automation": {
        "questions": [
            "¿La pirámide de tests es sana (unit > contract > e2e)?",
            "¿Los tests son independientes y paralelizables?",
            "¿Se ejecutan en CI y localmente con el mismo comando?",
            "¿Fixtures reutilizables entre tests?",
        ],
        "blockers": [
            "Tests dependientes de orden.",
            "E2E sin cleanup.",
        ],
        "checklist": [
            "Coverage razonable (según componente).",
            "Sin `.skip` sin ticket asociado.",
        ],
    },
    "observability": {
        "questions": [
            "¿Se emiten eventos clave (create_material, approve, export)?",
            "¿Los logs son estructurados (JSON) y sin PII?",
            "¿Hay métricas de latencia y errores?",
            "¿El audit log es inmutable y consultable?",
        ],
        "blockers": [
            "Log con PII.",
            "Sin audit log en acción sensible (aprobar, exportar).",
        ],
        "checklist": [
            "Eventos versionados.",
            "Dashboard mínimo (aunque sea local).",
        ],
    },
    "documentation": {
        "questions": [
            "¿La documentación refleja el estado real (no aspiracional)?",
            "¿Cada doc tiene audiencia clara?",
            "¿Los enlaces internos funcionan?",
            "¿Hay 'Ver también' con referencias cruzadas?",
        ],
        "blockers": [
            "README obsoleto.",
            "Enlaces rotos.",
        ],
        "checklist": [
            "Skill `docs-generate` aplicada.",
            "Índices actualizados.",
        ],
    },
    "easy-reading": {
        "questions": [
            "¿Frases < 15 palabras?",
            "¿Voz activa, sujeto-verbo-objeto?",
            "¿Vocabulario común, glosario para tecnicismos?",
            "¿Ejemplos concretos en vez de abstracción?",
        ],
        "blockers": [
            "Traducción literal sin simplificación.",
            "Ausencia de validación con persona del colectivo diana.",
        ],
        "checklist": [
            "Doble revisión (adaptador + validador).",
            "Estructura predecible por sección.",
        ],
    },
    "ux-accessibility": {
        "questions": [
            "¿El diseño respeta el design system (Serena)?",
            "¿Los estados (hover/focus/active/disabled) son claros?",
            "¿Los mensajes de error explican qué hacer?",
            "¿La densidad de información se puede reducir para usuarios que lo necesiten?",
        ],
        "blockers": [
            "Modal sin cierre por teclado.",
            "Formulario sin indicación de campo obligatorio.",
        ],
        "checklist": [
            "Iconografía consistente.",
            "Espaciado y jerarquía visual coherentes.",
        ],
    },
    "openspec-steward": {
        "questions": [
            "¿La change tiene los 4 archivos (proposal, design, tasks, spec)?",
            "¿`spec.md` es verificable (no aspiracional)?",
            "¿`tasks.md` tiene tareas atómicas?",
            "¿Precedencias/dependencias con otras changes documentadas?",
        ],
        "blockers": [
            "Change sin alguno de los 4 archivos.",
            "Spec con requisitos vagos ('debe funcionar bien').",
        ],
        "checklist": [
            "Skill `openspec-lifecycle` aplicada.",
            "Referencia a gates críticos.",
        ],
    },
    "release-manager": {
        "questions": [
            "¿La versión semántica es correcta (major/minor/patch)?",
            "¿Las release notes cubren cambios usuario + técnicos + compliance?",
            "¿El PR tiene aprobaciones y CI verde?",
            "¿Hay plan de rollback si algo falla?",
        ],
        "blockers": [
            "Release sin `human_review` documentado.",
            "Release notes ausentes.",
        ],
        "checklist": [
            "Tag git creado.",
            "CHANGELOG actualizado.",
            "Comunicación a stakeholders preparada.",
        ],
    },
}


def render_persona(entry: dict, content: dict) -> str:
    name = entry["name"]
    role = entry["role"]
    scope = entry.get("scope", [])
    gates = entry.get("gates_enforced", [])
    frontmatter = (
        "---\n"
        f"name: {name}\n"
        f"role: {role}\n"
        f"scope: {scope}\n"
        f"gates_enforced: {gates}\n"
        "---\n\n"
    )
    body = f"# Persona: {role}\n\n"
    body += "> Persona de dominio invocada internamente por los agentes-fase. "
    body += "No es seleccionable en la UI del IDE.\n\n"
    body += "## Preguntas que debo hacer\n\n"
    for q in content["questions"]:
        body += f"- {q}\n"
    body += "\n## Bloqueos que debo levantar\n\n"
    for b in content["blockers"]:
        body += f"- ❌ {b}\n"
    body += "\n## Checklist obligatoria\n\n"
    for c in content["checklist"]:
        body += f"- [ ] {c}\n"
    body += "\n## Ver también\n\n"
    body += "- Gates: [`mandatory-gates.md`](../rules/mandatory-gates.md)\n"
    body += "- Agentes que me invocan: ver `.agents/catalog/agents.yaml`\n"
    return frontmatter + body


def main() -> None:
    data = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    for entry in data["personas"]:
        name = entry["name"]
        content = PERSONA_CONTENT.get(name)
        if not content:
            print(f"⚠️  Sin contenido definido para {name} — se omite")
            continue
        target = OUT / f"{name}.persona.md"
        target.write_text(render_persona(entry, content), encoding="utf-8")
        print(f"✅ {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
