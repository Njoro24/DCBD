from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
cors = CORS()

def create_app():
    app= Flask(__name__)
    app.config.from_object(Config)
    CORS

    db.init_app(app)
    cors.init_app(app)

    from routes.home import home_bp
    app.register_blueprint(home_bp)

    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context(): 
        db.create_all()
    app.run(debug=True)





