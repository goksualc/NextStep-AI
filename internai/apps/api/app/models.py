"""
Pydantic models for InternAI API.
"""

from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """User profile model."""

    name: str | None = Field(None, description="Full name of the user")
    email: str | None = Field(None, description="Email address")
    linkedin_url: str | None = Field(None, description="LinkedIn profile URL")
    resume_url: str | None = Field(None, description="URL to resume/CV file")
    skills: list[str] | None = Field(None, description="List of user skills")


class JobItem(BaseModel):
    """Job/internship opportunity model."""

    id: str = Field(..., description="Unique identifier for the job")
    source: str = Field(
        ..., description="Source of the job posting (e.g., 'linkedin', 'indeed')"
    )
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: str | None = Field(None, description="Job location")
    url: str = Field(..., description="URL to the job posting")
    desc: str | None = Field(None, description="Job description")


class MatchResult(BaseModel):
    """Result of matching a user profile with a job."""

    job: JobItem = Field(..., description="The matched job")
    score: float = Field(..., ge=0, le=100, description="Match score (0-100)")
    missing_skills: list[str] = Field(
        default_factory=list, description="Skills the user lacks for this job"
    )


class WriteRequest(BaseModel):
    """Request for writing application materials."""

    job: JobItem = Field(..., description="Job to write application for")
    profile: UserProfile = Field(..., description="User profile information")


class CoachRequest(BaseModel):
    """Request for career coaching."""

    role: str = Field(..., description="Target role or position")
    company: str | None = Field(None, description="Target company (optional)")
    profile: UserProfile | None = Field(None, description="User profile (optional)")


class AnalyzeRequest(BaseModel):
    """Request for profile analysis."""

    text: str | None = Field(None, description="Resume text to analyze")
    resume_text: str | None = Field(
        None, description="Alternative field for resume text"
    )


class AnalyzeResponse(BaseModel):
    """Response from profile analysis."""

    skills: list[str] = Field(..., description="Extracted skills from profile")
    highlights: list[str] = Field(
        default_factory=list, description="Key highlights from the profile"
    )
    profile_text: str = Field("", description="Summarized profile text")


class WriteResponse(BaseModel):
    """Response from application writing."""

    cover_letter: str = Field(..., description="Generated cover letter")


class QuestionItem(BaseModel):
    """Individual interview question with guidance."""

    q: str = Field(..., description="The interview question")
    ideal_answer: str = Field(..., description="Guidance for answering the question")


class CoachResponse(BaseModel):
    """Response from career coaching."""

    questions: list[QuestionItem] = Field(
        ..., description="Interview questions with guidance"
    )
    tips: list[str] = Field(..., description="Career tips and advice")
