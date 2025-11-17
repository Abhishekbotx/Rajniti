"""
Authentication routes for Google OAuth and user management.
"""

from flask import Blueprint, jsonify, request, redirect, url_for, current_app
from functools import wraps

from app.services.auth_service import AuthService
from app.database import get_db_session
from app.database.models import User

# Create blueprint
auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

# Initialize auth service
auth_service = AuthService()


def token_required(f):
    """
    Decorator to require authentication token.
    
    Usage:
        @auth_bp.route('/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({"user": current_user.to_dict()})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'success': False, 'error': 'Token is missing'}), 401
        
        # Verify token and get user
        user = auth_service.get_user_from_token(token)
        if not user:
            return jsonify({'success': False, 'error': 'Token is invalid or expired'}), 401
        
        return f(current_user=user, *args, **kwargs)
    
    return decorated


# ==================== GOOGLE OAUTH ROUTES ====================

@auth_bp.route("/google/login", methods=["GET"])
def google_login():
    """
    Initiate Google OAuth login.
    
    Redirects to Google's OAuth consent screen.
    """
    try:
        redirect_uri = url_for('auth.google_callback', _external=True)
        return auth_service.google.authorize_redirect(redirect_uri)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to initiate Google login: {str(e)}'
        }), 500


@auth_bp.route("/google/callback", methods=["GET"])
def google_callback():
    """
    Handle Google OAuth callback.
    
    Exchanges authorization code for user info and creates/updates user.
    """
    try:
        # Get token from Google
        token = auth_service.google.authorize_access_token()
        
        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            # Fetch user info if not in token
            resp = auth_service.google.get('userinfo')
            user_info = resp.json()
        
        # Get or create user
        user = auth_service.get_or_create_user(user_info)
        
        # Create JWT token
        jwt_token = auth_service.create_jwt_token(user)
        
        # In production, redirect to frontend with token
        # For now, return the token
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:3000')
        redirect_url = f"{frontend_url}/auth/callback?token={jwt_token}"
        
        return redirect(redirect_url)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Authentication failed: {str(e)}'
        }), 500


@auth_bp.route("/logout", methods=["POST"])
@token_required
def logout(current_user):
    """
    Logout user.
    
    Note: With JWT, we can't invalidate tokens server-side.
    Client should delete the token from storage.
    """
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })


# ==================== USER ROUTES ====================

@auth_bp.route("/me", methods=["GET"])
@token_required
def get_current_user(current_user):
    """Get current authenticated user's information."""
    return jsonify({
        'success': True,
        'data': current_user.to_dict()
    })


@auth_bp.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    """
    Update user profile.
    
    Request body:
        {
            "name": "John Doe",
            "phone": "+91-9876543210",
            "state": "Delhi",
            "city": "New Delhi",
            "age_group": "26-35"
        }
    """
    try:
        data = request.get_json()
        
        # Allowed fields for update
        allowed_fields = ['name', 'phone', 'state', 'city', 'age_group']
        update_data = {k: v for k, v in data.items() if k in allowed_fields}
        
        # Update user
        updated_user = auth_service.update_user_profile(current_user.id, **update_data)
        
        if not updated_user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': updated_user.to_dict(),
            'message': 'Profile updated successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update profile: {str(e)}'
        }), 500


@auth_bp.route("/onboarding", methods=["POST"])
@token_required
def complete_onboarding(current_user):
    """
    Complete user onboarding with basic details and political preferences.
    
    Request body:
        {
            "phone": "+91-9876543210",
            "state": "Delhi",
            "city": "New Delhi",
            "age_group": "26-35",
            "political_interest": "High",
            "preferred_parties": ["Bharatiya Janata Party", "Indian National Congress"],
            "topics_of_interest": ["Economy", "Healthcare", "Education"]
        }
    """
    try:
        data = request.get_json()
        
        # Complete onboarding
        updated_user = auth_service.complete_user_onboarding(
            user_id=current_user.id,
            phone=data.get('phone'),
            state=data.get('state'),
            city=data.get('city'),
            age_group=data.get('age_group'),
            political_interest=data.get('political_interest'),
            preferred_parties=data.get('preferred_parties', []),
            topics_of_interest=data.get('topics_of_interest', [])
        )
        
        if not updated_user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': updated_user.to_dict(),
            'message': 'Onboarding completed successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to complete onboarding: {str(e)}'
        }), 500


# ==================== HEALTH CHECK ====================

@auth_bp.route("/health", methods=["GET"])
def auth_health():
    """Check authentication service health."""
    google_configured = bool(
        current_app.config.get('GOOGLE_CLIENT_ID') and 
        current_app.config.get('GOOGLE_CLIENT_SECRET')
    )
    
    return jsonify({
        'success': True,
        'service': 'Authentication',
        'google_oauth': {
            'configured': google_configured
        }
    })
