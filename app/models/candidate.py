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
    MLA = "MLA"
    MP = "MP"


class Candidate(BaseModel):
    """Base candidate model"""

    id: Optional[str] = None
    name: str
    party_id: str
    constituency_id: str
    image_url: Optional[str] = None
    status: Optional[CandidateStatus] = None
    type: Optional[CandidateType] = None


class LokSabhaCandidate(Candidate):
    """Lok Sabha candidate model"""

    state_id: Optional[str] = None
    type: CandidateType = CandidateType.MP


class AssemblyCandidate(Candidate):
    """Assembly candidate model (Vidhan Sabha)"""

    state_id: Optional[str] = None
    type: CandidateType = CandidateType.MLA
