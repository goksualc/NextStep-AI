"""
API routes for InternAI services.
"""

# Import embeddings from the local package
import json
import sys
from pathlib import Path

import numpy as np
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
from .settings import get_settings

# Add the embeddings package to the path
embeddings_path = Path(__file__).parent.parent.parent.parent / "packages" / "embeddings"
sys.path.insert(0, str(embeddings_path))

try:
    # Import from the local embeddings package
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "embeddings", embeddings_path / "__init__.py"
    )
    embeddings_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(embeddings_module)

    EmbeddingsClient = embeddings_module.EmbeddingsClient
    cosine_sim = embeddings_module.cosine_sim
except Exception as e:
    print(f"Warning: Could not import embeddings module: {e}")
    print("Embeddings functionality will be disabled. Install the embeddings package.")
    EmbeddingsClient = None
    cosine_sim = None

router = APIRouter()

# Load and cache sample jobs
_sample_jobs_cache = None


def _load_sample_jobs():
    """Load sample jobs from the web app's public directory."""
    global _sample_jobs_cache
    if _sample_jobs_cache is None:
        try:
            # Path to the sample jobs JSON file in the web app
            sample_jobs_path = (
                Path(__file__).parent.parent.parent.parent
                / "apps"
                / "web"
                / "public"
                / "sample_jobs.json"
            )
            with open(sample_jobs_path) as f:
                _sample_jobs_cache = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load sample jobs: {e}")
            _sample_jobs_cache = []
    return _sample_jobs_cache


# Initialize EmbeddingsClient with settings
settings = get_settings()
embeddings_client = None

if EmbeddingsClient and settings.MISTRAL_API_KEY:
    try:
        embeddings_client = EmbeddingsClient(
            api_key=settings.MISTRAL_API_KEY, model="mistral-embed"
        )
    except Exception as e:
        print(f"Warning: Could not initialize EmbeddingsClient: {e}")
        embeddings_client = None

# Curated set of skill keywords for missing skills detection
SKILL_KEYWORDS = {
    "python",
    "javascript",
    "typescript",
    "java",
    "c++",
    "c#",
    "go",
    "rust",
    "swift",
    "kotlin",
    "react",
    "vue",
    "angular",
    "node.js",
    "express",
    "django",
    "flask",
    "fastapi",
    "spring",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "elasticsearch",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "terraform",
    "jenkins",
    "gitlab",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "graphql",
    "rest api",
    "microservices",
    "agile",
    "scrum",
    "devops",
    "ci/cd",
    "linux",
    "bash",
    "git",
    "jira",
    "confluence",
    "figma",
    "photoshop",
    "data analysis",
    "statistics",
    "r",
    "matlab",
    "tableau",
    "power bi",
    "cybersecurity",
    "penetration testing",
    "blockchain",
    "web3",
    "solidity",
}


@router.get("/jobs/sample")
async def get_sample_jobs():
    """
    Get sample job opportunities for testing and demonstration.

    Returns:
        List of sample JobItem objects
    """
    return _load_sample_jobs()


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


def _build_profile_text(profile: UserProfile) -> str:
    """Build a comprehensive profile text from user data."""
    parts = []

    # Add skills
    if profile.skills:
        parts.append(f"Skills: {', '.join(profile.skills)}")

    # Add LinkedIn profile reference
    if profile.linkedin_url:
        parts.append(f"LinkedIn: {profile.linkedin_url}")

    # Add name and email for context
    if profile.name:
        parts.append(f"Name: {profile.name}")
    if profile.email:
        parts.append(f"Email: {profile.email}")

    # Add resume reference
    if profile.resume_url:
        parts.append(f"Resume: {profile.resume_url}")

    return " | ".join(parts)


def _build_job_text(job: JobItem) -> str:
    """Build a comprehensive job text from job data."""
    parts = [f"Title: {job.title}", f"Company: {job.company}"]

    if job.location:
        parts.append(f"Location: {job.location}")

    if job.desc:
        parts.append(f"Description: {job.desc}")

    return " | ".join(parts)


def _find_missing_skills(profile: UserProfile, job: JobItem) -> list[str]:
    """Find skills present in job description but missing from profile."""
    if not profile.skills or not job.desc:
        return []

    # Check each skill keyword against job description
    missing_skills = []
    job_desc_lower = job.desc.lower()

    for skill in SKILL_KEYWORDS:
        # Check if skill appears in job description
        if skill.lower() in job_desc_lower:
            # Check if user doesn't have this skill
            if not any(
                skill.lower() in profile_skill.lower()
                for profile_skill in profile.skills
            ):
                missing_skills.append(skill.title())

    # Return top 5 missing skills
    return missing_skills[:5]


@router.post("/match", response_model=list[MatchResult])
async def match_jobs(profile: UserProfile, jobs: list[JobItem]) -> list[MatchResult]:
    """
    Match user profile with job opportunities using embeddings-based similarity.

    Args:
        profile: User profile information
        jobs: List of job opportunities to match against

    Returns:
        List[MatchResult]: Matched jobs with scores and missing skills
    """
    if not jobs:
        return []

    # Build profile text
    profile_text = _build_profile_text(profile)

    # Build job texts
    job_texts = [_build_job_text(job) for job in jobs]

    # Prepare all texts for embedding (profile + all jobs)
    all_texts = [profile_text] + job_texts

    # Check if embeddings client is available
    if embeddings_client and cosine_sim:
        try:
            # Get embeddings for all texts
            embeddings = embeddings_client.embed_texts(all_texts)

            # Extract profile embedding (first one)
            profile_embedding = np.array(embeddings[0])

            # Calculate similarities and build results
            results = []
            for i, (job, _job_text) in enumerate(zip(jobs, job_texts, strict=False)):
                # Get job embedding (i+1 because profile is at index 0)
                job_embedding = np.array(embeddings[i + 1])

                # Calculate cosine similarity
                similarity = cosine_sim(profile_embedding, job_embedding)

                # Convert to score (0-100) and round to 1 decimal
                score = round(similarity * 100, 1)

                # Find missing skills
                missing_skills = _find_missing_skills(profile, job)

                results.append(
                    MatchResult(job=job, score=score, missing_skills=missing_skills)
                )

            # Sort by score (highest first)
            results.sort(key=lambda x: x.score, reverse=True)

            return results

        except Exception as e:
            # Fallback to simple scoring if embeddings fail
            print(f"Embeddings failed, using fallback: {e}")

    # Fallback to simple scoring if embeddings client is not available
    results = []
    for i, job in enumerate(jobs):
        # Simple fallback scoring
        score = max(60, 95 - (i * 5))
        missing_skills = _find_missing_skills(profile, job)

        results.append(MatchResult(job=job, score=score, missing_skills=missing_skills))

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


# Local Agent Endpoints
@router.post("/local/cv_analyzer")
async def cv_analyzer(request: dict):
    """
    CV Analyzer agent endpoint.

    Args:
        request: {"text": "..."}

    Returns:
        {"skills": [...]}
    """
    text = request.get("text", "")

    # Simple keyword extraction for now
    # TODO: Replace with actual LLM processing

    # Common technical skills keywords
    skill_keywords = [
        "python",
        "javascript",
        "typescript",
        "java",
        "c++",
        "c#",
        "go",
        "rust",
        "react",
        "vue",
        "angular",
        "node.js",
        "express",
        "django",
        "flask",
        "fastapi",
        "sql",
        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "elasticsearch",
        "aws",
        "azure",
        "gcp",
        "docker",
        "kubernetes",
        "terraform",
        "git",
        "linux",
        "bash",
        "jenkins",
        "gitlab",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "graphql",
        "rest api",
        "microservices",
        "agile",
        "scrum",
        "devops",
        "figma",
        "photoshop",
        "illustrator",
        "sketch",
        "data analysis",
        "statistics",
        "r",
        "matlab",
        "tableau",
        "power bi",
        "cybersecurity",
        "penetration testing",
        "blockchain",
        "web3",
        "solidity",
    ]

    # Extract skills from text
    found_skills = []
    text_lower = text.lower()

    for skill in skill_keywords:
        if skill.lower() in text_lower:
            found_skills.append(skill.title())

    # Remove duplicates and return
    unique_skills = list(set(found_skills))

    return {"skills": unique_skills}


@router.post("/local/job_scout")
async def job_scout(request: dict):
    """
    Job Scout agent endpoint.

    Args:
        request: {"filters": {...}} (ignored for now)

    Returns:
        {"jobs": [...]} - same as /jobs/sample
    """
    # Return the same sample jobs as /jobs/sample
    sample_jobs = _load_sample_jobs()
    return {"jobs": sample_jobs}


@router.post("/local/matcher")
async def matcher(request: dict):
    """
    Matcher agent endpoint.

    Args:
        request: {"profile": {...}, "jobs": [...]}

    Returns:
        {"matches": [...]} - same logic as /match but wrapped
    """
    profile_data = request.get("profile", {})
    jobs_data = request.get("jobs", [])

    if not profile_data or not jobs_data:
        return {"matches": []}

    # Convert to proper models
    try:
        profile = UserProfile(**profile_data)
        jobs = [JobItem(**job) for job in jobs_data]

        # Use existing match logic
        matches = await match_jobs(profile, jobs)

        # Wrap in matches format
        return {"matches": matches}

    except Exception as e:
        print(f"Error in matcher: {e}")
        return {"matches": []}


@router.post("/local/app_writer")
async def app_writer(request: dict):
    """
    Application Writer agent endpoint.

    Args:
        request: {"job": {...}, "profile": {...}}

    Returns:
        {"cover_letter": "..."} - reuse /write logic
    """
    job_data = request.get("job", {})
    profile_data = request.get("profile", {})

    if not job_data or not profile_data:
        return {"cover_letter": "Missing job or profile data"}

    try:
        # Convert to proper models
        job = JobItem(**job_data)
        profile = UserProfile(**profile_data)

        # Create write request
        write_request = WriteRequest(job=job, profile=profile)

        # Use existing write logic
        result = await write_application(write_request)

        return {"cover_letter": result.cover_letter}

    except Exception as e:
        print(f"Error in app_writer: {e}")
        return {"cover_letter": f"Error generating cover letter: {str(e)}"}


@router.post("/local/coach")
async def coach(request: dict):
    """
    Interview Coach agent endpoint.

    Args:
        request: {"role": "...", "company": "..."}

    Returns:
        {"questions": [...], "tips": [...]} - reuse /coach logic
    """
    role = request.get("role", "")
    company = request.get("company", "")

    if not role:
        return {
            "questions": [],
            "tips": ["Please provide a role to get coaching advice"],
        }

    try:
        # Create coach request (with minimal profile)
        coach_request = CoachRequest(
            role=role,
            company=company,
            profile=UserProfile(
                name="", email="", skills=[], linkedin_url="", resume_url=""
            ),
        )

        # Use existing coach logic
        result = await get_coaching(coach_request)

        return {"questions": result.questions, "tips": result.tips}

    except Exception as e:
        print(f"Error in coach: {e}")
        return {"questions": [], "tips": [f"Error getting coaching advice: {str(e)}"]}
