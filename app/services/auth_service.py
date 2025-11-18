"""
Authentication service for Google OAuth.
"""

import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

import jwt
from authlib.integrations.flask_client import OAuth

from app.database import get_db_session
from app.database.models import User


class AuthService:
    """Service for handling authentication operations."""

    def __init__(self):
        """Initialize authentication service."""
        self.oauth = OAuth()
        self.jwt_secret = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
        self.jwt_algorithm = "HS256"
        self.token_expiry_hours = 24

    def configure_google_oauth(self, app):
        """
        Configure Google OAuth provider.
        
        Args:
            app: Flask application instance
        """
        self.oauth.init_app(app)
        
        # Register Google OAuth provider
        self.google = self.oauth.register(
            name='google',
            client_id=os.getenv('GOOGLE_CLIENT_ID'),
            client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile'
            }
        )

    def get_or_create_user(self, google_user_info: Dict[str, Any]) -> User:
        """
        Get existing user or create a new one from Google user info.
        
        Args:
            google_user_info: User information from Google OAuth
            
        Returns:
            User object
        """
        with get_db_session() as session:
            user_id = google_user_info.get('sub')  # Google user ID
            email = google_user_info.get('email')
            name = google_user_info.get('name')
            picture = google_user_info.get('picture')
            
            # Check if user exists
            user = User.get_by_id(session, user_id)
            
            if not user:
                # Create new user
                user = User.create(
                    session=session,
                    id=user_id,
                    email=email,
                    name=name,
                    profile_picture=picture
                )
            else:
                # Update profile picture if changed
                if picture and user.profile_picture != picture:
                    user.update(session, profile_picture=picture)
            
            # Update last login
            user.update_last_login(session)
            
            return user

    def create_jwt_token(self, user: User) -> str:
        """
        Create a JWT token for the user.
        
        Args:
            user: User object
            
        Returns:
            JWT token string
        """
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return token

    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload or None if invalid
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def get_user_from_token(self, token: str) -> Optional[User]:
        """
        Get user from JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            User object or None if token is invalid
        """
        payload = self.verify_jwt_token(token)
        if not payload:
            return None
        
        user_id = payload.get('user_id')
        if not user_id:
            return None
        
        with get_db_session() as session:
            user = User.get_by_id(session, user_id)
            return user

    def update_user_profile(
        self,
        user_id: str,
        **kwargs
    ) -> Optional[User]:
        """
        Update user profile information.
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated user object or None if user not found
        """
        with get_db_session() as session:
            user = User.get_by_id(session, user_id)
            if not user:
                return None
            
            user.update(session, **kwargs)
            return user

    def complete_user_onboarding(
        self,
        user_id: str,
        username: Optional[str] = None,
        phone: Optional[str] = None,
        state: Optional[str] = None,
        city: Optional[str] = None,
        age_group: Optional[str] = None,
        political_interest: Optional[str] = None,
        preferred_parties: Optional[list] = None,
        topics_of_interest: Optional[list] = None,
    ) -> Optional[User]:
        """
        Complete user onboarding with profile and political preferences.
        
        Args:
            user_id: User ID
            username: Unique username
            phone: Phone number
            state: State of residence
            city: City of residence
            age_group: Age group
            political_interest: Level of political interest
            preferred_parties: List of preferred party names
            topics_of_interest: List of topics of interest
            
        Returns:
            Updated user object or None if user not found
        """
        with get_db_session() as session:
            user = User.get_by_id(session, user_id)
            if not user:
                return None
            
            # Convert lists to comma-separated strings
            preferred_parties_str = ",".join(preferred_parties) if preferred_parties else None
            topics_str = ",".join(topics_of_interest) if topics_of_interest else None
            
            user.complete_onboarding(
                session=session,
                username=username,
                phone=phone,
                state=state,
                city=city,
                age_group=age_group,
                political_interest=political_interest,
                preferred_parties=preferred_parties_str,
                topics_of_interest=topics_str
            )
            
            return user

    def check_username_available(self, username: str) -> bool:
        """
        Check if username is available.
        
        Args:
            username: Username to check
            
        Returns:
            True if username is available, False otherwise
        """
        with get_db_session() as session:
            user = User.get_by_username(session, username)
            return user is None
