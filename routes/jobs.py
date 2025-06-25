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