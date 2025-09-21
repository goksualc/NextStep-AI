"""
FastAPI application for InternAI backend services.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agents_registry import AGENTS, ensure_agents_registered
from app.coral_client import CoralClient
from app.routes import router
from app.settings import settings

# Initialize FastAPI app
app = FastAPI(
    title="InternAI API",
    description="AI-powered internship matching and application assistance platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Response models
class HealthResponse(BaseModel):
    ok: bool
    status: str = "healthy"


class APIInfo(BaseModel):
    name: str
    version: str
    description: str


# Include API routes under /v1 prefix
app.include_router(router, prefix="/v1", tags=["api"])


# Startup event
@app.on_event("startup")
async def _startup():
    """Initialize Coral client and register agents on startup."""
    if settings.CORAL_SERVER_URL and settings.CORAL_API_KEY:
        coral = CoralClient(settings.CORAL_SERVER_URL, settings.CORAL_API_KEY)
        await ensure_agents_registered(coral)


# Root routes
@app.get("/", response_model=APIInfo)
async def root():
    """Root endpoint with API information."""
    return APIInfo(
        name="InternAI API",
        version="1.0.0",
        description="AI-powered internship matching and application assistance platform",
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(ok=True, status="healthy")


@app.get("/api/info")
async def api_info():
    """API information endpoint."""
    return {
        "api_version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "features": ["cv_analyzer", "job_scout", "matcher", "app_writer", "coach"],
        "coral_status": (
            "configured"
            if settings.CORAL_SERVER_URL and settings.CORAL_API_KEY
            else "disconnected"
        ),
    }


@app.get("/v1/agents")
async def list_agents():
    """
    List all registered agents from cache file.

    Returns:
        List of agent metadata with key, name, and id
    """
    import json
    import os

    try:
        cache_file = ".coral_agents.json"
        if not os.path.exists(cache_file):
            return {
                "agents": [],
                "status": "no_cache",
                "message": "No agents registered yet",
            }

        with open(cache_file) as f:
            cached_data = json.load(f)
            agent_ids = cached_data.get("agent_ids", {})

        # Build condensed agent list
        agents = []
        for agent in AGENTS:
            agent_key = agent["key"]
            agent_id = agent_ids.get(agent_key, "")
            agents.append(
                {
                    "key": agent_key,
                    "name": agent["name"],
                    "id": agent_id,
                }
            )

        return {
            "agents": agents,
            "status": "cached",
            "count": len(agents),
        }

    except Exception as e:
        return {
            "error": f"Failed to load agents: {str(e)}",
            "agents": [],
            "status": "error",
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
