"""
Tests for Pydantic models.
"""

from app.models import CoachRequest, JobItem, MatchResult, UserProfile, WriteRequest


def test_user_profile_model():
    """Test UserProfile model validation."""
    # Test with all fields
    profile = UserProfile(
        name="John Doe",
        email="john@example.com",
        linkedin_url="https://linkedin.com/in/johndoe",
        resume_url="https://example.com/resume.pdf",
        skills=["Python", "React"],
    )
    assert profile.name == "John Doe"
    assert profile.skills == ["Python", "React"]

    # Test with minimal fields
    minimal_profile = UserProfile()
    assert minimal_profile.name is None
    assert minimal_profile.skills is None


def test_job_item_model():
    """Test JobItem model validation."""
    job = JobItem(
        id="123",
        source="linkedin",
        title="Software Engineer",
        company="TechCorp",
        url="https://example.com/job/123",
    )
    assert job.id == "123"
    assert job.source == "linkedin"
    assert job.location is None  # Optional field


def test_match_result_model():
    """Test MatchResult model validation."""
    job = JobItem(
        id="123",
        source="linkedin",
        title="Software Engineer",
        company="TechCorp",
        url="https://example.com/job/123",
    )

    match = MatchResult(job=job, score=85.5, missing_skills=["Docker", "AWS"])
    assert match.score == 85.5
    assert match.missing_skills == ["Docker", "AWS"]


def test_write_request_model():
    """Test WriteRequest model validation."""
    job = JobItem(
        id="123",
        source="linkedin",
        title="Software Engineer",
        company="TechCorp",
        url="https://example.com/job/123",
    )

    profile = UserProfile(name="John Doe")

    request = WriteRequest(job=job, profile=profile)
    assert request.job.company == "TechCorp"
    assert request.profile.name == "John Doe"


def test_coach_request_model():
    """Test CoachRequest model validation."""
    request = CoachRequest(role="Software Engineer")
    assert request.role == "Software Engineer"
    assert request.company is None
    assert request.profile is None

    # Test with optional fields
    profile = UserProfile(name="John Doe")
    full_request = CoachRequest(
        role="Data Scientist", company="DataCorp", profile=profile
    )
    assert full_request.role == "Data Scientist"
    assert full_request.company == "DataCorp"
    assert full_request.profile.name == "John Doe"
