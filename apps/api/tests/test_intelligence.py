from fastapi.testclient import TestClient

from yemenjpt.main import app


def test_intelligence_status(client: TestClient) -> None:
    response = client.get("/intelligence/status")
    assert response.status_code == 200
    assert response.json()["status"] == "not_implemented"