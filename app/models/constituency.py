"""
Constituency data model based on existing JSON structure
"""

from pydantic import BaseModel, Field


class Constituency(BaseModel):
    """Constituency model matching existing JSON structure"""

    id: str = Field(alias="id")
    name: str = Field(alias="name")
    state_id: str = Field(alias="state_id")
