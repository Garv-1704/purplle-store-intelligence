from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_funnel():

    response = client.get("/stores/1/funnel")

    assert response.status_code == 200

    data = response.json()

    assert "conversion_rate" in data
    assert "transactions" in data