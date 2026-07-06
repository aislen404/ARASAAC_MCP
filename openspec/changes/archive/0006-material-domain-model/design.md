# Design — 0006-material-domain-model

Los modelos de dominio no dependen de HTTP, MCP o base de datos. Los IDs son UUID
generados por el sistema. Los únicos datos de autoría operativa son identificadores
de sesión anónimos opcionales; no existen nombre, email, diagnóstico, historia
clínica ni identificador de beneficiario.

Cada bloque usa texto genérico y una referencia inmutable a ARASAAC. El material
mantiene versión, estado, atribución, revisión y timestamps UTC.

Las transiciones permitidas son:

```text
draft -> in_review -> approved
                   -> rejected -> draft
approved -> draft (nueva versión)
```

La exportación futura solo puede aceptar `approved`.
