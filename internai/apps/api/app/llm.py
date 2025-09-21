"""
LLM integration module for InternAI using Mistral AI.
"""

import json
import re

from mistralai import Mistral

from .settings import settings

# Initialize Mistral client
mistral = Mistral(api_key=settings.MISTRAL_API_KEY)


async def draft_cover_letter(job, profile) -> str:
    """
    Generate a professional cover letter using Mistral AI.

    Args:
        job: JobItem object with job details
        profile: UserProfile object with user information

    Returns:
        Generated cover letter text
    """
    system_prompt = """You are a concise, professional cover letter writer specializing in internship applications.
Your cover letters should be:
- Professional but enthusiastic
- 3-4 paragraphs maximum
- Specific to the role and company
- Highlight relevant skills and experience
- Show genuine interest in the company/role
- Use proper business letter format

Focus on how the candidate's skills align with the job requirements and what they can contribute to the team."""

    # Build job description
    job_text = f"""Position: {job.title}
Company: {job.company}
Location: {job.location or 'Not specified'}
Description: {job.desc}"""

    # Build profile summary
    profile_text = f"""Name: {profile.name or 'Candidate'}
Skills: {', '.join(profile.skills) if profile.skills else 'Various technical skills'}
LinkedIn: {profile.linkedin_url or 'Available upon request'}
Email: {profile.email or 'Available upon request'}"""

    user_prompt = f"""JOB:
{job_text}

PROFILE:
{profile_text}

Write a compelling 1-page cover letter that connects the candidate's background to this specific opportunity.
Make it personal, professional, and demonstrate clear value proposition for the hiring manager."""

    try:
        response = mistral.chat.complete(
            model="mistral-medium-2508",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=800,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"Error generating cover letter: {e}")
        # Fallback to template-based response
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job.title} position at {job.company}. With my background in {', '.join(profile.skills[:3]) if profile.skills else 'technology'}, I am excited about the opportunity to contribute to your team.

I am particularly drawn to {job.company} because of your innovative approach and commitment to excellence. My experience with {', '.join(profile.skills[:2]) if profile.skills else 'various technologies'} aligns well with the requirements for this role.

I am eager to discuss how my skills and enthusiasm can contribute to your organization's continued success.

Best regards,
{profile.name or 'Candidate'}"""


async def interview_coach(role: str, company: str, skills: list[str]) -> dict:
    """
    Generate interview coaching questions and tips using Mistral AI.

    Args:
        role: Job role/title
        company: Company name
        skills: List of candidate skills

    Returns:
        Dictionary with questions and tips
    """
    system_prompt = """Return JSON {questions:[{q,ideal_answer}], tips:[...]}

You are a practical interview coach specializing in tech internships and entry-level positions.
Your coaching should be:
- Specific to the role and company
- Practical and actionable
- Focused on common internship interview scenarios
- Include both technical and behavioral aspects

Format questions as: {"q": "question text", "ideal_answer": "brief guidance"}
Provide exactly 5 targeted interview questions and 3 improvement tips.
Return only valid JSON, no additional text."""

    skills_text = ", ".join(skills) if skills else "various technical skills"

    user_prompt = f"""ROLE: {role}
COMPANY: {company}
SKILLS: {skills_text}

Generate interview coaching for this specific role and company combination."""

    try:
        response = mistral.chat.complete(
            model="mistral-medium-2508",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1200,
            temperature=0.6,
        )

        content = response.choices[0].message.content.strip()

        # Try to parse JSON response
        try:
            # Clean the response to extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]

            # Remove any leading/trailing non-JSON text
            content = content.strip()
            if content.startswith("{"):
                result = json.loads(content)

                # Ensure proper format
                questions = []
                if "questions" in result:
                    for q in result["questions"]:
                        if isinstance(q, dict) and "q" in q:
                            questions.append(
                                {
                                    "q": q["q"],
                                    "ideal_answer": q.get(
                                        "ideal_answer",
                                        "Provide a specific example from your experience.",
                                    ),
                                }
                            )
                        elif isinstance(q, str):
                            questions.append(
                                {
                                    "q": q,
                                    "ideal_answer": "Provide a specific example from your experience.",
                                }
                            )

                tips = result.get("tips", [])
                if isinstance(tips, list):
                    tips = [str(tip) for tip in tips if tip]

                return {
                    "questions": questions[:5],  # Ensure max 5 questions
                    "tips": tips[:3],  # Ensure max 3 tips
                }
        except json.JSONDecodeError:
            # If JSON parsing fails, try repair prompt
            repair_prompt = f"""Fix this JSON response for interview coaching:

{content}

Return valid JSON with format: {{"questions":[{{"q":"question","ideal_answer":"guidance"}}],"tips":["tip1","tip2"]}}"""

            try:
                repair_response = mistral.chat.complete(
                    model="mistral-medium-2508",
                    messages=[{"role": "user", "content": repair_prompt}],
                    max_tokens=800,
                    temperature=0.3,
                )

                repair_content = repair_response.choices[0].message.content.strip()
                if "```json" in repair_content:
                    repair_content = repair_content.split("```json")[1].split("```")[0]
                elif "```" in repair_content:
                    repair_content = repair_content.split("```")[1].split("```")[0]

                repair_content = repair_content.strip()
                if repair_content.startswith("{"):
                    result = json.loads(repair_content)
                    return {
                        "questions": result.get("questions", [])[:5],
                        "tips": result.get("tips", [])[:3],
                    }
            except Exception:
                pass

        # Fallback to text parsing
        return _parse_coaching_response(content)

    except Exception as e:
        print(f"Error generating interview coaching: {e}")
        # Fallback to template-based response
        return {
            "questions": [
                {
                    "q": f"Tell me about your experience with {role} and what interests you most about this field.",
                    "ideal_answer": "Focus on specific projects, technologies, or experiences that demonstrate your passion and relevant skills.",
                },
                {
                    "q": f"What do you know about {company} and why do you want to work here?",
                    "ideal_answer": "Research their products, mission, recent news, and company culture. Show genuine interest and alignment with their values.",
                },
                {
                    "q": "Describe a challenging project you've worked on and how you overcame obstacles.",
                    "ideal_answer": "Use the STAR method: describe the Situation, Task, Action you took, and Result achieved. Show problem-solving skills.",
                },
                {
                    "q": f"Where do you see yourself in 5 years, and how does this {role} role fit into your career goals?",
                    "ideal_answer": "Show long-term thinking while demonstrating how this role is a stepping stone toward your career aspirations.",
                },
                {
                    "q": "Do you have any questions about the role or company culture?",
                    "ideal_answer": "Ask thoughtful questions about team dynamics, growth opportunities, or specific projects you'd work on.",
                },
            ],
            "tips": [
                f"Research {company} thoroughly - understand their products, mission, and recent news.",
                "Prepare specific examples of your work using the STAR method (Situation, Task, Action, Result).",
                "Practice explaining technical concepts in simple terms for non-technical interviewers.",
            ],
        }


def _parse_coaching_response(content: str) -> dict:
    """
    Parse the LLM response to extract questions and tips.

    Args:
        content: Raw LLM response text

    Returns:
        Dictionary with questions and tips lists
    """
    try:
        # Try to parse as JSON first
        if content.strip().startswith("{"):
            return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Fallback to text parsing
    questions = []
    tips = []

    # Split content into sections
    sections = re.split(r"\n\n+", content)

    current_section = "questions"

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Look for section headers
        if any(
            keyword in section.lower()
            for keyword in ["tip", "advice", "improvement", "recommendation"]
        ):
            current_section = "tips"
        elif any(
            keyword in section.lower() for keyword in ["question", "ask", "interview"]
        ):
            current_section = "questions"

        # Extract numbered or bulleted items
        lines = section.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Remove numbering/bullets
            line = re.sub(r"^[\d\.\-\*\•]\s*", "", line)

            if len(line) > 10:  # Filter out very short lines
                if current_section == "questions" and len(questions) < 5:
                    questions.append(line)
                elif current_section == "tips" and len(tips) < 3:
                    tips.append(line)

    # Ensure we have at least some content
    if not questions:
        questions = [
            "Tell me about your relevant experience.",
            "What interests you about this role?",
            "How do you handle challenges?",
            "What are your career goals?",
            "Do you have any questions for us?",
        ]

    if not tips:
        tips = [
            "Research the company thoroughly before the interview.",
            "Prepare specific examples of your achievements.",
            "Practice explaining your experience clearly.",
        ]

    return {
        "questions": questions[:5],  # Ensure max 5 questions
        "tips": tips[:3],  # Ensure max 3 tips
    }


async def extract_skills_from_text(text: str) -> list[str]:
    """
    Extract skills from resume/LinkedIn text using Mistral AI.

    Args:
        text: Resume or LinkedIn profile text

    Returns:
        List of extracted skills
    """
    system_prompt = """You are a resume analyzer specializing in extracting technical and soft skills from candidate profiles.
Extract only the most relevant and specific skills mentioned in the text.
Return them as a clean list without explanations or formatting."""

    user_prompt = f"""Analyze this text and extract all relevant skills (technical, programming languages, frameworks, tools, soft skills, etc.):

{text[:2000]}  # Limit text length

Return only a simple list of skills, one per line, without numbering or bullet points."""

    try:
        response = mistral.chat.complete(
            model="mistral-medium-2508",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=300,
            temperature=0.3,
        )

        content = response.choices[0].message.content.strip()

        # Parse skills from response
        skills = []
        for line in content.split("\n"):
            line = line.strip()
            # Remove common prefixes and clean up
            line = re.sub(r"^[\d\.\-\*\•]\s*", "", line)
            if line and len(line) > 2 and len(line) < 50:
                skills.append(line.title())

        return list(set(skills))  # Remove duplicates

    except Exception as e:
        print(f"Error extracting skills: {e}")
        # Fallback to keyword-based extraction
        return _extract_skills_fallback(text)


def _extract_skills_fallback(text: str) -> list[str]:
    """
    Fallback keyword-based skill extraction.

    Args:
        text: Input text

    Returns:
        List of extracted skills
    """
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
        "leadership",
        "teamwork",
        "communication",
        "problem solving",
        "project management",
    ]

    found_skills = []
    text_lower = text.lower()

    for skill in skill_keywords:
        if skill.lower() in text_lower:
            found_skills.append(skill.title())

    return list(set(found_skills))
