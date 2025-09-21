"""
Agent registry for InternAI agents.
"""

import json
import os
from typing import Any

from .coral_client import CoralClient

# Simplified agent definitions
AGENTS = [
    {
        "key": "cv_analyzer",
        "name": "CV Analyzer",
        "description": "Extracts skills & highlights from resume/LinkedIn.",
        "schema": {
            "input": {
                "type": "object",
                "properties": {"text": {"type": "string"}},
                "required": ["text"],
            },
            "output": {
                "type": "object",
                "properties": {
                    "skills": {"type": "array", "items": {"type": "string"}}
                },
            },
        },
        "endpoint": "/v1/local/cv_analyzer",
    },
    {
        "key": "job_scout",
        "name": "Job Scout",
        "description": "Returns curated internship listings.",
        "schema": {
            "input": {"type": "object", "properties": {"filters": {"type": "object"}}},
            "output": {"type": "object", "properties": {"jobs": {"type": "array"}}},
        },
        "endpoint": "/v1/local/job_scout",
    },
    {
        "key": "matcher",
        "name": "Matcher",
        "description": "Embeddings-based job matching.",
        "schema": {
            "input": {
                "type": "object",
                "properties": {
                    "profile": {"type": "object"},
                    "jobs": {"type": "array"},
                },
                "required": ["profile", "jobs"],
            },
            "output": {"type": "object", "properties": {"matches": {"type": "array"}}},
        },
        "endpoint": "/v1/local/matcher",
    },
    {
        "key": "app_writer",
        "name": "Application Writer",
        "description": "Role/company-specific cover letter drafting.",
        "schema": {
            "input": {
                "type": "object",
                "properties": {
                    "job": {"type": "object"},
                    "profile": {"type": "object"},
                },
                "required": ["job", "profile"],
            },
            "output": {
                "type": "object",
                "properties": {"cover_letter": {"type": "string"}},
            },
        },
        "endpoint": "/v1/local/app_writer",
    },
    {
        "key": "coach",
        "name": "Interview Coach",
        "description": "Q&A + tips for interviews.",
        "schema": {
            "input": {
                "type": "object",
                "properties": {
                    "role": {"type": "string"},
                    "company": {"type": "string"},
                },
                "required": ["role"],
            },
            "output": {
                "type": "object",
                "properties": {
                    "questions": {"type": "array"},
                    "tips": {"type": "array"},
                },
            },
        },
        "endpoint": "/v1/local/coach",
    },
]


async def ensure_agents_registered(coral: CoralClient) -> dict[str, str]:
    """
    Ensure all agents are registered with Coral platform.

    Fetches list_agents(), checks by name, if missing calls register_agent()
    and persists {key: agent_id} to .coral_agents.json

    Args:
        coral: CoralClient instance for registration

    Returns:
        Dict mapping agent keys to their agent IDs

    Raises:
        Exception: If agent registration fails
    """
    cache_file = ".coral_agents.json"
    agent_ids = {}

    # Load existing agent IDs from cache
    if os.path.exists(cache_file):
        try:
            with open(cache_file) as f:
                cached_data = json.load(f)
                agent_ids = cached_data.get("agent_ids", {})
        except (json.JSONDecodeError, KeyError):
            # If cache is corrupted, start fresh
            agent_ids = {}

    try:
        # Fetch existing agents from Coral
        existing_agents = await coral.list_agents()
        existing_agent_names = {agent.get("name") for agent in existing_agents}
    except Exception as e:
        print(f"Warning: Could not fetch existing agents from Coral: {e}")
        existing_agent_names = set()

    # Register each agent if not already registered
    for agent in AGENTS:
        agent_key = agent["key"]
        agent_name = agent["name"]

        # Check if agent is already cached
        if agent_key in agent_ids:
            print(f"Agent '{agent_key}' already cached with ID: {agent_ids[agent_key]}")
            continue

        # Check if agent exists on Coral server by name
        if agent_name in existing_agent_names:
            print(f"Agent '{agent_name}' already exists on Coral server")
            # Find the agent_id from existing agents
            for existing_agent in existing_agents:
                if existing_agent.get("name") == agent_name:
                    agent_ids[agent_key] = existing_agent.get("agent_id", "")
                    break
            continue

        # Register new agent
        try:
            result = await coral.register_agent(
                name=agent["name"],
                description=agent["description"],
                schema=agent["schema"],
                endpoint=agent["endpoint"],
                pricing=None,  # No pricing for local agents
            )

            agent_ids[agent_key] = result["agent_id"]
            print(
                f"Registered agent '{agent_key}' ({agent_name}) with ID: {result['agent_id']}"
            )

        except Exception as e:
            print(f"Failed to register agent '{agent_key}': {e}")
            # Continue with other agents even if one fails
            continue

    # Save agent IDs to cache
    try:
        with open(cache_file, "w") as f:
            json.dump({"agent_ids": agent_ids}, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save agent cache: {e}")

    return agent_ids


def get_agent_metadata(agent_key: str) -> dict[str, Any]:
    """
    Get metadata for a specific agent.

    Args:
        agent_key: Key of the agent

    Returns:
        Agent metadata dictionary

    Raises:
        KeyError: If agent key is not found
    """
    for agent in AGENTS:
        if agent["key"] == agent_key:
            return agent

    raise KeyError(f"Unknown agent: {agent_key}")


def list_agent_names() -> list[str]:
    """
    Get list of all registered agent keys.

    Returns:
        List of agent keys
    """
    return [agent["key"] for agent in AGENTS]


def list_agent_display_names() -> list[str]:
    """
    Get list of all registered agent display names.

    Returns:
        List of agent display names
    """
    return [agent["name"] for agent in AGENTS]
