"""
Crew for content planning, writing, and editing.
"""

from crewai import Crew
from investment_research_crew.agents.content_agents import content_agents
from investment_research_crew.tasks.plan_task import content_tasks


class ContentCrew:
    """
    Crew that includes content planning, writing, and editing agents.
    """

    crew = Crew(
        name="Investment Research Content Crew",
        agents=[
            content_agents().planner,
            content_agents().writer,
            content_agents().editor,
        ],
        tasks=[
            content_tasks().plan,
            content_tasks().write,
            content_tasks().edit,
        ],
        verbose=True,
    )


def content_crew() -> ContentCrew:
    """Creates and returns an instance of ContentCrew.

    Returns:
        ContentCrew: An instance of ContentCrew with
        content planning, writing, and editing capabilities.
    """
    return ContentCrew()
