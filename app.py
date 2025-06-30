from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from extensions import db, bcrypt, jwt
from routes.auth import auth_bp
from routes.users import users_bp
from resources.users import (
    UserResource,
    UserListResource,
    ChangePasswordResource,
    UserStatsResource,
    TokenVerificationResource,
    UserProfileResource,
    UserApplicationsResource,
    LogoutResource
)

from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173"],
          allow_headers=["Content-Type", "Authorization"],
          methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
          supports_credentials=True)
         
    db_path = os.path.join(os.getcwd(), "database", "instance", "dcbd.db")
    database_uri = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
        
    print(f"Current working directory: {os.getcwd()}")
    print(f"Database URI: {database_uri}")
            
    print(f"Database file exists: {os.path.exists(db_path)}")
    print(f"Database directory exists: {os.path.exists(os.path.dirname(db_path))}")
    db_dir = os.path.dirname(db_path)
    print(f"Database directory contents: {os.listdir(db_dir) if os.path.exists(db_dir) else 'Directory not found'}")
             
    print(f"Instance directory exists: {os.path.exists('instance')}")
    if os.path.exists('instance'):
        print(f"Instance directory permissions: {oct(os.stat('instance').st_mode)[-3:]}")
       
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Initialize Flask-RESTful API
    api = Api(app)
         
    # Register blueprints (existing routes)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)  
    
    # Register Flask-RESTful resources (new routes)
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(UserListResource, '/api/users')
    api.add_resource(ChangePasswordResource, '/api/users/change-password')
    api.add_resource(UserStatsResource, '/api/users/<int:user_id>/stats')
    api.add_resource(TokenVerificationResource, '/api/verify-token')
    api.add_resource(UserProfileResource, '/api/users/<int:user_id>/profile')
    api.add_resource(UserApplicationsResource, '/api/users/<int:user_id>/applications')
    api.add_resource(LogoutResource, '/api/logout')
             
    with app.app_context():
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        db.create_all()
     
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)