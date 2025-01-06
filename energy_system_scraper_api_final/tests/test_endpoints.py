import pytest
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_scrape_data():
    response = client.get("/scrape-data")
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Data scraped, transformed, and saved successfully."}

def test_fetch_processed_data():
    response = client.get("/fetch-processed-data")
    assert response.status_code == 200
    assert "data" in response.json()

def test_fetch_all_data():
    response = client.get("/fetch-all-data")
    assert response.status_code == 200
    assert "data" in response.json()
