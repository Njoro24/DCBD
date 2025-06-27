from flask import jsonify
from models.user import User
from sqlalchemy.exc import SQLAlchemyError

def get_user_posted_jobs(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        jobs = [job.to_dict() for job in user.posted_jobs]
        return jsonify(jobs), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
