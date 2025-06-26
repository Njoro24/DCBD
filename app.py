kibet
from flask import Flask
from extensions import db
from models.user import User
from models.job import Job
from models.client import Client

# ✅ Import the jobs blueprint
from routes.jobs import jobs_bp

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devconnect.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)

    # ✅ Register blueprints
    app.register_blueprint(jobs_bp)

    # Create tables within application context
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")
    
    return app

# For running directly
if __name__ == '__main__':

# app.py

from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, jwt
from routes.auth import auth_bp
from dotenv import load_dotenv
import os

from routes.jobs import RegisterResource, LoginResource, RefreshResource, ProfileResource, JobListResource

feature/profile-endpoints
# Import route classes

from routes.jobs import (
    JobResource, JobListResource, JobApplicationResource, 
    MyJobsResource, MyApplicationsResource, JobApplicationsResource
)
from routes.users import (
    UserResource, UserListResource, ChangePasswordResource, 
    UserStatsResource
)
=======
#  Load environment variables
load_dotenv()
main

def create_app():
    app = Flask(__name__)
    CORS(app)

    #  Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///instance/devconnect.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    #  Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    #  Register Blueprints
    app.register_blueprint(auth_bp)

    return app

if __name__ == "__main__":
main
    app = create_app()
    app.run(debug=True)
