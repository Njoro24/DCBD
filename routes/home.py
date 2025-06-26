from flask import Blueprint, jsonify
from app import db # Import the db instance to perform database queries
from models.job import Job # Import the Job model
from models.user import User # Import the User model to access client names

# Create a Blueprint instance.
# 'home_bp' is the name of this blueprint. Blueprints help organize routes
# and other Flask components into modular, reusable sections.
home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/api/jobs/featured', methods=['GET'])
def get_featured_jobs():
    """
    API endpoint to retrieve a list of featured jobs.

    This route handles GET requests to '/api/jobs/featured'.
    It queries the database for the first 3 job listings and returns
    them as a JSON array, including details like title, company name,
    budget, description, and post date.
    """
    try:
        # Query the Job model to retrieve the first 3 jobs.
        # .limit(3): Restricts the query to return only the first 3 records.
        # .all(): Executes the query and returns a list of Job objects.
        jobs = Job.query.limit(3).all()

        # Prepare an empty list to store the formatted job data.
        result = []

        # Iterate through each Job object retrieved from the database.
        for job in jobs:
            # Safely get the client's name using the 'client' backref.
            # The 'client' attribute is created by the db.relationship in the User model.
            client_name = job.client.name if job.client else "Unknown Company"

            # Append a dictionary representing the job details to the result list.
            result.append({
                "id": job.id,
                "title": job.title,
                "company": client_name,         # Display the name of the client/company
                "budget": f"${job.budget:.2f}", # Format budget as currency (e.g., $1200.00)
                "description": job.description,
                "posted_on": job.created_at.strftime('%Y-%m-%d') # Format date as YYYY-MM-DD
            })

        # Return the formatted list of jobs as a JSON response.
        # jsonify() serializes the Python list/dict to JSON format.
        # The second argument '200' sets the HTTP status code to OK.
        return jsonify(result), 200

    except Exception as e:
        # Basic error handling: Catches any unexpected exceptions during the process.
        # In a production environment, you would:
        # 1. Log the full traceback for debugging (e.g., using app.logger.error(e)).
        # 2. Return a more generic and less revealing error message to the client
        #    to prevent exposing sensitive server details.
        print(f"Error fetching featured jobs: {e}")
        return jsonify({"error": "An internal server error occurred. Could not retrieve featured jobs."}), 500

# Additional routes can be defined within this blueprint, e.g.:
# @home_bp.route('/api/jobs/<int:job_id>', methods=['GET'])
# def get_job_details(job_id):
#     # Logic to fetch and return details for a specific job by its ID
#     pass
