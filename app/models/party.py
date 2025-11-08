"""
Party data model based on existing JSON structure
"""

from pydantic import BaseModel, Field


class Party(BaseModel):
    """Party model matching existing JSON structure"""

    id: str = Field(alias="id")
    name: str = Field(alias="name")
    short_name: str = Field(alias="short_name")
    symbol: str = Field(alias="symbol")

    class Config:
        allow_population_by_field_name = True
