from datetime import UTC, datetime

from fastapi.testclient import TestClient

from arasaac_platform.api.pictograms import get_arasaac_client
from arasaac_platform.domain.materials import PictogramReference
from arasaac_platform.main import app


class StubArasaacClient:
    async def search(
        self,
        query: str,
        *,
        locale: str = "es",
        limit: int = 12,
    ) -> list[PictogramReference]:
        return [reference(query)][:limit]

    async def get(
        self,
        pictogram_id: int,
        *,
        locale: str = "es",
    ) -> PictogramReference:
        return reference("detalle", pictogram_id)


def reference(label: str, pictogram_id: int = 101) -> PictogramReference:
    return PictogramReference.model_validate(
        {
            "pictogram_id": pictogram_id,
            "label": label,
            "source_url": (
                f"https://static.arasaac.org/pictograms/"
                f"{pictogram_id}/{pictogram_id}_300.png"
            ),
            "retrieved_at": datetime.now(UTC),
        }
    )


def client() -> TestClient:
    app.dependency_overrides[get_arasaac_client] = StubArasaacClient
    return TestClient(app)


def test_search_endpoint_returns_traced_candidates() -> None:
    response = client().post(
        "/api/pictograms/search",
        json={"query": "casa", "limit": 1},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["requires_human_selection"] is True
    assert body["candidates"][0]["origin"] == "ARASAAC"
    assert body["candidates"][0]["author"] == "Sergio Palao"


def test_search_endpoint_rejects_extra_input() -> None:
    response = client().post(
        "/api/pictograms/search",
        json={"query": "casa", "arbitrary_url": "https://example.com"},
    )

    assert response.status_code == 422


def test_detail_endpoint_validates_path_and_locale() -> None:
    test_client = client()

    assert test_client.get("/api/pictograms/0").status_code == 422
    assert test_client.get("/api/pictograms/1?locale=xx").status_code == 422
    assert test_client.get("/api/pictograms/6964").status_code == 200
