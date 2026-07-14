---
name: a11y-audit
description: Auditoría WCAG 2.2 AA + keyboard + focus + color-independence + labels + cognitive.
inputs:
  - target        # page_url | component_path | material_id
outputs:
  - Report con secciones: axe, keyboard, focus, contrast, labels, cognitive
  - PASS / WARN / FAIL por sección
invoked_by_agents: [verify]
gates: []
---

# Skill: a11y-audit

## Cuándo usarla
- La change modifica `apps/web/**` o `packages/ui/**`.
- El material tiene componentes interactivos.
- Antes de release.

## Procedimiento paso a paso

### 1. Axe scan automatizado
```bash
pnpm --filter web test:a11y  # o playwright + @axe-core/playwright
```
- Sin violaciones "serious" o "critical".
- Warnings "moderate" documentados o corregidos.

### 2. Keyboard navigation
- Tab recorre todos los elementos interactivos en orden lógico.
- Shift+Tab retrocede correctamente.
- Enter/Space activan botones y links.
- Escape cierra modales/menús.
- **FAIL** si un elemento interactivo es inalcanzable por teclado.

### 3. Focus visible
- Cada elemento con focus tiene indicador visual (outline ≥ 2px, contraste ≥ 3:1).
- No hay `outline: none` sin reemplazo.
- **FAIL** si focus invisible.

### 4. Contrast (WCAG AA)
- Texto normal ≥ 4.5:1.
- Texto grande (≥ 18pt o 14pt bold) ≥ 3:1.
- Componentes UI (bordes, iconos) ≥ 3:1.
- Comprobar en modo claro Y oscuro.

### 5. Color independence
- La información no se transmite solo por color (usar iconos, texto, patrones).
- **FAIL** si estado (error/success/warning) diferenciado únicamente por color.

### 6. Labels y roles ARIA
- Cada input tiene `<label>` asociado.
- Cada botón tiene texto o `aria-label`.
- Roles ARIA correctos (`role="button"` solo si no es `<button>`).
- `aria-live` en regiones dinámicas.
- Landmarks: `<main>`, `<nav>`, `<header>`, `<footer>`.

### 7. Cognitive accessibility
- Textos comprensibles (aplicar checks de [`compliance-scan`](../compliance-scan/SKILL.md) §5).
- Iconos con texto asociado.
- Errores explican qué hacer (no solo "campo inválido").
- Tiempo suficiente en operaciones (no timeouts agresivos).

## Reporte tipo

```md
## A11y audit — <target>
| Check | Status | Findings |
|---|---|---|
| Axe | ✅ PASS | 0 critical, 0 serious, 2 moderate (docs) |
| Keyboard | ✅ PASS | Todos alcanzables |
| Focus visible | ⚠️ WARN | Botón X con outline débil |
| Contrast | ✅ PASS | Textos ≥ 4.5:1 |
| Color independence | ✅ PASS | Estados con icono + texto |
| Labels/ARIA | ✅ PASS | |
| Cognitive | ⚠️ WARN | Mensaje error de form Y poco claro |
```

## Errores comunes

- ❌ Axe verde ≠ accesible: complementa con checks manuales de teclado.
- ❌ Silenciar reglas de axe sin justificación técnica.
- ❌ `role="presentation"` en elementos interactivos.
- ❌ Modales sin trap-focus o sin cerrar con Escape.

## Ver también

- Personas: `accessibility-qa`, `a11y-cognitive`, `ux-accessibility`
- Skill: [`compliance-scan`](../compliance-scan/SKILL.md) §Plain language
- Doc: `docs/testing/test-plan-mvp0.md`
