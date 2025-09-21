"""
Agent registry for InternAI agents.
"""

import json
import os
from typing import Dict, List, Any
from .coral_client import CoralClient


# Agent metadata definitions
AGENT_METADATA = {
    "cv_analyzer": {
        "name": "cv_analyzer",
        "description": "Analyzes CVs and resumes to extract structured information including skills, experience, and qualifications",
        "endpoint": "/v1/analyze",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Full name of the user"},
                "email": {"type": "string", "description": "Email address"},
                "linkedin_url": {"type": "string", "description": "LinkedIn profile URL"},
                "resume_url": {"type": "string", "description": "URL to resume/CV file"},
                "skills": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of user skills"
                }
            },
            "required": []
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "skills": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Extracted skills from profile"
                }
            },
            "required": ["skills"]
        },
        "pricing": {
            "per_request": 0.01,
            "currency": "USD"
        }
    },
    
    "job_scout": {
        "name": "job_scout",
        "description": "Discovers and scouts job opportunities from various sources including LinkedIn, Indeed, and company websites",
        "endpoint": "/v1/scout",
        "input_schema": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Search keywords for job discovery"
                },
                "location": {"type": "string", "description": "Preferred job location"},
                "job_type": {"type": "string", "description": "Type of job (internship, full-time, etc.)"},
                "limit": {"type": "integer", "description": "Maximum number of results"}
            },
            "required": ["keywords"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "jobs": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "title": {"type": "string"},
                            "company": {"type": "string"},
                            "location": {"type": "string"},
                            "url": {"type": "string"}
                        }
                    }
                }
            },
            "required": ["jobs"]
        },
        "pricing": {
            "per_request": 0.02,
            "currency": "USD"
        }
    },
    
    "matcher": {
        "name": "matcher",
        "description": "Matches user profiles with job opportunities using AI-powered algorithms to calculate compatibility scores",
        "endpoint": "/v1/match",
        "input_schema": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "linkedin_url": {"type": "string"},
                        "resume_url": {"type": "string"},
                        "skills": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                },
                "jobs": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "source": {"type": "string"},
                            "title": {"type": "string"},
                            "company": {"type": "string"},
                            "location": {"type": "string"},
                            "url": {"type": "string"},
                            "desc": {"type": "string"}
                        }
                    }
                }
            },
            "required": ["profile", "jobs"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "matches": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "job": {"type": "object"},
                            "score": {"type": "number", "minimum": 0, "maximum": 100},
                            "missing_skills": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            },
            "required": ["matches"]
        },
        "pricing": {
            "per_request": 0.03,
            "currency": "USD"
        }
    },
    
    "app_writer": {
        "name": "app_writer",
        "description": "Generates personalized cover letters and application materials tailored to specific job opportunities",
        "endpoint": "/v1/write",
        "input_schema": {
            "type": "object",
            "properties": {
                "job": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "source": {"type": "string"},
                        "title": {"type": "string"},
                        "company": {"type": "string"},
                        "location": {"type": "string"},
                        "url": {"type": "string"},
                        "desc": {"type": "string"}
                    }
                },
                "profile": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "linkedin_url": {"type": "string"},
                        "resume_url": {"type": "string"},
                        "skills": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            },
            "required": ["job", "profile"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "cover_letter": {
                    "type": "string",
                    "description": "Generated cover letter"
                }
            },
            "required": ["cover_letter"]
        },
        "pricing": {
            "per_request": 0.05,
            "currency": "USD"
        }
    },
    
    "coach": {
        "name": "coach",
        "description": "Provides personalized career coaching, interview preparation, and professional development guidance",
        "endpoint": "/v1/coach",
        "input_schema": {
            "type": "object",
            "properties": {
                "role": {"type": "string", "description": "Target role or position"},
                "company": {"type": "string", "description": "Target company (optional)"},
                "profile": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "linkedin_url": {"type": "string"},
                        "resume_url": {"type": "string"},
                        "skills": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            },
            "required": ["role"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Interview questions for the role"
                },
                "tips": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Career tips and advice"
                }
            },
            "required": ["questions", "tips"]
        },
        "pricing": {
            "per_request": 0.04,
            "currency": "USD"
        }
    }
}


def ensure_agents_registered(coral: CoralClient) -> Dict[str, str]:
    """
    Ensure all agents are registered with Coral platform.
    
    Args:
        coral: CoralClient instance for registration
        
    Returns:
        Dict mapping agent names to their agent IDs
        
    Raises:
        Exception: If agent registration fails
    """
    cache_file = ".coral_agents.json"
    agent_ids = {}
    
    # Load existing agent IDs from cache
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                agent_ids = cached_data.get("agent_ids", {})
        except (json.JSONDecodeError, KeyError):
            # If cache is corrupted, start fresh
            agent_ids = {}
    
    # Register each agent if not already cached
    for agent_name, metadata in AGENT_METADATA.items():
        if agent_name not in agent_ids:
            try:
                # Create combined schema for input/output
                combined_schema = {
                    "input": metadata["input_schema"],
                    "output": metadata["output_schema"]
                }
                
                result = coral.register_agent(
                    name=metadata["name"],
                    description=metadata["description"],
                    schema=combined_schema,
                    endpoint=metadata["endpoint"],
                    pricing=metadata.get("pricing")
                )
                
                agent_ids[agent_name] = result["agent_id"]
                print(f"Registered agent '{agent_name}' with ID: {result['agent_id']}")
                
            except Exception as e:
                print(f"Failed to register agent '{agent_name}': {e}")
                # Continue with other agents even if one fails
                continue
    
    # Save agent IDs to cache
    try:
        with open(cache_file, 'w') as f:
            json.dump({"agent_ids": agent_ids}, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save agent cache: {e}")
    
    return agent_ids


def get_agent_metadata(agent_name: str) -> Dict[str, Any]:
    """
    Get metadata for a specific agent.
    
    Args:
        agent_name: Name of the agent
        
    Returns:
        Agent metadata dictionary
        
    Raises:
        KeyError: If agent name is not found
    """
    if agent_name not in AGENT_METADATA:
        raise KeyError(f"Unknown agent: {agent_name}")
    
    return AGENT_METADATA[agent_name]


def list_agent_names() -> List[str]:
    """
    Get list of all registered agent names.
    
    Returns:
        List of agent names
    """
    return list(AGENT_METADATA.keys())
