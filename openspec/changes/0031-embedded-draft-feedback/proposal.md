# Proposal — 0031 Embedded Draft Feedback

## Problema

En la vista integrada del constructor de materiales, al pulsar `Crear borrador` puede parecer que no ocurre nada. La acción ejecuta `createMaterial()` y actualiza el estado del builder, pero el feedback no se muestra junto al botón y el panel de revisión embebido oculta el mensaje compartido.

Esto genera una falsa impresión de fallo, dificulta comprender el siguiente paso del flujo y reduce la confianza en la interfaz guiada.

## Cambio propuesto

1. Mostrar feedback visible y accesible junto al botón `Crear borrador` en `EditorPanel`.
2. Mantener visible el mensaje compartido en `ReviewPanel` también en modo embebido.
3. Asegurar que el estado `draft` se perciba claramente tras la creación del borrador.
4. Cubrir el flujo con tests de frontend del modo embebido.

## Fuera de alcance

- Cambios en endpoints backend de materiales.
- Persistencia adicional o nuevas transiciones de workflow.
- Cambios en exportación o revisión humana.

## Valor

La vista integrada comunica de forma honesta y accesible que el borrador se ha creado y cuál es el siguiente paso, sin depender de inspección técnica ni de feedback lejano al control accionado.
