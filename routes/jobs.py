kibet
# routes/jobs.py

from flask import Blueprint, request, jsonify, current_app
from extensions import db  # CORRECT import
from models.job import Job  #  Import Job model only — don't redefine it!
from sqlalchemy.exc import IntegrityError

#  Register Blueprint
jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

#  Helper functions
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

def success_response(data=None, message=None, status_code=200):
    response = {}
    if data is not None:
        response['data'] = data
    if message:
        response['message'] = message
    return jsonify(response), status_code

#  CRUD Routes

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

from flask import Flask, request
from flask_restful import Api, Resource
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from controllers.job_controller import JobController
from controllers.user_controller import UserController
import os

app = Flask(__name__)
api = Api(app)


DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///jobs.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

class JobResource(Resource):
    def get(self, job_id):
        """
        GET /api/jobs/:id
        Get job by ID with client information
        """
        db = get_db()
        job_controller = JobController(db)
        
        try:
            job = job_controller.get_job_by_id(job_id)
            
            if not job:
                return {'error': 'Job not found'}, 404
            
            return job, 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500
        finally:
            db.close()

class UserResource(Resource):
    def get(self, user_id):
        """
        GET /api/users/:id
        Fetch client info associated with a job
        """
        db = get_db()
        user_controller = UserController(db)
        
        try:
            user = user_controller.get_client_info(user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            return user, 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500
        finally:
            db.close()

class JobApplicationResource(Resource):
    def post(self, job_id):
        """
        POST /api/jobs/:id/apply
        Handle job application logic
        """
        db = get_db()
        job_controller = JobController(db)
        
        try:
            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            applicant_id = data.get('applicant_id')
            if not applicant_id:
                return {'error': 'Applicant ID is required'}, 400

            application_data = {
                'cover_letter': data.get('cover_letter', ''),
                'resume_url': data.get('resume_url', '')
            }
            
            result = job_controller.apply_to_job(job_id, applicant_id, application_data)
            
            if result['success']:
                return result, 201
            else:
                return {'error': result['error']}, 400
                
        except Exception as e:
            return {'error': 'Internal server error'}, 500
        finally:
            db.close()


api.add_resource(JobResource, '/api/jobs/<int:job_id>')
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(JobApplicationResource, '/api/jobs/<int:job_id>/apply')

if __name__ == '__main__':
    app.run(debug=True)
main
