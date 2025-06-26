from sqlalchemy.orm import Session
from models.user import User
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Dict, Any

class UserController:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch user information by ID
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            return user.to_dict()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None
    
    def get_client_info(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch client information associated with a job
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            # Return client-specific information
            client_info = user.to_dict()
            # Add additional client-specific fields if needed
            client_info['total_jobs_posted'] = len(user.posted_jobs) if user.posted_jobs else 0
            
            return client_info
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None