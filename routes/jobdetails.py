from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from controllers.job_controller import JobController
from controllers.user_controller import UserController
from controllers.skill_controller import SkillController
import os

# Create blueprint
job_details_bp = Blueprint('job_details', __name__)

# Database setup (you'll need to configure this with your actual database)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///jobs.db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@job_details_bp.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """
    GET /api/jobs/:id
    Get job by ID with client information
    """
    db = get_db()
    job_controller = JobController(db)
    
    try:
        job = job_controller.get_job_by_id(job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify(job), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        db.close()

@job_details_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    GET /api/users/:id
    Fetch client info associated with a job
    """
    db = get_db()
    user_controller = UserController(db)
    
    try:
        user = user_controller.get_client_info(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        db.close()

@job_details_bp.route('/api/jobs/<int:job_id>/apply', methods=['POST'])
def apply_to_job(job_id):
    """
    POST /api/jobs/:id/apply
    Handle job application logic
    """
    db = get_db()
    job_controller = JobController(db)
    
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        applicant_id = data.get('applicant_id')
        if not applicant_id:
            return jsonify({'error': 'Applicant ID is required'}), 400
        
        # Prepare application data
        application_data = {
            'cover_letter': data.get('cover_letter', ''),
            'resume_url': data.get('resume_url', '')
        }
        
        # Apply to job
        result = job_controller.apply_to_job(job_id, applicant_id, application_data)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify({'error': result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        db.close()

@job_details_bp.route('/api/jobs', methods=['GET'])
def search_jobs():
    """
    GET /api/jobs
    Search and filter jobs with optional skill filter and pagination
    Query params: search, skill, page, limit
    """
    db = get_db()
    job_controller = JobController(db)
    
    try:
        search = request.args.get('search')
        skill = request.args.get('skill')
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)
        
        result = job_controller.search_jobs(search=search, skill=skill, page=page, limit=limit)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        db.close()

@job_details_bp.route('/api/skills', methods=['GET'])
def get_skills():
    """
    GET /api/skills
    Get all skills
    """
    db = get_db()
    skill_controller = SkillController(db)
    
    try:
        skills = skill_controller.get_all_skills()
        return jsonify(skills), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        db.close()
