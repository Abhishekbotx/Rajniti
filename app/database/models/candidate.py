"""
Candidate database model with CRUD operations.
"""

from typing import List, Optional

from sqlalchemy import Column, Enum as SQLEnum, String
from sqlalchemy.orm import Session

from ..base import Base


class Candidate(Base):
    """
    Candidate database model.
    
    Stores election candidate information.
    """
    
    __tablename__ = "candidates"
    
    # Columns
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    party_id = Column(String, nullable=False, index=True)
    constituency_id = Column(String, nullable=False, index=True)
    state_id = Column(String, nullable=False, index=True)
    image_url = Column(String, nullable=True)
    status = Column(SQLEnum("WON", "LOST", name="candidate_status"), nullable=False)
    type = Column(SQLEnum("MP", "MLA", name="candidate_type"), nullable=False, default="MP")
    
    def __repr__(self) -> str:
        return f"<Candidate(id={self.id}, name={self.name}, party_id={self.party_id})>"
    
    # CRUD Operations
    
    @classmethod
    def create(
        cls,
        session: Session,
        id: str,
        name: str,
        party_id: str,
        constituency_id: str,
        state_id: str,
        status: str,
        type: str = "MP",
        image_url: Optional[str] = None,
    ) -> "Candidate":
        """
        Create a new candidate.
        
        Args:
            session: Database session
            id: Candidate ID
            name: Candidate name
            party_id: Party ID
            constituency_id: Constituency ID
            state_id: State ID code
            status: Candidate status (WON/LOST)
            type: Candidate type (MP/MLA), defaults to MP
            image_url: URL to candidate image (optional)
        
        Returns:
            Created Candidate instance
        """
        candidate = cls(
            id=id,
            name=name,
            party_id=party_id,
            constituency_id=constituency_id,
            state_id=state_id,
            status=status,
            type=type,
            image_url=image_url,
        )
        session.add(candidate)
        session.flush()
        return candidate
    
    @classmethod
    def get_by_id(cls, session: Session, candidate_id: str) -> Optional["Candidate"]:
        """
        Get candidate by ID.
        
        Args:
            session: Database session
            candidate_id: Candidate ID
        
        Returns:
            Candidate instance or None if not found
        """
        return session.query(cls).filter(cls.id == candidate_id).first()
    
    @classmethod
    def get_by_party(cls, session: Session, party_id: str) -> List["Candidate"]:
        """
        Get all candidates for a party.
        
        Args:
            session: Database session
            party_id: Party ID
        
        Returns:
            List of Candidate instances
        """
        return session.query(cls).filter(cls.party_id == party_id).all()
    
    @classmethod
    def get_by_constituency(cls, session: Session, constituency_id: str) -> List["Candidate"]:
        """
        Get all candidates for a constituency.
        
        Args:
            session: Database session
            constituency_id: Constituency ID
        
        Returns:
            List of Candidate instances
        """
        return session.query(cls).filter(cls.constituency_id == constituency_id).all()
    
    @classmethod
    def get_winners(cls, session: Session, skip: int = 0, limit: int = 100) -> List["Candidate"]:
        """
        Get all winning candidates with pagination.
        
        Args:
            session: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
        
        Returns:
            List of Candidate instances
        """
        return session.query(cls).filter(cls.status == "WON").offset(skip).limit(limit).all()
    
    @classmethod
    def search_by_name(cls, session: Session, name: str) -> List["Candidate"]:
        """
        Search candidates by name (case-insensitive, partial match).
        
        Args:
            session: Database session
            name: Name to search for
        
        Returns:
            List of Candidate instances
        """
        return session.query(cls).filter(cls.name.ilike(f"%{name}%")).all()
    
    @classmethod
    def get_all(cls, session: Session, skip: int = 0, limit: int = 100) -> List["Candidate"]:
        """
        Get all candidates with pagination.
        
        Args:
            session: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
        
        Returns:
            List of Candidate instances
        """
        return session.query(cls).offset(skip).limit(limit).all()
    
    def update(self, session: Session, **kwargs) -> "Candidate":
        """
        Update candidate attributes.
        
        Args:
            session: Database session
            **kwargs: Attributes to update
        
        Returns:
            Updated Candidate instance
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        session.flush()
        return self
    
    def delete(self, session: Session) -> None:
        """
        Delete this candidate.
        
        Args:
            session: Database session
        """
        session.delete(self)
        session.flush()
    
    @classmethod
    def bulk_create(cls, session: Session, candidates: List[dict]) -> List["Candidate"]:
        """
        Create multiple candidates at once.
        
        Args:
            session: Database session
            candidates: List of candidate dictionaries
        
        Returns:
            List of created Candidate instances
        """
        candidate_objects = [
            cls(
                id=c["id"],
                name=c["name"],
                party_id=c["party_id"],
                constituency_id=c["constituency_id"],
                state_id=c["state_id"],
                status=c["status"],
                type=c.get("type", "MP"),
                image_url=c.get("image_url"),
            )
            for c in candidates
        ]
        session.bulk_save_objects(candidate_objects, return_defaults=True)
        session.flush()
        return candidate_objects
