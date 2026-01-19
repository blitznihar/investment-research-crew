"""
investment_research_crew.api
API endpoints for Investment Research Crew.
Endpoints:
- GET /health: Health check endpoint.
- POST /content/run: Run content crew for a given topic.
"""

from fastapi import FastAPI

from investment_research_crew.crews.content_crews import ContentCrew
from investment_research_crew.config import load_settings
from investment_research_crew.crews.crewsupport_crews import CrewSupportCrew
from investment_research_crew.models.content_request import ContentRequest
from investment_research_crew.models.crewsupport_request import CrewSupportRequest

app = FastAPI(title="Investment Research Crew API", version="0.1.0")


@app.get("/health")
def health():
    """
    Health check endpoint.
    """
    settings = load_settings()
    return {
        "status": "ok",
        "llm_provider": settings.llm_provider,
        "ai_url": settings.url_in_use,
        "ai_model": settings.model_in_use,
        "key_present": bool(settings.key_in_use),
    }


@app.post("/content/run")
def run_content(req: ContentRequest):
    """
    Run the content crew for the given topic."""

    try:
        crew = ContentCrew().crew
        result = crew.kickoff(inputs={"topic": req.topic})
        return {"topic": req.topic, "result": str(result)}
    except Exception as e:  # pylint: disable=broad-exception-caught
        return {"error": str(e)}


@app.post("/support/run")
def run_crew_support(req: CrewSupportRequest):
    """
    Run the crew support crew for the given inquiry."""
    try:
        crew = CrewSupportCrew().crew
        result = crew.kickoff(
            inputs={
                "customer": req.customer,
                "person": req.person,
                "inquiry": req.inquiry,
            }
        )
        return {"inquiry": req.inquiry, "result": str(result)}
    except Exception as e:  # pylint: disable=broad-exception-caught
        return {"error": str(e)}
