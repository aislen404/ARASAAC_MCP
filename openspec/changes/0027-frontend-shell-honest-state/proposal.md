# Proposal — 0027 Frontend Shell Honest State

## Problema

El shell Convergencia Serena (0026) reproduce la dirección visual, pero varios bloques muestran datos inventados, controles sin efecto y jerarquía visual confusa:

- Buscador de cabecera sin función.
- Badges de accesibilidad que se desbordan y se confunden con el toggle de tema.
- Icono de navegación activa invisible en el menú lateral.
- Métricas de progreso y validación con valores hardcodeados.
- Tarjeta "Continuar" con borrador ficticio y botón inactivo.
- Sugerencias con maquetación inconsistente y enlace erróneo.
- Asistente IA sin feedback visible de estado, carga o errores.

Esto erosiona la confianza del usuario y contradice el principio de revisión humana y transparencia.

## Cambio propuesto

Conectar el shell al estado real del constructor de materiales y eliminar controles muertos:

1. Eliminar buscador de cabecera.
2. Clarificar jerarquía visual entre badges informativos y controles interactivos.
3. Corregir contraste del icono activo en navegación lateral.
4. Derivar métricas, continuar y sugerencias del flujo real (`MaterialBuilderProvider`).
5. Mostrar estado vacío honesto (ceros) cuando no hay progreso.
6. Mejorar feedback del asistente IA en el paso de creación.

## Fuera de alcance

- Búsqueda global de materiales o colecciones persistentes.
- Cambios en endpoints backend o gobernanza ARASAAC.
- Autenticación o perfiles de usuario reales.
- Generación de pictogramas con IA.

## Valor

El shell deja de simular actividad y refleja el estado real del flujo guiado, reforzando credibilidad y accesibilidad.
