"""
Defines agents for content planning, writing, and editing.
"""
# pylint: disable=too-few-public-methods

from crewai import Agent, LLM
from investment_research_crew.config import load_settings


def get_local_llm() -> LLM:
    """
    Docstring for get_local_llm

    :return: Description
    :rtype: LLM
    """
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

    def __init__(self) -> None:
        """
        Docstring for __init__

        :param self: Constructor reference
        :type self: ContentAgents
        :return: None
        :rtype: None
        """
        self.llm = get_local_llm()
        self.planner = Agent(
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
            llm=self.llm,
        )

        self.editor = Agent(
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
            llm=self.llm,
        )

        self.writer = Agent(
            role="Content Writer",
            goal="Write short but engaging and factually accurate content on {topic}",
            backstory=(
                "You're working on writing "
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
                "you write in a clear, concise, and engaging manner."
                "Keeping content brief and to the point."
                "Keep the entire essay under 300 words."
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )
