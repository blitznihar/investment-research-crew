"""
Crew for content planning, writing, and editing.
"""
# pylint: disable=too-few-public-methods

from crewai import Crew

from investment_research_crew.agents.content_agents import ContentAgents
from investment_research_crew.tasks.content_tasks import ContentTasks


class ContentCrew:
    """
    Crew that includes content planning, writing, and editing agents.
    """

    def __init__(self) -> None:
        """
        Docstring for __init__

        :param self: Description
        """
        self.content_agents = ContentAgents()
        self.content_tasks = ContentTasks()
        self.crew = Crew(
            name="Investment Research Content Crew",
            agents=[
                self.content_agents.planner,
                self.content_agents.writer,
                self.content_agents.editor,
            ],
            tasks=[
                self.content_tasks.plan,
                self.content_tasks.write,
                self.content_tasks.edit,
            ],
            verbose=True,
        )
