from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_review_endpoint():
    payload = {"patient": {"name_title": "Test", "problem_description": "fall"}, "assessment": {"oxygen_saturation": 90}, "observations": []}
    response = client.post("/api/review", json=payload)
    assert response.status_code == 200
    assert response.json()["score"] < 100
    assert "summary_en" in response.json()
