from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, jwt
from routes.auth import auth_bp
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)  #  fixed __name__
    CORS(app)

    basedir = os.path.abspath(os.path.dirname(__file__))  # fixed __file__

    # Ensure the 'instance' folder exists
    os.makedirs(os.path.join(basedir, "instance"), exist_ok=True)

    # Load DB URI from env and handle SQLite relative paths
    db_uri = os.getenv("DATABASE_URL")
    if db_uri and db_uri.startswith("sqlite:///") and not db_uri.startswith("sqlite:////"):
        rel_path = db_uri.replace("sqlite:///", "")
        abs_path = os.path.join(basedir, rel_path)
        db_uri = f"sqlite:///{abs_path}"
    elif not db_uri:
        db_uri = f"sqlite:///{os.path.join(basedir, 'instance', 'devconnect.db')}"

    # App config
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

    return app

# Entry point
if __name__ == "__main__":  # fixed __name__
    app = create_app()
    with app.app_context():
        db.create_all()  # Dev-only: auto-create tables
    app.run(debug=True)
