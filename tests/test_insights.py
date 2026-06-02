from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_insights():

    response = client.get("/stores/1/insights")

    assert response.status_code == 200

    data = response.json()

    assert "top_brand" in data
    assert "top_category" in data
    assert "revenue" in data