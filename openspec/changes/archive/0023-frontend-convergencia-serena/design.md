# Design — 0023-frontend-convergencia-serena

## Decisión

Convergencia Serena se implementará como una capa de diseño y orientación sobre
el flujo gobernado existente. No se reemplaza el constructor ni se alteran sus
garantías.

## Arquitectura

```text
apps/web/src/
  app/
    layout.tsx
    page.tsx
    material-builder.tsx
    styles.css
  components/
    app-shell.tsx
    guided-flow.tsx
    theme-toggle.tsx
  design-system/
    tokens.css
    README.md
```

`page.tsx` compone el shell y el constructor. Los componentes puramente
presentacionales reciben datos constantes sin PII. `ThemeToggle` es el único
componente cliente nuevo y aplica `data-theme` al elemento raíz.

## Sistema visual

- Marfil, navy, salvia, cobre y cian de foco en light.
- Midnight, superficies escalonadas, salvia clara, amber y cian en dark.
- Escala de espaciado de 4 a 64 px.
- Targets interactivos mínimos de 44 px.
- Estados con texto o símbolo además del color.
- Movimiento reducido cuando el sistema lo solicita.

## Flujo guiado adaptado

Las fases se expresan en términos compatibles con el producto actual:

1. Definir necesidad.
2. Explorar pictogramas.
3. Organizar material.
4. Validar accesibilidad.
5. Revisar y compartir.

El constructor permanece como área principal de trabajo. La navegación del shell
usa anclas a secciones existentes o informativas; no promete rutas sin
implementar.

## Tema

El botón usa `aria-pressed`, nombre visible y un target de 44 px. La preferencia
se guarda en `localStorage` y se aplica a `document.documentElement`. Sin
JavaScript, el tema claro sigue siendo funcional.

## Accesibilidad

- landmarks y encabezados en orden;
- skip link;
- `aria-current="step"` en la fase activa;
- foco visible global;
- estado de tema anunciado por texto y `aria-pressed`;
- navegación responsive sin ocultar acciones críticas;
- axe sin incidencias serious/critical.

## Compliance precheck

- No se añaden ni modifican pictogramas.
- No se incorpora generación visual por IA.
- No se cambia la atribución visible.
- No se rebaja el gate de revisión humana.
- No se añaden datos personales ni contenido diagnóstico.
- No se añaden endpoints ni tools MCP.
