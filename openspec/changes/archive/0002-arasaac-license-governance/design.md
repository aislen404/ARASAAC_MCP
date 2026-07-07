# Design — 0002-arasaac-license-governance

## Fuente

La política se deriva de las condiciones oficiales publicadas en
`https://arasaac.org/terms-of-use`.

## Invariantes

- `commercial_use=false`.
- Licencia exacta `CC BY-NC-SA`.
- Origen `ARASAAC`.
- Autor `Sergio Palao`.
- Propietario `Gobierno de Aragón`.
- Cada uso conserva ID, label, URL y fecha de recuperación.
- Toda salida final conserva atribución visible.
- Señalética declara la necesidad del logotipo ARASAAC.

Los modelos son `frozen` para impedir que otra capa altere metadatos de licencia.
Los validadores devuelven problemas estructurados y nunca corrigen o modifican un
pictograma.
