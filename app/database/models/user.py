"""
User database model with authentication and onboarding support.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, String, Text
from sqlalchemy.orm import Session

from ..base import Base


class User(Base):
    """
    User database model for authentication and onboarding.

    Stores user authentication details, profile information, and political preferences.
    """

    __tablename__ = "users"

    # Primary identification
    id = Column(String, primary_key=True, index=True)  # Google user ID
    email = Column(String, unique=True, nullable=False, index=True)
    
    # Basic profile information
    name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    
    # Onboarding information
    phone = Column(String, nullable=True)
    state = Column(String, nullable=True)
    city = Column(String, nullable=True)
    age_group = Column(String, nullable=True)  # e.g., "18-25", "26-35", etc.
    
    # Political preferences
    political_interest = Column(String, nullable=True)  # e.g., "High", "Medium", "Low"
    preferred_parties = Column(Text, nullable=True)  # Comma-separated party names
    topics_of_interest = Column(Text, nullable=True)  # Comma-separated topics
    
    # Onboarding status
    onboarding_completed = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"

    # CRUD Operations

    @classmethod
    def create(
        cls,
        session: Session,
        id: str,
        email: str,
        name: Optional[str] = None,
        profile_picture: Optional[str] = None,
    ) -> "User":
        """
        Create a new user.

        Args:
            session: Database session
            id: User ID (Google user ID)
            email: User email
            name: User's full name
            profile_picture: URL to profile picture

        Returns:
            Created user object
        """
        user = cls(
            id=id,
            email=email,
            name=name,
            profile_picture=profile_picture,
            onboarding_completed=False,
        )
        session.add(user)
        session.flush()
        return user

    @classmethod
    def get_by_id(cls, session: Session, user_id: str) -> Optional["User"]:
        """Get user by ID."""
        return session.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def get_by_email(cls, session: Session, email: str) -> Optional["User"]:
        """Get user by email."""
        return session.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_all(cls, session: Session) -> List["User"]:
        """Get all users."""
        return session.query(cls).all()

    def update(
        self,
        session: Session,
        **kwargs
    ) -> "User":
        """
        Update user fields.

        Args:
            session: Database session
            **kwargs: Fields to update

        Returns:
            Updated user object
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        session.flush()
        return self

    def complete_onboarding(
        self,
        session: Session,
        phone: Optional[str] = None,
        state: Optional[str] = None,
        city: Optional[str] = None,
        age_group: Optional[str] = None,
        political_interest: Optional[str] = None,
        preferred_parties: Optional[str] = None,
        topics_of_interest: Optional[str] = None,
    ) -> "User":
        """
        Complete user onboarding with basic details and political preferences.

        Args:
            session: Database session
            phone: Phone number
            state: State of residence
            city: City of residence
            age_group: Age group
            political_interest: Level of political interest
            preferred_parties: Comma-separated list of preferred parties
            topics_of_interest: Comma-separated list of topics of interest

        Returns:
            Updated user object
        """
        self.phone = phone
        self.state = state
        self.city = city
        self.age_group = age_group
        self.political_interest = political_interest
        self.preferred_parties = preferred_parties
        self.topics_of_interest = topics_of_interest
        self.onboarding_completed = True
        self.updated_at = datetime.utcnow()
        session.flush()
        return self

    def update_last_login(self, session: Session) -> "User":
        """Update last login timestamp."""
        self.last_login = datetime.utcnow()
        session.flush()
        return self

    def delete(self, session: Session) -> None:
        """Delete user."""
        session.delete(self)
        session.flush()

    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "profile_picture": self.profile_picture,
            "phone": self.phone,
            "state": self.state,
            "city": self.city,
            "age_group": self.age_group,
            "political_interest": self.political_interest,
            "preferred_parties": self.preferred_parties.split(",") if self.preferred_parties else [],
            "topics_of_interest": self.topics_of_interest.split(",") if self.topics_of_interest else [],
            "onboarding_completed": self.onboarding_completed,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
