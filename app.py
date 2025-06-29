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

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Ensure the 'instance' folder exists
    os.makedirs(os.path.join(basedir, "instance"), exist_ok=True)

    # Load DB URI from env and safely resolve relative SQLite path
    db_uri = os.getenv("DATABASE_URL")
    if db_uri and db_uri.startswith("sqlite:///") and not db_uri.startswith("sqlite:////"):
        # Convert relative SQLite path to absolute path
        rel_path = db_uri.replace("sqlite:///", "")
        abs_path = os.path.join(basedir, rel_path)
        db_uri = f"sqlite:///{abs_path}"
    elif not db_uri:
        # Fallback default
        db_uri = f"sqlite:///{os.path.join(basedir, 'instance', 'devconnect.db')}"

    # Apply config
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "supersecret")
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "superjwt")

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)

    # Import models to register them with SQLAlchemy before creating tables
    from models.user import User
    from models.job import Job
    from models.skill import Skill

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # Only for development use
    app.run(debug=True)
