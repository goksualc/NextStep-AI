"""
CV Parser module for extracting skills and highlights from resume text.
"""

import json
import re
import unicodedata

from .llm import mistral


def normalize_text(text: str) -> str:
    """Normalize text by converting to lowercase and removing accents."""
    # Remove accents and convert to lowercase
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.lower().strip()


# Curated skill sets for regex matching
SKILL_SETS = {
    "programming_languages": [
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
    ],
    "frameworks_libraries": [
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
    ],
    "databases": [
        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "elasticsearch",
        "sqlite",
        "cassandra",
        "dynamodb",
        "neo4j",
    ],
    "cloud_platforms": [
        "aws",
        "azure",
        "gcp",
        "google cloud",
        "amazon web services",
        "microsoft azure",
        "cloudflare",
    ],
    "devops_tools": [
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
    ],
    "ai_ml": [
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
    ],
    "blockchain": [
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
    ],
    "security": [
        "cybersecurity",
        "penetration testing",
        "vulnerability assessment",
        "security auditing",
        "cryptography",
        "network security",
    ],
    "devrel": [
        "developer relations",
        "technical writing",
        "community management",
        "developer advocacy",
        "content creation",
        "documentation",
    ],
    "data_engineering": [
        "data engineering",
        "etl",
        "data pipelines",
        "apache spark",
        "kafka",
        "airflow",
        "data warehousing",
        "big data",
    ],
}


def regex_scan_skills(text: str) -> list[str]:
    """Scan text for skills using regex patterns."""
    normalized_text = normalize_text(text)
    found_skills = []

    # Create a flat list of all skills
    all_skills = []
    for _category, skills in SKILL_SETS.items():
        all_skills.extend(skills)

    # Remove duplicates while preserving order
    unique_skills = list(dict.fromkeys(all_skills))

    # Scan for each skill
    for skill in unique_skills:
        # Create a regex pattern that matches word boundaries
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, normalized_text):
            found_skills.append(skill.title())

    return found_skills


async def llm_extract_skills(text: str) -> dict[str, list[str]]:
    """Extract skills using Mistral LLM."""
    system_prompt = """Extract skill keywords only, return JSON {skills:[], highlights:[]}

Focus on:
- Technical skills (programming languages, frameworks, tools)
- Soft skills (leadership, communication, teamwork)
- Domain expertise (AI/ML, security, blockchain, etc.)
- Certifications and achievements

Return only the JSON object, no additional text."""

    user_prompt = (
        f"Analyze this resume text and extract skills and highlights:\n\n{text[:2000]}"
    )

    try:
        response = mistral.chat.complete(
            model="mistral-medium-2508",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=500,
            temperature=0.3,
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
                return {
                    "skills": result.get("skills", []),
                    "highlights": result.get("highlights", []),
                }
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract skills from text
            lines = content.split("\n")
            skills = []
            highlights = []

            for line in lines:
                line = line.strip()
                if line and len(line) < 100:  # Reasonable skill length
                    if any(
                        keyword in line.lower()
                        for keyword in ["skill", "experience", "proficient"]
                    ):
                        skills.append(line)
                    else:
                        highlights.append(line)

            return {"skills": skills, "highlights": highlights}

    except Exception as e:
        print(f"Error in LLM skill extraction: {e}")
        return {"skills": [], "highlights": []}

    return {"skills": [], "highlights": []}


def merge_and_dedupe_skills(
    regex_skills: list[str], llm_skills: list[str]
) -> list[str]:
    """Merge and deduplicate skills from regex and LLM extraction."""
    # Combine all skills
    all_skills = regex_skills + llm_skills

    # Normalize and deduplicate
    normalized_skills = {}
    for skill in all_skills:
        normalized = skill.strip().title()
        if normalized and len(normalized) > 1:
            normalized_skills[normalized] = skill

    return list(normalized_skills.keys())


async def analyze_profile(text: str) -> dict[str, any]:
    """
    Analyze profile text using both regex and LLM extraction.

    Args:
        text: Resume or profile text

    Returns:
        Dictionary with skills, highlights, and profile_text
    """
    if not text or not text.strip():
        return {"skills": [], "highlights": [], "profile_text": ""}

    # Normalize the input text
    normalize_text(text)

    # Extract skills using regex
    regex_skills = regex_scan_skills(text)

    # Extract skills using LLM
    llm_result = await llm_extract_skills(text)
    llm_skills = llm_result.get("skills", [])
    llm_highlights = llm_result.get("highlights", [])

    # Merge and deduplicate skills
    merged_skills = merge_and_dedupe_skills(regex_skills, llm_skills)

    # Create profile text summary
    profile_text = f"Skills: {', '.join(merged_skills[:10])}"
    if llm_highlights:
        profile_text += f" | Highlights: {'; '.join(llm_highlights[:3])}"

    return {
        "skills": merged_skills,
        "highlights": llm_highlights,
        "profile_text": profile_text,
    }
