# Spec — PDF Export Offline Test Isolation

## MUST

- MUST expose the PDF export image fetcher as an overridable FastAPI
  dependency (`get_image_fetcher`) in `arasaac_platform.api.materials`.
- MUST default to the real ARASAAC image fetcher when no override is
  configured (no behavior change in production).
- MUST allow tests to override the fetcher via
  `app.dependency_overrides[get_image_fetcher]` without touching
  `services/export.py`.
- MUST NOT require live network access to `static.arasaac.org` for the
  default API test suite (`pytest services/api/tests`) to pass.
- MUST keep the `/api/materials/{id}/export?format=pdf` contract unchanged
  (same request/response shape, same 409 on non-approved material).

## SHOULD

- SHOULD reuse the existing dependency-override pattern already used for
  `get_repository`, for consistency across the API module.

## Scenarios

1. **Approved agenda, offline test environment**: given a material approved
   through the normal workflow, when `GET /export?format=pdf` is called with
   the image fetcher overridden to an in-memory fake, then the response is
   `200` with `media_type = "application/pdf"` and no outbound HTTP call is
   made.
2. **No override configured (production/default)**: given no
   `dependency_overrides` entry for `get_image_fetcher`, when
   `export_material` runs, then it resolves and uses the real ARASAAC image
   fetcher exactly as before this change.
