from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_anomalies():

    response = client.get("/stores/1/anomalies")

    assert response.status_code == 200

    data = response.json()

    assert "anomalies" in data