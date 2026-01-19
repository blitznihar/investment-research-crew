"""
Docstring for src.investment_research_crew.main
"""

import uvicorn

from investment_research_crew.config import load_settings


def run() -> None:
    """
    CLI entrypoint: Start FastAPI server.
    `uv run investment-research-crew` will start the API.
    """
    settings = load_settings()

    host = settings.host
    port = settings.port
    reload = settings.reload

    print("✅ Starting Investment Research Crew API...")
    print(f"LLM Provider: {settings.llm_provider}")
    print(f"Docker URL: {settings.docker_ai_url}")
    print(f"Docker Model: {settings.docker_ai_model}")
    print(f"API: http://{host}:{port}")

    uvicorn.run(
        "investment_research_crew.api:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    run()
