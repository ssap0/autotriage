import pytest
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path
import json

client = TestClient(app)


def test_read_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello World"


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_email():
    """Test the category endpoint."""
    # Data file path
    dataFile = Path("data/emails.json")
    # for each data send and print out result using functions
    with open(dataFile, "r", encoding="utf-8") as f:
        data = json.load(f)
        for email in data:
            response = client.post("/email", json = data)
            assert response.status_code == 200
            responseJson = response.json()
            print(responseJson)
   
