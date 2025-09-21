"""
Tests for main FastAPI application.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns API info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "InternAI API"
    assert data["version"] == "1.0.0"


def test_health_endpoint():
    """Test health endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["status"] == "healthy"


def test_api_info_endpoint():
    """Test API info endpoint returns feature list."""
    response = client.get("/api/info")
    assert response.status_code == 200
    data = response.json()
    assert "features" in data
    assert "cv_analyzer" in data["features"]
