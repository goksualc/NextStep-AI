"""
API routes for InternAI services.
"""

from fastapi import APIRouter

from .models import (
    AnalyzeResponse,
    CoachRequest,
    CoachResponse,
    JobItem,
    MatchResult,
    UserProfile,
    WriteRequest,
    WriteResponse,
)

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_profile(profile: UserProfile) -> AnalyzeResponse:
    """
    Analyze user profile and extract skills from resume/LinkedIn.

    Args:
        profile: User profile information

    Returns:
        AnalyzeResponse: Extracted skills
    """
    # TODO: Implement actual profile analysis using AI/ML
    # For now, return stub data
    stub_skills = ["Python", "React", "JavaScript", "SQL", "Git"]

    return AnalyzeResponse(skills=stub_skills)


@router.post("/match", response_model=list[MatchResult])
async def match_jobs(profile: UserProfile, jobs: list[JobItem]) -> list[MatchResult]:
    """
    Match user profile with job opportunities.

    Args:
        profile: User profile information
        jobs: List of job opportunities to match against

    Returns:
        List[MatchResult]: Matched jobs with scores and missing skills
    """
    # TODO: Implement actual matching algorithm using AI
    # For now, return stub data with dummy scores
    results = []

    for i, job in enumerate(jobs):
        # Generate dummy score based on job index
        score = max(60, 95 - (i * 5))
        if score < 60:
            score = 60

        # Generate dummy missing skills
        missing_skills = []
        if i % 2 == 0:
            missing_skills = ["Machine Learning", "Docker"]
        elif i % 3 == 0:
            missing_skills = ["AWS", "Kubernetes"]
        else:
            missing_skills = ["GraphQL"]

        results.append(MatchResult(job=job, score=score, missing_skills=missing_skills))

    # Sort by score (highest first)
    results.sort(key=lambda x: x.score, reverse=True)

    return results


@router.post("/write", response_model=WriteResponse)
async def write_application(request: WriteRequest) -> WriteResponse:
    """
    Generate personalized application materials.

    Args:
        request: WriteRequest with job and profile information

    Returns:
        WriteResponse: Generated cover letter
    """
    # TODO: Implement actual application writing using AI
    # For now, return stub cover letter

    cover_letter = f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {request.job.title} position at {request.job.company}.

With my background in software development and passion for technology, I am excited about the opportunity to contribute to your team. My experience with various programming languages and frameworks aligns well with the requirements for this role.

I am particularly drawn to {request.job.company} because of your commitment to innovation and your reputation in the industry. I believe my skills and enthusiasm would make me a valuable addition to your team.

Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your organization.

Best regards,
{request.profile.name or "Applicant"}
"""

    return WriteResponse(cover_letter=cover_letter.strip())


@router.post("/coach", response_model=CoachResponse)
async def get_coaching(request: CoachRequest) -> CoachResponse:
    """
    Provide career coaching and interview preparation.

    Args:
        request: CoachRequest with role and optional company/profile info

    Returns:
        CoachResponse: Interview questions and career tips
    """
    # TODO: Implement actual coaching using AI
    # For now, return stub content

    # Generate role-specific questions
    questions = [
        f"Tell me about your experience with {request.role}.",
        f"What interests you most about working in {request.role}?",
        "Describe a challenging project you've worked on and how you overcame obstacles.",
        "How do you stay updated with the latest trends in your field?",
        "Where do you see yourself in 5 years?",
    ]

    # Add company-specific question if provided
    if request.company:
        questions.append(
            f"What do you know about {request.company} and why do you want to work here?"
        )

    # Generate tips based on role
    tips = [
        f"Research the company thoroughly before your {request.role} interview.",
        "Prepare specific examples of your achievements using the STAR method.",
        "Practice explaining technical concepts in simple terms.",
        "Prepare thoughtful questions to ask the interviewer about the role and company culture.",
        "Dress professionally and arrive 5-10 minutes early for in-person interviews.",
    ]

    # Add role-specific tips
    if "engineer" in request.role.lower():
        tips.extend(
            [
                "Be ready to discuss your coding process and problem-solving approach.",
                "Prepare to explain technical decisions and trade-offs you've made in past projects.",
            ]
        )
    elif "data" in request.role.lower():
        tips.extend(
            [
                "Be prepared to discuss your experience with data analysis tools and methodologies.",
                "Have examples ready of how you've used data to drive business decisions.",
            ]
        )

    return CoachResponse(questions=questions, tips=tips)
