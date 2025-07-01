from flask import Blueprint
from flask_restful import Api
from resources.user_profile_resource import UserProfileResource  

# Create Blueprint for user routes
users_bp = Blueprint("users", __name__, url_prefix="/api/users")
api = Api(users_bp)

# Register user profile route: GET /api/users/<user_id>
api.add_resource(UserProfileResource, "/<int:user_id>")
