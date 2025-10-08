"""
Example test file for the Flood Forecaster API.
Run with: pytest tests/
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operational"
    assert "version" in data


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_create_flood_event():
    """Test creating a flood event."""
    flood_data = {
        "location_name": "Test Street",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "description": "Test flood event"
    }
    response = client.post("/api/v1/floods/", json=flood_data)
    assert response.status_code == 201
    data = response.json()
    assert data["location_name"] == "Test Street"
    assert "risk_score" in data
    assert "severity" in data


def test_get_flood_events():
    """Test retrieving flood events."""
    response = client.get("/api/v1/floods/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_calculate_risk():
    """Test risk calculation without saving."""
    risk_data = {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "location_name": "Test Location"
    }
    response = client.post("/api/v1/floods/calculate-risk", json=risk_data)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "severity" in data
    assert data["risk_score"] >= 0
    assert data["risk_score"] <= 100


def test_invalid_coordinates():
    """Test validation for invalid coordinates."""
    invalid_data = {
        "location_name": "Invalid Location",
        "latitude": 200,  # Invalid latitude
        "longitude": -74.0060
    }
    response = client.post("/api/v1/floods/", json=invalid_data)
    assert response.status_code == 422  # Validation error


# Add more tests as needed
