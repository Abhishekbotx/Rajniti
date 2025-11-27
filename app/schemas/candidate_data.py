from typing import List, Optional, Literal
from pydantic import BaseModel, Field, validator
import re

class EducationDetails(BaseModel):
    year: Optional[str] = Field(None, description="Year of completion")
    college: Optional[str] = Field(None, description="Name of the college or school")
    stream: Optional[str] = Field(None, description="Field of study or stream")
    other_details: Optional[str] = Field(None, description="Any other relevant details")

    @validator('year')
    def validate_year(cls, v):
        if v and not re.match(r'^\d{4}$', str(v)):
            raise ValueError('Year must be a 4-digit number')
        return v

class PoliticalHistory(BaseModel):
    party: str = Field(..., min_length=2, description="Name of the political party")
    constituency: Optional[str] = Field(None, min_length=2, description="Constituency contested from")
    election_year: Optional[str] = Field(None, description="Year of the election")
    position: Optional[str] = Field(None, description="Position contested for (e.g., MP, MLA)")
    result: Optional[Literal["WON", "LOST"]] = Field(None, description="Result of the election")

    @validator('election_year')
    def validate_year(cls, v):
        if v and not re.match(r'^\d{4}$', str(v)):
            raise ValueError('Year must be a 4-digit number')
        return v

class FamilyMember(BaseModel):
    name: Optional[str] = Field(None, min_length=2, description="Name of the family member")
    profession: Optional[str] = Field(None, description="Profession of the family member")
    relation: str = Field(..., min_length=2, description="Relation to the candidate")
    age: Optional[str] = Field(None, description="Age of the family member")

class AssetDetails(BaseModel):
    type: Literal["CASH", "BOND", "LAND", "EQUITY", "AUTOMOBILE", "JEWELRY", "OTHER"] = Field(..., description="Type of asset")
    amount: Optional[float] = Field(None, ge=0, description="Monetary value of the asset")
    description: Optional[str] = Field(None, description="Description or details of the asset")
    owned_by: Literal["SELF", "SPOUSE", "DEPENDENT", "HUF", "OTHER"] = Field("SELF", description="Owner of the asset")

class LiabilityDetails(BaseModel):
    type: Literal["LOAN", "OTHER"] = Field(..., description="Type of liability")
    amount: Optional[float] = Field(None, ge=0, description="Monetary value of the liability")
    description: Optional[str] = Field(None, description="Description or details of the liability")
    owned_by: Literal["SELF", "SPOUSE", "DEPENDENT", "HUF", "OTHER"] = Field("SELF", description="Owner of the liability")

class CrimeCaseDetails(BaseModel):
    fir_no: Optional[str] = Field(None, description="FIR Number")
    police_station: Optional[str] = Field(None, description="Police Station")
    sections_applied: List[str] = Field(default_factory=list, description="List of IPC or other sections applied")
    charges_framed: bool = Field(False, description="Whether charges have been framed")
    description: Optional[str] = Field(None, description="Brief description of the case")

class CandidateDetailedProfile(BaseModel):
    education_background: List[EducationDetails] = Field(default_factory=list)
    political_background: List[PoliticalHistory] = Field(default_factory=list)
    family_background: List[FamilyMember] = Field(default_factory=list)
    assets: List[AssetDetails] = Field(default_factory=list)
    liabilities: List[LiabilityDetails] = Field(default_factory=list)
    crime_cases: List[CrimeCaseDetails] = Field(default_factory=list)
