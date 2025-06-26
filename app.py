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
    app = create_app()
    app.run(debug=True)
