from flask import Blueprint, jsonify
from controllers.profile_controller import (
    get_user_profile,
    get_user_jobs,
    get_user_applications
)

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/api/users/<int:id>', methods=['GET'])
def user_profile(id):
    return get_user_profile(id)

@users_bp.route('/api/users/<int:id>/jobs', methods=['GET'])
def user_jobs(id):
    return get_user_jobs(id)

@users_bp.route('/api/users/<int:id>/applications', methods=['GET'])
def user_applications(id):
    return get_user_applications(id)
