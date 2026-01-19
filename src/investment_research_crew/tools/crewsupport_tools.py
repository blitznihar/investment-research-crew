"""Returns Tools
for crew support.
"""
# pylint: disable=too-few-public-methods

from crewai_tools import ScrapeWebsiteTool


class CrewSupportTools:
    """
    Defines tools required for crew support.
    """

    def __init__(self) -> None:
        self.docs_scrape_tool = ScrapeWebsiteTool(
            website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
        )
