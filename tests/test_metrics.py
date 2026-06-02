from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_metrics():

    response = client.get("/stores/1/metrics")

    assert response.status_code == 200

    data = response.json()

    assert "entries" in data
    assert "exits" in data
    assert "active_visitors" in data