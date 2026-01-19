"""
Defines agents for content planning, writing, and editing.
"""

from crewai import Agent, LLM
from investment_research_crew.config import load_settings


def get_local_llm() -> LLM:
    settings = load_settings()
    return LLM(
        model=settings.docker_ai_model,
        base_url=settings.docker_ai_url,
        api_key=settings.docker_ai_key,
    )


class ContentAgents:
    """
    Defines agents for content planning, writing, and editing.
    """

    planner = Agent(
        role="Content Planner",
        goal="Plan engaging and factually accurate content on {topic}",
        backstory=(
            "You're working on planning a blog article "
            "about the topic: {topic}."
            "You collect information that helps the "
            "audience learn something "
            "and make informed decisions. "
            "Your work is the basis for "
            "the Content Writer to write"
            "an article on this topic."
        ),
        allow_delegation=False,
        verbose=True,
        llm=get_local_llm(),
    )

    editor = Agent(
        role="Content Editor",
        goal="Edit a given blog post to align with the writing style of the organization.",
        backstory=(
            "You are an editor who receives a blog post "
            "from the Content Writer. "
            "Your goal is to review the blog post "
            "to ensure that it follows journalistic best practices,"
            "provides balanced viewpoints "
            "when providing opinions or assertions, "
            "and also avoids major controversial topics "
            "or opinions when possible."
        ),
        allow_delegation=False,
        verbose=True,
        llm=get_local_llm(),
    )

    writer = Agent(
        role="Content Writer",
        goal="Write engaging and factually accurate content on {topic}",
        backstory=(
            "You're working on a writing "
            "a new opinion piece about the topic: {topic}. "
            "You base your writing on the work of "
            "the Content Planner, who provides an outline "
            "and relevant context about the topic. "
            "You follow the main objectives and "
            "direction of the outline, "
            "as provide by the Content Planner. "
            "You also provide objective and impartial insights "
            "and back them up with information "
            "provide by the Content Planner. "
            "You acknowledge in your opinion piece "
            "when your statements are opinions "
            "as opposed to objective statements."
        ),
        allow_delegation=False,
        verbose=True,
        llm=get_local_llm(),
    )


def content_agents() -> ContentAgents:
    return ContentAgents()
