"""
Docstring for src.investment_research_crew.main
"""

from investment_research_crew.config import load_settings
from investment_research_crew.crews.content_crew import content_crew


def run() -> None:
    print("✅ investment-research-crew is running!")

    settings = load_settings()  # <-- create instance

    # Print a safe subset (don’t print full keys)
    print(f"LLM Provider: {settings.llm_provider}")
    print(f"Docker URL: {settings.docker_ai_url}")
    print(f"Docker Model: {settings.docker_ai_model}")

    # If you want to show key presence (without leaking it)
    print(f"Docker Key Present: {bool(settings.docker_ai_key.strip())}")
    crew = content_crew().crew
    result = crew.kickoff(inputs={"topic": "Artificial Intelligence"})
    print(result)


if __name__ == "__main__":
    run()
