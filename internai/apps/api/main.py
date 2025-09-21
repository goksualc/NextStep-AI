"""
FastAPI application for InternAI backend services.
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agents_registry import ensure_agents_registered
from app.coral_client import CoralClient
from app.routes import router

# Load environment variables
load_dotenv()

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
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Alternative port
    ],
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


# Global Coral client instance
coral_client = None


# Include API routes under /v1 prefix
app.include_router(router, prefix="/v1", tags=["api"])


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize Coral client and register agents on startup."""
    global coral_client

    try:
        # Initialize Coral client
        coral_client = CoralClient()
        print(f"Connected to Coral server: {coral_client.server_url}")

        # Register all agents
        agent_ids = ensure_agents_registered(coral_client)
        print(f"Registered {len(agent_ids)} agents with Coral")

    except ValueError as e:
        print(f"Warning: Coral client initialization failed: {e}")
        print("Continuing without Coral integration...")
        coral_client = None
    except Exception as e:
        print(f"Warning: Agent registration failed: {e}")
        print("Continuing without agent registration...")


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
        "environment": os.getenv("ENVIRONMENT", "development"),
        "features": ["cv_analyzer", "job_scout", "matcher", "app_writer", "coach"],
        "coral_status": "connected" if coral_client else "disconnected",
    }


@app.get("/v1/agents")
async def list_agents():
    """
    List all registered agents.

    Returns:
        List of agent metadata and status
    """
    if not coral_client:
        return {
            "error": "Coral client not initialized",
            "agents": [],
            "status": "disconnected",
        }

    try:
        agents = coral_client.list_agents()
        return {"agents": agents, "status": "connected", "count": len(agents)}
    except Exception as e:
        return {
            "error": f"Failed to list agents: {str(e)}",
            "agents": [],
            "status": "error",
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
