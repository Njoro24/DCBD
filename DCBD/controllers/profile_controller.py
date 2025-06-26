from flask import jsonify
from models.user import User
from models.job import Job
from models.application import Application
from database.db import db

def get_user_profile(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200

def get_user_jobs(user_id):
    jobs = Job.query.filter_by(client_id=user_id).all()
    return jsonify([job.to_dict() for job in jobs]), 200

def get_user_applications(user_id):
    apps = Application.query.filter_by(applicant_id=user_id).all()
    return jsonify([app.to_dict() for app in apps]), 200
