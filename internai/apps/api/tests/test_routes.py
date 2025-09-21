"""
Tests for API routes.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_analyze_endpoint():
    """Test analyze endpoint with sample profile."""
    profile_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "linkedin_url": "https://linkedin.com/in/johndoe",
        "skills": ["Python", "JavaScript"],
    }

    response = client.post("/v1/analyze", json=profile_data)
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data
    assert isinstance(data["skills"], list)


def test_match_endpoint():
    """Test match endpoint with sample data."""
    request_data = {
        "profile": {"name": "John Doe", "skills": ["Python", "React"]},
        "jobs": [
            {
                "id": "1",
                "source": "linkedin",
                "title": "Software Engineer",
                "company": "TechCorp",
                "url": "https://example.com/job/1",
            }
        ],
    }

    response = client.post("/v1/match", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # If we have results
        match = data[0]
        assert "job" in match
        assert "score" in match
        assert "missing_skills" in match


def test_write_endpoint():
    """Test write endpoint with sample request."""
    request_data = {
        "job": {
            "id": "1",
            "source": "linkedin",
            "title": "Software Engineer",
            "company": "TechCorp",
            "url": "https://example.com/job/1",
        },
        "profile": {"name": "John Doe", "email": "john@example.com"},
    }

    response = client.post("/v1/write", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "cover_letter" in data
    assert isinstance(data["cover_letter"], str)


def test_coach_endpoint():
    """Test coach endpoint with sample request."""
    request_data = {"role": "Software Engineer", "company": "TechCorp"}

    response = client.post("/v1/coach", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert "tips" in data
    assert isinstance(data["questions"], list)
    assert isinstance(data["tips"], list)
