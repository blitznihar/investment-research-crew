"""
Request model for running the content crew.
"""

from pydantic import BaseModel, Field


class ContentRequest(BaseModel):
    """
    Request model for running the content crew.
    """

    topic: str = Field(..., min_length=3)
