"""
Docstring for crew_agents
"""

from crewai import Agent, Task, Crew, Process
from investment_research_crew.config import load_settings
from investment_research_crew.llm.llm import Llm

settings = load_settings()

llm = Llm().llm


def run_research(topic: str) -> str:
    """
    Docstring for run_research

    :param topic: Description
    :type topic: str
    :return: Description
    :rtype: str
    """
    researcher = Agent(
        role="Researcher",
        goal="Produce concise factual bullets and key points.",
        backstory="You extract the essentials and avoid fluff.",
        llm=llm,
        verbose=True,
    )

    t = Task(
        description=f"Give 6-10 bullet points about: {topic}. Keep it factual and short.",
        expected_output="Bulleted list of key points.",
        agent=researcher,
    )

    crew = Crew(agents=[researcher], tasks=[t], process=Process.sequential)
    out = crew.kickoff()
    return str(out)


def run_write(summary_bullets: str) -> str:
    """
    Docstring for run_write

    :param summary_bullets: Description
    :type summary_bullets: str
    :return: Description
    :rtype: str
    """
    writer = Agent(
        role="Writer",
        goal="Turn bullets into a short, polished paragraph.",
        backstory="You write crisp and structured.",
        llm=llm,
        verbose=True,
    )

    t = Task(
        description=(
            "Convert the following bullets into a short 1-paragraph explanation. "
            "Keep it clear and readable.\n\n"
            f"Bullets:\n{summary_bullets}"
        ),
        expected_output="One paragraph, 5-8 sentences.",
        agent=writer,
    )

    crew = Crew(agents=[writer], tasks=[t], process=Process.sequential)
    out = crew.kickoff()
    return str(out)
