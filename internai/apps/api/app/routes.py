"""
API routes for InternAI services.
"""

# Import embeddings from the local package
import json
import sys
from pathlib import Path

import numpy as np
from fastapi import APIRouter

from .cv_parser import analyze_profile
from .llm import draft_cover_letter, interview_coach
from .models import (
    AnalyzeRequest,
    AnalyzeResponse,
    CoachRequest,
    CoachResponse,
    JobItem,
    MatchResult,
    QuestionItem,
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
    """Load sample jobs from the API's data directory."""
    global _sample_jobs_cache
    if _sample_jobs_cache is None:
        try:
            # Path to the sample jobs JSON file in the API data directory
            sample_jobs_path = Path(__file__).parent / "data" / "sample_jobs.json"
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
    # Programming Languages
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",
    "go",
    "rust",
    "swift",
    "kotlin",
    "php",
    "ruby",
    "scala",
    "r",
    "matlab",
    "sql",
    # Frameworks & Libraries
    "react",
    "vue",
    "angular",
    "node.js",
    "express",
    "django",
    "flask",
    "fastapi",
    "spring",
    "laravel",
    "rails",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    # Databases
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "elasticsearch",
    "sqlite",
    "cassandra",
    "dynamodb",
    "neo4j",
    # Cloud Platforms
    "aws",
    "azure",
    "gcp",
    "google cloud",
    "amazon web services",
    "microsoft azure",
    "cloudflare",
    # DevOps Tools
    "docker",
    "kubernetes",
    "terraform",
    "jenkins",
    "gitlab",
    "github actions",
    "ansible",
    "prometheus",
    "grafana",
    "elk stack",
    # AI/ML
    "machine learning",
    "deep learning",
    "neural networks",
    "nlp",
    "natural language processing",
    "computer vision",
    "reinforcement learning",
    "data science",
    "data analysis",
    "mlops",
    # Blockchain
    "blockchain",
    "web3",
    "solidity",
    "ethereum",
    "smart contracts",
    "defi",
    "nft",
    "cairo",
    "starknet",
    "zkproofs",
    "zero knowledge",
    # Security
    "cybersecurity",
    "penetration testing",
    "vulnerability assessment",
    "security auditing",
    "cryptography",
    "network security",
    # DevRel
    "developer relations",
    "technical writing",
    "community management",
    "developer advocacy",
    "content creation",
    "documentation",
    # Data Engineering
    "data engineering",
    "etl",
    "data pipelines",
    "apache spark",
    "kafka",
    "airflow",
    "data warehousing",
    "big data",
    # General
    "git",
    "linux",
    "bash",
    "agile",
    "scrum",
    "devops",
    "ci/cd",
    "rest api",
    "graphql",
    "microservices",
    "api development",
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
async def analyze_profile_endpoint(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Analyze user profile and extract skills from resume text.

    Args:
        request: AnalyzeRequest with text or resume_text

    Returns:
        AnalyzeResponse: Extracted skills, highlights, and profile text
    """
    try:
        # Get text from either field
        text = request.text or request.resume_text or ""

        if not text.strip():
            return AnalyzeResponse(
                skills=["Python", "JavaScript", "Git", "Problem Solving"],
                highlights=["Strong analytical skills", "Team collaboration"],
                profile_text="Basic technical profile",
            )

        # Use CV parser for comprehensive analysis
        result = await analyze_profile(text)

        return AnalyzeResponse(
            skills=result["skills"],
            highlights=result["highlights"],
            profile_text=result["profile_text"],
        )

    except Exception as e:
        print(f"Error in profile analysis: {e}")
        # Fallback response
        return AnalyzeResponse(
            skills=["Python", "JavaScript", "Git", "Problem Solving"],
            highlights=["Strong analytical skills", "Team collaboration"],
            profile_text="Basic technical profile",
        )


def _build_profile_text(profile: UserProfile) -> str:
    """Build a comprehensive profile text from user data."""
    parts = []

    # Add skills
    if profile.skills:
        parts.append(f"Skills: {', '.join(profile.skills)}")

    # Add name and email for context
    if profile.name:
        parts.append(f"Name: {profile.name}")
    if profile.email:
        parts.append(f"Email: {profile.email}")

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

    # Normalize profile skills for comparison
    profile_skills_lower = {skill.lower() for skill in profile.skills}
    job_desc_lower = job.desc.lower()

    missing_skills = []

    # Check each skill keyword against job description
    for skill in SKILL_KEYWORDS:
        skill_lower = skill.lower()

        # Check if skill appears in job description
        if skill_lower in job_desc_lower:
            # Check if user doesn't have this skill (exact match or partial match)
            has_skill = False
            for profile_skill in profile_skills_lower:
                if skill_lower in profile_skill or profile_skill in skill_lower:
                    has_skill = True
                    break

            if not has_skill:
                missing_skills.append(skill.title())

    # Remove duplicates and return top 5 missing skills
    unique_missing = list(dict.fromkeys(missing_skills))
    return unique_missing[:5]


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
    try:
        # Use LLM to generate cover letter
        cover_letter = await draft_cover_letter(request.job, request.profile)
        return WriteResponse(cover_letter=cover_letter)

    except Exception as e:
        print(f"Error generating cover letter: {e}")
        # Fallback to template-based cover letter
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
    try:
        # Extract skills from profile for better coaching
        skills = (
            request.profile.skills if request.profile and request.profile.skills else []
        )

        # Use LLM to generate coaching content
        coaching_data = await interview_coach(
            request.role, request.company or "", skills
        )

        # Convert questions to QuestionItem objects
        question_items = []
        for q in coaching_data["questions"]:
            if isinstance(q, dict):
                question_items.append(
                    QuestionItem(
                        q=q.get("q", ""),
                        ideal_answer=q.get(
                            "ideal_answer",
                            "Provide a specific example from your experience.",
                        ),
                    )
                )
            else:
                question_items.append(
                    QuestionItem(
                        q=str(q),
                        ideal_answer="Provide a specific example from your experience.",
                    )
                )

        return CoachResponse(questions=question_items, tips=coaching_data["tips"])

    except Exception as e:
        print(f"Error generating coaching: {e}")
        # Fallback to template-based coaching
        fallback_questions = [
            QuestionItem(
                q=f"Tell me about your experience with {request.role}.",
                ideal_answer="Focus on specific projects, technologies, or experiences that demonstrate your passion and relevant skills.",
            ),
            QuestionItem(
                q=f"What interests you most about working in {request.role}?",
                ideal_answer="Show genuine enthusiasm and explain how this role aligns with your career goals.",
            ),
            QuestionItem(
                q="Describe a challenging project you've worked on and how you overcame obstacles.",
                ideal_answer="Use the STAR method: describe the Situation, Task, Action you took, and Result achieved.",
            ),
            QuestionItem(
                q="How do you stay updated with the latest trends in your field?",
                ideal_answer="Mention specific resources like blogs, courses, conferences, or communities you follow.",
            ),
            QuestionItem(
                q="Where do you see yourself in 5 years?",
                ideal_answer="Show long-term thinking while demonstrating how this role is a stepping stone.",
            ),
        ]

        # Add company-specific question if provided
        if request.company:
            fallback_questions.append(
                QuestionItem(
                    q=f"What do you know about {request.company} and why do you want to work here?",
                    ideal_answer="Research their products, mission, recent news, and company culture.",
                )
            )

        # Generate tips based on role
        tips = [
            f"Research the company thoroughly before your {request.role} interview.",
            "Prepare specific examples of your achievements using the STAR method.",
            "Practice explaining technical concepts in simple terms.",
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

        return CoachResponse(questions=fallback_questions[:5], tips=tips[:3])


# Local Agent Endpoints
@router.post("/local/cv_analyzer")
async def cv_analyzer(request: dict):
    """
    CV Analyzer agent endpoint.

    Args:
        request: {"text": "..."}

    Returns:
        {"skills": [...], "highlights": [...], "profile_text": "..."}
    """
    text = request.get("text", "")

    if not text.strip():
        return {"skills": [], "highlights": [], "profile_text": ""}

    try:
        # Use CV parser for comprehensive analysis
        result = await analyze_profile(text)
        return {
            "skills": result["skills"],
            "highlights": result["highlights"],
            "profile_text": result["profile_text"],
        }

    except Exception as e:
        print(f"Error in CV analyzer: {e}")
        # Fallback to basic extraction
        return {
            "skills": ["Python", "JavaScript", "Git"],
            "highlights": [],
            "profile_text": "Basic technical skills",
        }


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
        {"cover_letter": "..."} - uses LLM for generation
    """
    job_data = request.get("job", {})
    profile_data = request.get("profile", {})

    if not job_data or not profile_data:
        return {"cover_letter": "Missing job or profile data"}

    try:
        # Convert to proper models
        job = JobItem(**job_data)
        profile = UserProfile(**profile_data)

        # Use LLM directly for cover letter generation
        cover_letter = await draft_cover_letter(job, profile)
        return {"cover_letter": cover_letter}

    except Exception as e:
        print(f"Error in app_writer: {e}")
        return {"cover_letter": f"Error generating cover letter: {str(e)}"}


@router.post("/local/coach")
async def coach(request: dict):
    """
    Interview Coach agent endpoint.

    Args:
        request: {"role": "...", "company": "...", "skills": [...]}

    Returns:
        {"questions": [...], "tips": [...]} - uses LLM for generation
    """
    role = request.get("role", "")
    company = request.get("company", "")
    skills = request.get("skills", [])

    if not role:
        return {
            "questions": [],
            "tips": ["Please provide a role to get coaching advice"],
        }

    try:
        # Use LLM directly for coaching generation
        coaching_data = await interview_coach(role, company, skills)
        return {"questions": coaching_data["questions"], "tips": coaching_data["tips"]}

    except Exception as e:
        print(f"Error in coach: {e}")
        return {"questions": [], "tips": [f"Error getting coaching advice: {str(e)}"]}
