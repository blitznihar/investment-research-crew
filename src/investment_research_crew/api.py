"""
investment_research_crew.api
API endpoints for Investment Research Crew.
Endpoints:
- GET /health: Health check endpoint.
- POST /content/run: Run content crew for a given topic.
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from investment_research_crew.crews.content_crews import ContentCrew
from investment_research_crew.config import load_settings

app = FastAPI(title="Investment Research Crew API", version="0.1.0")


class CrewRequest(BaseModel):
    """
    Request model for running the content crew.
    """

    topic: str = Field(..., min_length=3)


@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    settings = load_settings()
    return {
        "status": "ok",
        "llm_provider": settings.llm_provider,
        "docker_ai_url": settings.docker_ai_url,
        "docker_ai_model": settings.docker_ai_model,
        "docker_key_present": bool(settings.docker_ai_key),
    }


@app.post("/content/run")
def run_content(req: CrewRequest):
    """
    Run the content crew for the given topic."""
    crew = ContentCrew().crew
    result = crew.kickoff(inputs={"topic": req.topic})
    return {"topic": req.topic, "result": str(result)}
