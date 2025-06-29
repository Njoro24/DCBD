from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialize extensions without an app instance
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
