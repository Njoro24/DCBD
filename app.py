from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, jwt
from routes.auth import auth_bp
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configuration
    # Use absolute path for SQLite database
    db_path = os.path.join(os.getcwd(), "database", "instance", "dcbd.db")
    database_uri = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

    # Debug information
    print(f"Current working directory: {os.getcwd()}")
    print(f"Database URI: {database_uri}")
    
    # Check if database file exists
    print(f"Database file exists: {os.path.exists(db_path)}")
    print(f"Database directory exists: {os.path.exists(os.path.dirname(db_path))}")
    db_dir = os.path.dirname(db_path)
    print(f"Database directory contents: {os.listdir(db_dir) if os.path.exists(db_dir) else 'Directory not found'}")
    
    # Check instance directory
    print(f"Instance directory exists: {os.path.exists('instance')}")
    if os.path.exists('instance'):
        print(f"Instance directory permissions: {oct(os.stat('instance').st_mode)[-3:]}")

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)

    # Create database tables if they don't exist
    with app.app_context():
        # Ensure database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)