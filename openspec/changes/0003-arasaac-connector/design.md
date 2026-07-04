# Design — 0003-arasaac-connector

El conector usa `https://api.arasaac.org/api` como base fija. El usuario nunca
proporciona URLs. Las imágenes se referencian mediante la URL oficial e inmutable
`https://static.arasaac.org/pictograms/{id}/{id}_300.png`.

Inputs: locale allowlisted, texto limitado y `limit <= 50`. Outputs: modelos
Pydantic estrictos con trazabilidad. Errores de red, timeout y payload inválido se
traducen a errores propios sin filtrar secretos.
