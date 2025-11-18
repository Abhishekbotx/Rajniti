"""
Tests for authentication functionality.
"""
import pytest
from app.database.models import User


def test_user_model_creation():
    """Test User model can be instantiated."""
    user = User(
        id="test_123",
        email="test@example.com",
        name="Test User",
        profile_picture="https://example.com/pic.jpg",
        onboarding_completed=False
    )
    
    assert user.id == "test_123"
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.profile_picture == "https://example.com/pic.jpg"
    assert user.onboarding_completed is False


def test_user_to_dict():
    """Test User model to_dict method."""
    user = User(
        id="test_123",
        email="test@example.com",
        name="Test User",
        username="testuser",
        phone="+91-9876543210",
        state="Delhi",
        city="New Delhi",
        age_group="26-35",
        political_interest="Rightist",
        preferred_parties="BJP,INC",
        topics_of_interest="Economy,Healthcare",
        onboarding_completed=True
    )
    
    user_dict = user.to_dict()
    
    assert user_dict['id'] == "test_123"
    assert user_dict['email'] == "test@example.com"
    assert user_dict['name'] == "Test User"
    assert user_dict['username'] == "testuser"
    assert user_dict['phone'] == "+91-9876543210"
    assert user_dict['state'] == "Delhi"
    assert user_dict['city'] == "New Delhi"
    assert user_dict['age_group'] == "26-35"
    assert user_dict['political_interest'] == "Rightist"
    assert user_dict['preferred_parties'] == ["BJP", "INC"]
    assert user_dict['topics_of_interest'] == ["Economy", "Healthcare"]
    assert user_dict['onboarding_completed'] is True


def test_user_model_fields():
    """Test User model has all required fields."""
    required_fields = [
        'id', 'email', 'name', 'username', 'profile_picture',
        'phone', 'state', 'city', 'age_group',
        'political_interest', 'preferred_parties', 'topics_of_interest',
        'onboarding_completed', 'created_at', 'updated_at', 'last_login'
    ]
    
    user = User(id="test", email="test@example.com")
    
    for field in required_fields:
        assert hasattr(user, field), f"User model missing field: {field}"


def test_auth_service_imports():
    """Test auth service can be imported."""
    from app.services.auth_service import AuthService
    
    auth_service = AuthService()
    
    assert auth_service is not None
    assert hasattr(auth_service, 'oauth')
    assert hasattr(auth_service, 'jwt_secret')
    assert hasattr(auth_service, 'jwt_algorithm')
    assert hasattr(auth_service, 'create_jwt_token')
    assert hasattr(auth_service, 'verify_jwt_token')
    assert hasattr(auth_service, 'get_user_from_token')
    assert hasattr(auth_service, 'check_username_available')


def test_auth_routes_import():
    """Test auth routes can be imported."""
    from app.routes.auth_routes import auth_bp, token_required
    
    assert auth_bp is not None
    assert auth_bp.name == "auth"
    assert auth_bp.url_prefix == "/api/v1/auth"
    assert token_required is not None
