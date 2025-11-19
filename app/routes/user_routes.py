"""
User routes for user data management.
No authentication logic - NextAuth handles authentication.
Backend only provides user data operations.
"""

from flask import Blueprint, jsonify, request

from app.services.user_service import UserService
from app.database import get_db_session
from app.database.models import User

# Create blueprint
user_bp = Blueprint("user", __name__, url_prefix="/api/v1/users")

# Initialize user service
user_service = UserService()


# ==================== USER ROUTES ====================

@user_bp.route("/sync", methods=["POST"])
def sync_user():
    """
    Sync user from NextAuth to backend database.
    Called by NextAuth after successful Google OAuth.
    
    Request body:
        {
            "id": "google_user_id",
            "email": "user@example.com",
            "name": "John Doe",
            "profile_picture": "https://..."
        }
    """
    try:
        data = request.get_json()
        
        user_id = data.get('id')
        email = data.get('email')
        name = data.get('name')
        profile_picture = data.get('profile_picture')
        
        if not user_id or not email:
            return jsonify({
                'success': False,
                'error': 'User ID and email are required'
            }), 400
        
        # Get or create user in backend
        user = user_service.get_or_create_user({
            'id': user_id,
            'email': email,
            'name': name,
            'profile_picture': profile_picture
        })
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to sync user: {str(e)}'
        }), 500


@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get user information by ID."""
    try:
        user = user_service.get_user_by_id(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get user: {str(e)}'
        }), 500


@user_bp.route("/<user_id>", methods=["PUT"])
def update_profile(user_id):
    """
    Update user profile.
    
    Request body:
        {
            "name": "John Doe",
            "phone": "+91-9876543210",
            "state": "Delhi",
            "city": "New Delhi",
            "age_group": "26-35",
            "preferred_parties": ["Bharatiya Janata Party", "Indian National Congress"],
            "topics_of_interest": ["Economy", "Healthcare", "Education"]
        }
    """
    try:
        data = request.get_json()
        
        # Handle preferred_parties and topics_of_interest separately (convert lists to strings)
        update_data = {}
        for key, value in data.items():
            if key == 'preferred_parties' or key == 'topics_of_interest':
                # Convert list to comma-separated string
                if isinstance(value, list):
                    update_data[key] = ",".join(value) if value else None
                else:
                    update_data[key] = value
            elif key in ['name', 'phone', 'state', 'city', 'age_group', 'profile_picture']:
                update_data[key] = value
        
        # Update user
        updated_user = user_service.update_user_profile(user_id, **update_data)
        
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


@user_bp.route("/<user_id>/onboarding", methods=["POST"])
def complete_onboarding(user_id):
    """
    Complete user onboarding with political inclination and username.
    
    Request body:
        {
            "username": "johndoe",
            "political_interest": "Rightist"
        }
    """
    try:
        data = request.get_json()
        
        # Validate username if provided
        username = data.get('username')
        if username:
            # Check if username is already taken by another user
            with get_db_session() as session:
                existing_user = User.get_by_username(session, username)
                if existing_user and existing_user.id != user_id:
                    return jsonify({
                        'success': False,
                        'error': 'Username is already taken'
                    }), 400
        
        # Complete onboarding - only political_interest and username
        updated_user = user_service.complete_user_onboarding(
            user_id=user_id,
            username=username,
            political_interest=data.get('political_interest')
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


@user_bp.route("/check-username", methods=["POST"])
def check_username():
    """
    Check if a username is available.
    
    Request body:
        {
            "username": "johndoe",
            "user_id": "optional_user_id_to_exclude"
        }
    """
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        user_id = data.get('user_id')  # Optional: exclude this user from check
        
        if not username:
            return jsonify({
                'success': False,
                'error': 'Username is required'
            }), 400
        
        # Check if username is available
        is_available = user_service.check_username_available(username, exclude_user_id=user_id)
        
        return jsonify({
            'success': True,
            'available': is_available
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to check username: {str(e)}'
        }), 500


# ==================== HEALTH CHECK ====================

@user_bp.route("/health", methods=["GET"])
def user_health():
    """Check user service health."""
    return jsonify({
        'success': True,
        'service': 'User Service',
        'message': 'User service is operational'
    })

