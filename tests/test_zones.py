from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_zones():

    response = client.get("/stores/1/zones")

    assert response.status_code == 200

    data = response.json()

    assert "zones" in data