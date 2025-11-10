"""
Candidate data models based on existing JSON structure
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CandidateStatus(str, Enum):
    WON = "WON"
    LOST = "LOST"


class CandidateType(str, Enum):
    MP = "MP"


class Candidate(BaseModel):
    """Lok Sabha candidate model"""

    id: str
    name: str
    party_id: str
    constituency_id: str
    state_id: str
    image_url: Optional[str] = None
    status: CandidateStatus
    type: CandidateType = CandidateType.MP
