"""
Crew for content planning, writing, and editing.
"""
# pylint: disable=too-few-public-methods

from crewai import Crew

from investment_research_crew.agents.crewsupport_agents import CrewSupportAgents
from investment_research_crew.tasks.crewsupport_tasks import CrewSupportTasks


class CrewSupportCrew:
    """
    Crew that includes content planning, writing, and editing agents.
    """

    def __init__(self) -> None:
        self.crewsupport_agents = CrewSupportAgents()
        self.crewsupport_tasks = CrewSupportTasks()
        self.crew = Crew(
            name="Crew Support Agent Crew",
            agents=[
                self.crewsupport_agents.support_agent,
                self.crewsupport_agents.support_quality_assurance_agent,
            ],
            tasks=[
                self.crewsupport_tasks.inquiry_resolution,
                self.crewsupport_tasks.quality_assurance_review,
            ],
            verbose=True,
            memory=True,
        )
