"""
investment_research_crew.api
API endpoints for Investment Research Crew.
Endpoints:
- GET /health: Health check endpoint.
- POST /content/run: Run content crew for a given topic.
"""

import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from investment_research_crew.crews.content_crews import ContentCrew
from investment_research_crew.config import load_settings
from investment_research_crew.crews.crewsupport_crews import CrewSupportCrew
from investment_research_crew.models.content_request import ContentRequest
from investment_research_crew.models.crewsupport_request import CrewSupportRequest
from investment_research_crew.crews.testcrew.queue_bus import publish, new_envelope
from investment_research_crew.crews.testcrew.checkpoint import get_state


class StartRequest(BaseModel):
    """
    Docstring for StartRequest
    """
    topic: str
    crash_test: bool = False


class StartResponse(BaseModel):
    """
    Docstring for StartResponse
    """
    run_id: str
    thread_id: str


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


@app.post("/resilientresearcher/startruns", response_model=StartResponse)
def start_run(req: StartRequest):
    """
    Docstring for start_run
    
    :param req: Description
    :type req: StartRequest
    """
    run_id = str(uuid.uuid4())
    thread_id = str(uuid.uuid4())

    msg = new_envelope(
        step="research",
        to="research",
        payload={"topic": req.topic, "crash_test": req.crash_test},
        thread_id=thread_id,
        run_id=run_id,
    )
    publish("task.research", msg)
    return StartResponse(run_id=run_id, thread_id=thread_id)


@app.get("/resilientresearcher/statusruns/{run_id}")
def get_run_status(run_id: str):
    """
    Docstring for get_run_status
    
    :param run_id: Description
    :type run_id: str
    """
    state = get_state(run_id)
    if not state:
        raise HTTPException(status_code=404, detail="run_id not found")
    return state
