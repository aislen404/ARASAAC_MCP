---
name: arasaac-fetch
description: Consultar API de ARASAAC, normalizar metadata, cachear y generar entrada de manifest.
inputs:
  - query        # búsqueda por keyword
  - locale       # "es" / "en" / etc.
  - pictogram_id # opcional (búsqueda directa)
outputs:
  - Pictogram metadata (id, url, author, license, retrieved_at)
  - Cache entry
  - Manifest entry (para export)
invoked_by_agents: [build]
gates: [license]
---

# Skill: arasaac-fetch

## Cuándo usarla
- Un material necesita pictogramas ARASAAC.
- Vas a integrar la API ARASAAC en backend o script.
- Actualizas cache de pictogramas.

## Procedimiento paso a paso

1. **Validar entrada**:
   - `query` no vacío o `pictogram_id` válido.
   - `locale` en whitelist (`es`, `en`, `fr`, `pt`, `ca`, `gl`, `eu`).
2. **Consultar cache local** primero (Redis o filesystem según config del proyecto).
3. **Si miss**, llamar a la API oficial ARASAAC:
   - Endpoint: `https://api.arasaac.org/api/pictograms/<locale>/search/<query>`
   - Timeout 10s, retry con backoff exponencial (máx 3).
   - Respetar rate limit.
4. **Normalizar metadata** al esquema interno:
   ```json
   {
     "id": 2547,
     "url": "https://api.arasaac.org/api/pictograms/2547",
     "author": "Sergio Palao",
     "owner": "Gobierno de Aragón",
     "license": "CC BY-NC-SA",
     "keywords": ["comer", "eating"],
     "locale": "es",
     "retrieved_at": "2025-01-20T14:32:00Z"
   }
   ```
5. **Cachear** con TTL razonable (días para metadata, permanente para el binario).
6. **Generar entrada de manifest** (para export con atribución):
   ```json
   {
     "pictogram_id": 2547,
     "used_in": "material-abc.pdf",
     "attribution": "Autor: Sergio Palao. Origen: ARASAAC (http://www.arasaac.org). Licencia: CC BY-NC-SA. Propiedad: Gobierno de Aragón."
   }
   ```
7. **Devolver** metadata + manifest entry al llamador.

## Gate `license`

**Obligatorio**: cada pictograma cacheado debe conservar `author`, `owner`, `license`, `url`. Si la API no los devuelve, no cachear y logear error.

## Ejemplo

```python
from services.api.arasaac import fetch_pictogram

pic = fetch_pictogram(query="comer", locale="es")
assert pic.license == "CC BY-NC-SA"
```

## Errores comunes

- ❌ Cachear sin metadata de licencia → viola gate `license`.
- ❌ Modificar el SVG/PNG del pictograma → viola regla absoluta #3.
- ❌ Ignorar rate limit → baneo temporal de la API.
- ❌ Usar API no oficial o scraping → puede violar términos.

## Ver también

- Skill: [`export-with-manifest`](../export-with-manifest/SKILL.md)
- Regla: `.agents/rules/mandatory-gates.md#gate-1--license`
- Política: `docs/compliance/arasaac-license-policy.md`
