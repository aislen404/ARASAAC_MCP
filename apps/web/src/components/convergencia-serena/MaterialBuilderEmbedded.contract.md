# MaterialBuilder embedded adapter

El `MaterialBuilder` actual puede seguir teniendo estado local y llamadas API, pero debe aceptar una variante `embedded` o dividirse en subcomponentes. En modo embedded:

- No renderiza un grid propio que compita con el shell.
- Usa clases `cs-panel`, `cs-field`, `cs-input`, `cs-button`, `cs-chip`.
- Se organiza como:
  - Configura el material.
  - Proponer estructura con IA.
  - Buscar pictogramas reales ARASAAC.
  - Vista previa editable.
  - Revisión y exportación.
- La revisión/exportación debe estar visualmente integrada en el paso 4/5 del flujo.
