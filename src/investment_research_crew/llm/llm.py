"""
LLM module for Investment Research Crew.
"""
# pylint: disable=too-few-public-methods

from crewai.llm import LLM
from investment_research_crew.config import load_settings


settings = load_settings()


class Llm:
    """
    Docstring for Llm
    """

    def __init__(self) -> None:
        self.llm = LLM(
            model=settings.model_in_use,
            base_url=settings.url_in_use,
            api_key=settings.key_in_use,
        )
