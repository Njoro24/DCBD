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
            client_info['total_jobs_posted'] = len(user.posted_jobs) if hasattr(user, 'posted_jobs') and user.posted_jobs else 0
            
            return client_info
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None

    def update_user(self, user_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update user information
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            # Update user attributes
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            self.db.commit()
            return user.to_dict()
            
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            self.db.rollback()
            return None

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            self.db.delete(user)
            self.db.commit()
            return True
            
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            self.db.rollback()
            return False

    def search_users(self, search: str = "", company: str = "", position: str = "", page: int = 1, per_page: int = 10):
        """
        Search for users with filters
        """
        try:
            query = self.db.query(User)
            
            if search:
                search_filter = f"%{search}%"
                query = query.filter(
                    (User.first_name.ilike(search_filter)) |
                    (User.last_name.ilike(search_filter)) |
                    (User.email.ilike(search_filter))
                )
            
            if company:
                query = query.filter(User.company.ilike(f"%{company}%"))
            
            if position:
                query = query.filter(User.position.ilike(f"%{position}%"))
            
            # Pagination
            offset = (page - 1) * per_page
            users = query.offset(offset).limit(per_page).all()
            
            return [user.to_dict() for user in users]
            
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return []

    def get_user_applications(self, user_id: int):
        """
        Get all applications for a specific user
        Note: This assumes you have an Application model. Adjust as needed.
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            # If you have an applications relationship on User model
            if hasattr(user, 'applications'):
                return [app.to_dict() for app in user.applications]
            
            # If no applications model exists yet, return empty list
            return []
            
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return []

    def get_user_with_password(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user including password hash (for password verification)
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            user_dict = user.to_dict()
            # Add password hash if it exists
            if hasattr(user, 'password_hash'):
                user_dict['password_hash'] = user.password_hash
            
            return user_dict
            
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None

    def update_password(self, user_id: int, new_password_hash: str) -> bool:
        """
        Update user password
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            user.password_hash = new_password_hash
            self.db.commit()
            return True
            
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            self.db.rollback()
            return False

    def get_user_detailed_stats(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed statistics for a user (own profile)
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            stats = {
                'user_id': user_id,
                'total_applications': len(user.applications) if hasattr(user, 'applications') else 0,
                'total_jobs_posted': len(user.posted_jobs) if hasattr(user, 'posted_jobs') else 0,
                'profile_completed': True if user.bio and user.company else False
            }
            
            return stats
            
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None

    def get_user_public_stats(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get public statistics for a user
        """
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            stats = {
                'user_id': user_id,
                'total_jobs_posted': len(user.posted_jobs) if hasattr(user, 'posted_jobs') else 0,
                'member_since': user.created_at if hasattr(user, 'created_at') else None
            }
            
            return stats
            
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return None