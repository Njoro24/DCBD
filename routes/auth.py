# routes/auth.py

from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from controllers.auth_controller import register_user, login_user, get_current_user

auth_bp = Blueprint("auth", __name__)
api = Api(auth_bp)

# --- Auth Resources ---
class RegisterAPI(Resource):
    def post(self):
        return register_user()

class LoginAPI(Resource):
    def post(self):
        return login_user()

class MeAPI(Resource):
    @jwt_required()
    def get(self):
        return get_current_user()

# --- Register RESTful Routes ---
api.add_resource(RegisterAPI, '/api/auth/register')
api.add_resource(LoginAPI, '/api/auth/login')
api.add_resource(MeAPI, '/api/auth/me')

# --- Verify Token (Non-Resource Route) ---
@auth_bp.route('/api/auth/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    return jsonify({"message": "Token is valid"}), 200
