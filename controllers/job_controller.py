from sqlalchemy.orm import Session
from models.job import Job
from models.user import User
from models.application import Application, ApplicationStatus
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Dict, Any, List
from models.skill import Skill
from sqlalchemy import or_, and_

class JobController:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def get_job_by_id(self, job_id: int) -> Optional[Dict[str, Any]]:
        """
        Get job by ID with associated client information
        """
        try:
            job = self.db.query(Job).filter(Job.id == job_id).first()
            if not job:
                return None
            
            return job.to_dict()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None
    
    def apply_to_job(self, job_id: int, applicant_id: int, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle job application logic
        """
        try:
            # Check if job exists and is open
            job = self.db.query(Job).filter(Job.id == job_id).first()
            if not job:
                return {'success': False, 'error': 'Job not found'}
            
            if job.status.value != 'open':
                return {'success': False, 'error': 'Job is not accepting applications'}
            
            # Check if user exists
            user = self.db.query(User).filter(User.id == applicant_id).first()
            if not user:
                return {'success': False, 'error': 'User not found'}
            
            # Check if user already applied
            existing_application = self.db.query(Application).filter(
                Application.job_id == job_id,
                Application.applicant_id == applicant_id
            ).first()
            
            if existing_application:
                return {'success': False, 'error': 'You have already applied to this job'}
            
            # Create new application
            new_application = Application(
                job_id=job_id,
                applicant_id=applicant_id,
                cover_letter=application_data.get('cover_letter', ''),
                resume_url=application_data.get('resume_url', ''),
                status=ApplicationStatus.PENDING
            )
            
            self.db.add(new_application)
            self.db.commit()
            
            return {
                'success': True,
                'message': 'Application submitted successfully',
                'application': new_application.to_dict()
            }
            
        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"Database error: {e}")
            return {'success': False, 'error': 'Database error occurred'}
    
    def search_jobs(self, search: str = None, skill: str = None, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """
        Search and filter jobs with optional skill filter and pagination
        """
        try:
            query = self.db.query(Job)
            
            if search:
                search_filter = "%{}%".format(search)
                query = query.filter(or_(
                    Job.title.ilike(search_filter),
                    Job.description.ilike(search_filter),
                    Job.requirements.ilike(search_filter)
                ))
            
            if skill:
                # Join with skills table if skill filter is provided
                query = query.join(Job.skills).filter(Skill.name.ilike(f"%{skill}%"))
            
            total = query.count()
            jobs = query.offset((page - 1) * limit).limit(limit).all()
            
            return {
                'total': total,
                'page': page,
                'limit': limit,
                'jobs': [job.to_dict() for job in jobs]
            }
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return {'error': 'Database error occurred'}
