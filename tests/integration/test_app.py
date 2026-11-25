from fastapi.testclient import TestClient


def test_health_reports_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["mode"] == "solo"


def test_home_page_renders(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "VSHMS is running" in response.text
