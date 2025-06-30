from flask import request
from models.user import User
from extensions import db
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError

def register_user():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not all([name, email, password, role]):
        return {"error": "All fields are required"}, 400

    if len(password) < 6:
        return {"error": "Password must be at least 6 characters"}, 400

    user = User(name=name, email=email, role=role)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email already exists"}, 409

    access_token = create_access_token(identity=user.id)
    return {
        "access_token": access_token,
        "user": user.to_dict()
    }, 201


def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return {"error": "Email and password are required"}, 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {"error": "Invalid credentials"}, 401

    access_token = create_access_token(identity=user.id)
    return {
        "access_token": access_token,
        "user": user.to_dict()
    }, 200


def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found"}, 404

    return {"user": user.to_dict()}, 200
