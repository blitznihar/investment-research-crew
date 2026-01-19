"""
Defines agents for content planning, writing, and editing.
"""
# pylint: disable=too-few-public-methods

from crewai import Agent
from investment_research_crew.llm.llm import Llm


class CrewSupportAgents:
    """
    Defines agents for crew support.
    """

    def __init__(self) -> None:
        """
        Docstring for __init__

        :param self: Constructor reference
        :type self: CrewSupportAgents
        :return: None
        :rtype: None
        """
        self.llm = Llm().llm
        self.support_agent = Agent(
            role="Senior Support Representative",
            goal="Be the most friendly and helpful support representative in your team",
            backstory=(
                "You work at crewAI (https://crewai.com) and "
                " are now working on providing "
                "support to {customer}, a super important customer "
                " for your company."
                "You need to make sure that you provide the best support!"
                "Make sure to provide full complete answers, "
                " and make no assumptions."
                "Do not exceed 150 words in your response."
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.llm,
        )

        self.support_quality_assurance_agent = Agent(
            role="Support Quality Assurance Specialist",
            goal="Get recognition for providing the best support quality assurance in your team",
            backstory=(
                "You work at crewAI (https://crewai.com) and "
                "are now working with your team "
                "on a request from {customer} ensuring that "
                "the support representative is "
                "providing the best support possible.\n"
                "You need to make sure that the support representative "
                "is providing full "
                "complete answers, and make no assumptions."
                "Do not exceed 150 words in your response."
            ),
            verbose=True,
            llm=self.llm,
        )
