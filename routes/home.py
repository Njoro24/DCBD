from flask import Blueprint, jsonify
from models.job import Job
from models.user import User
from app import db

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('api/jobs/featured', methods=['GET'])
def get_featured_jobs():

    