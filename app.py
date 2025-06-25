from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os

# Import route classes
from routes.jobs import RegisterResource, LoginResource, RefreshResource, ProfileResource
from routes.jobs import (
    JobResource, JobListResource, JobApplicationResource, 
    MyJobsResource, MyApplicationsResource, JobApplicationsResource
)
from routes.users import (
    UserResource, UserListResource, ChangePasswordResource, 
    UserStatsResource
)

def create_app():
    # Create Flask app instance
    app = Flask(__name__)

    # Enable CORS (Cross-Origin Resource Sharing)
    CORS(app)

    # JWT configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    # Initialize JWT Manager
    jwt = JWTManager(app)

    # Initialize Flask-RESTful API
    api = Api(app)

    # ----------------- Register API Routes ------------------

    # Auth routes
    api.add_resource(RegisterResource, '/api/auth/register')
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(RefreshResource, '/api/auth/refresh')
    api.add_resource(ProfileResource, '/api/auth/profile')

    # Job routes
    api.add_resource(JobListResource, '/api/jobs')
    api.add_resource(JobResource, '/api/jobs/<int:job_id>')
    api.add_resource(JobApplicationResource, '/api/jobs/<int:job_id>/apply')
    api.add_resource(JobApplicationsResource, '/api/jobs/<int:job_id>/applications')
    api.add_resource(MyJobsResource, '/api/jobs/my-jobs')
    api.add_resource(MyApplicationsResource, '/api/jobs/my-applications')

    # User routes
    api.add_resource(UserListResource, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(ChangePasswordResource, '/api/users/<int:user_id>/change-password')
    api.add_resource(UserStatsResource, '/api/users/<int:user_id>/stats')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
