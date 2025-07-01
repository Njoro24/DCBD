from flask import Blueprint, request, jsonify, current_app
from models.job import Job
from models.user import User
from models import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

def error_response(message, status_code):
    return jsonify({'error': message}), status_code

def success_response(data=None, message=None, status_code=200):
    response = {}
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    return jsonify(response), status_code

@jobs_bp.route('', methods=['GET'])
def get_all_jobs():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        include_user = request.args.get('include_user', 'false').lower() == 'true'
        status = request.args.get('status')
        category = request.args.get('category')
        is_featured = request.args.get('is_featured')

        query = Job.query

        # Apply filters
        if status:
            query = query.filter(Job.status == status)
        if category:
            query = query.filter(Job.category == category)
        if is_featured is not None:
            query = query.filter(Job.is_featured == (is_featured.lower() == 'true'))

        jobs = query.order_by(Job.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return success_response({
            'jobs': [job.to_dict(include_user=include_user) for job in jobs.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': jobs.total,
                'pages': jobs.pages
            }
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching jobs: {str(e)}")
        return error_response("Failed to fetch jobs", 500)

@jobs_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    try:
        include_user = request.args.get('include_user', 'false').lower() == 'true'
        job = Job.query.get(job_id)
        if not job:
            return error_response("Job not found", 404)
        return success_response(job.to_dict(include_user=include_user))
    except Exception as e:
        current_app.logger.error(f"Error fetching job {job_id}: {str(e)}")
        return error_response("Failed to fetch job", 500)

@jobs_bp.route('', methods=['POST'])
def create_job():
    try:
        data = request.get_json()

        required_fields = ['user_id', 'title', 'description']
        for field in required_fields:
            if not data or field not in data:
                return error_response(f"Missing required field: {field}", 400)

        # Verify user exists
        user = User.query.get(data['user_id'])
        if not user:
            return error_response("User not found", 400)

        # Parse deadline if provided
        deadline = None
        if data.get('deadline'):
            try:
                deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
            except ValueError:
                return error_response("Invalid deadline format. Use ISO 8601 format", 400)

        new_job = Job(
            user_id=data['user_id'],
            title=data['title'],
            description=data['description'],
            requirements=data.get('requirements'),
            budget_min=data.get('budget_min'),
            budget_max=data.get('budget_max'),
            currency=data.get('currency', 'USD'),
            is_featured=data.get('is_featured', False),
            status=data.get('status', 'open'),
            category=data.get('category'),
            skills_required=data.get('skills_required'),
            deadline=deadline
        )

        db.session.add(new_job)
        db.session.commit()

        return success_response(new_job.to_dict(include_user=True), "Job created successfully", 201)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating job: {str(e)}")
        return error_response("Failed to create job", 500)

@jobs_bp.route('/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    try:
        job = Job.query.get(job_id)
        if not job:
            return error_response("Job not found", 404)

        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)

        updatable_fields = [
            'title', 'description', 'requirements', 'budget_min', 'budget_max',
            'currency', 'is_featured', 'status', 'category', 'skills_required'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(job, field, data[field])

        # Handle deadline separately
        if 'deadline' in data:
            if data['deadline']:
                try:
                    job.deadline = datetime.fromisoformat(data['deadline'].replace('Z', '+00:00'))
                except ValueError:
                    return error_response("Invalid deadline format. Use ISO 8601 format", 400)
            else:
                job.deadline = None

        db.session.commit()
        return success_response(job.to_dict(include_user=True), "Job updated successfully")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating job {job_id}: {str(e)}")
        return error_response("Failed to update job", 500)

@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        job = Job.query.get(job_id)
        if not job:
            return error_response("Job not found", 404)

        db.session.delete(job)
        db.session.commit()
        return success_response(message="Job deleted successfully")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting job {job_id}: {str(e)}")
        return error_response("Failed to delete job", 500)

@jobs_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_jobs(user_id):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')

        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return error_response("User not found", 404)

        query = Job.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter(Job.status == status)

        jobs = query.order_by(Job.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return success_response({
            'jobs': [job.to_dict() for job in jobs.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': jobs.total,
                'pages': jobs.pages
            }
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching jobs for user {user_id}: {str(e)}")
        return error_response("Failed to fetch user jobs", 500)

@jobs_bp.route('/featured', methods=['GET'])
def get_featured_jobs():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        include_user = request.args.get('include_user', 'false').lower() == 'true'

        jobs = Job.query.filter_by(is_featured=True, status='open').order_by(
            Job.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)

        return success_response({
            'jobs': [job.to_dict(include_user=include_user) for job in jobs.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': jobs.total,
                'pages': jobs.pages
            }
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching featured jobs: {str(e)}")
        return error_response("Failed to fetch featured jobs", 500)