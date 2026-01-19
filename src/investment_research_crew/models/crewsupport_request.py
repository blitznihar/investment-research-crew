"""
Request model for running the crew support crew.
"""

from pydantic import BaseModel, Field


class CrewSupportRequest(BaseModel):
    """
    Request model for running the crew support crew.
    """

    customer: str = Field(..., min_length=5)
    person: str = Field(..., min_length=5)
    inquiry: str = Field(..., min_length=10)
