# routes/jobs.py

from flask import Blueprint, request, jsonify, current_app
from extensions import db  # ✅ CORRECT import
from models.job import Job  # ✅ Import Job model only — don't redefine it!
from sqlalchemy.exc import IntegrityError

# ✅ Register Blueprint
jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

# ✅ Helper functions
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

def success_response(data=None, message=None, status_code=200):
    response = {}
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    return jsonify(response), status_code

# ✅ CRUD Routes

# GET /api/jobs
@jobs_bp.route('', methods=['GET'])
def get_all_jobs():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        query = Job.query
        if status:
            query = query.filter_by(status=status)
        jobs = query.order_by(Job.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
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
        current_app.logger.error(f"Error fetching jobs: {str(e)}")
        return error_response("Failed to fetch jobs", 500)

# GET /api/jobs/featured
@jobs_bp.route('/featured', methods=['GET'])
def get_featured_jobs():
    try:
        featured_jobs = Job.query.filter_by(is_featured=True).order_by(Job.created_at.desc()).all()
        return success_response({
            'jobs': [job.to_dict() for job in featured_jobs],
            'count': len(featured_jobs)
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching featured jobs: {str(e)}")
        return error_response("Failed to fetch featured jobs", 500)

# GET /api/jobs/<id>
@jobs_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    try:
        job = Job.query.get(job_id)
        if not job:
            return error_response("Job not found", 404)
        return success_response(job.to_dict())
    except Exception as e:
        current_app.logger.error(f"Error fetching job {job_id}: {str(e)}")
        return error_response("Failed to fetch job", 500)

# POST /api/jobs
@jobs_bp.route('', methods=['POST'])
def create_job():
    try:
        data = request.get_json()
        required_fields = ['client_id', 'title', 'description']
        for field in required_fields:
            if not data or field not in data:
                return error_response(f"Missing required field: {field}", 400)
        new_job = Job(
            client_id=data['client_id'],
            title=data['title'],
            description=data['description'],
            requirements=data.get('requirements'),
            budget=data.get('budget'),
            is_featured=data.get('is_featured', False),
            status=data.get('status', 'open')
        )
        db.session.add(new_job)
        db.session.commit()
        return success_response(new_job.to_dict(), "Job created successfully", 201)
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(f"Database integrity error: {str(e)}")
        return error_response("Invalid client_id or constraint violation", 400)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating job: {str(e)}")
        return error_response("Failed to create job", 500)

# PUT /api/jobs/<id>
@jobs_bp.route('/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    try:
        job = Job.query.get(job_id)
        if not job:
            return error_response("Job not found", 404)
        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)
        for field in ['title', 'description', 'requirements', 'budget', 'is_featured', 'status']:
            if field in data:
                setattr(job, field, data[field])
        db.session.commit()
        return success_response(job.to_dict(), "Job updated successfully")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating job {job_id}: {str(e)}")
        return error_response("Failed to update job", 500)

# PATCH /api/jobs/<id>
@jobs_bp.route('/<int:job_id>', methods=['PATCH'])
def patch_job(job_id):
    try:
        job = Job.query.get(job_id)
        if not job:
            return error_response("Job not found", 404)
        data = request.get_json()
        if not data:
            return error_response("No data provided", 400)
        updated_fields = []
        for field in ['title', 'description', 'requirements', 'budget', 'is_featured', 'status']:
            if field in data:
                setattr(job, field, data[field])
                updated_fields.append(field)
        if not updated_fields:
            return error_response("No valid fields provided for update", 400)
        db.session.commit()
        return success_response(job.to_dict(), f"Updated fields: {', '.join(updated_fields)}")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error patching job {job_id}: {str(e)}")
        return error_response("Failed to update job", 500)

# DELETE /api/jobs/<id>
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
