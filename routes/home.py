from flask import Blueprint, jsonify
from app import db 
from models.job import Job
from models.user import User


home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/api/jobs/featured', methods=['GET'])
def get_featured_jobs():
  
        jobs = Job.query.limit(3).all()

    
        result = []

        for job in jobs:
            client_name = job.client.name if job.client else "Unknown Company"

            
            result.append({
                "id": job.id,
                "title": job.title,
                "company": client_name,       
                "budget": f"${job.budget:.2f}", 
                "description": job.description,
                "posted_on": job.created_at.strftime('%Y-%m-%d') 
            })

      
        return jsonify(result), 200

    except Exception as e:
        print(f"Error fetching featured jobs: {e}")
        return jsonify({"error": "An internal server error occurred. Could not retrieve featured jobs."}), 500

