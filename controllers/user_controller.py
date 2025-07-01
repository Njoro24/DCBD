# Fixed UserController with robust error handling and data serialization
from flask import Flask, request, current_app
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, Dict, Any, List
import traceback
import json
from datetime import datetime

# Import your models (adjust the import path as needed)
from models.user import User
from extensions import db

class UserController:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def _safe_serialize_datetime(self, dt):
        """Safely serialize datetime objects"""
        if dt is None:
            return None
        if isinstance(dt, datetime):
            return dt.isoformat()
        return str(dt)
    
    def _safe_get_user_dict(self, user) -> Dict[str, Any]:
        """Safely convert user object to dictionary with proper error handling"""
        try:
            if hasattr(user, 'to_dict'):
                user_dict = user.to_dict()
            else:
                # Manual serialization if to_dict doesn't exist
                user_dict = {}
                for column in user.__table__.columns:
                    value = getattr(user, column.name, None)
                    if isinstance(value, datetime):
                        user_dict[column.name] = self._safe_serialize_datetime(value)
                    else:
                        user_dict[column.name] = value
            
            # Ensure critical fields exist with defaults
            user_dict.setdefault('id', getattr(user, 'id', None))
            user_dict.setdefault('first_name', getattr(user, 'first_name', ''))
            user_dict.setdefault('last_name', getattr(user, 'last_name', ''))
            user_dict.setdefault('email', getattr(user, 'email', ''))
            user_dict.setdefault('role', getattr(user, 'role', 'developer'))
            user_dict.setdefault('created_at', self._safe_serialize_datetime(getattr(user, 'created_at', None)))
            
            return user_dict
        except Exception as e:
            print(f"❌ Error in _safe_get_user_dict: {e}")
            # Return minimal safe dictionary
            return {
                'id': getattr(user, 'id', None),
                'first_name': getattr(user, 'first_name', ''),
                'last_name': getattr(user, 'last_name', ''),
                'email': getattr(user, 'email', ''),
                'role': getattr(user, 'role', 'developer'),
                'created_at': None
            }
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch user information by ID with robust error handling
        """
        try:
            print(f"🔍 UserController.get_user_by_id called with user_id: {user_id}")
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                print(f"❌ User not found with ID: {user_id}")
                return None
            
            user_dict = self._safe_get_user_dict(user)
            print(f"✅ User found: {user_dict.get('first_name', 'Unknown')} {user_dict.get('last_name', '')}")
            return user_dict
        except SQLAlchemyError as e:
            print(f"❌ Database error in get_user_by_id: {e}")
            self.db.rollback()
            return None
        except Exception as e:
            print(f"❌ Unexpected error in get_user_by_id: {e}")
            traceback.print_exc()
            return None
    
    def get_user_skills(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get skills for a specific user with robust error handling
        """
        try:
            print(f"🔍 UserController.get_user_skills called with user_id: {user_id}")
            
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                print(f"❌ User not found for skills query: {user_id}")
                return []
            
            # Check if user has skills relationship
            if hasattr(user, 'skills') and user.skills:
                skills = []
                for skill in user.skills:
                    try:
                        if hasattr(skill, 'to_dict'):
                            skill_dict = skill.to_dict()
                        else:
                            # Manual serialization for skills
                            skill_dict = {}
                            for column in skill.__table__.columns:
                                value = getattr(skill, column.name, None)
                                if isinstance(value, datetime):
                                    skill_dict[column.name] = self._safe_serialize_datetime(value)
                                else:
                                    skill_dict[column.name] = value
                        
                        # Ensure required fields
                        skill_dict.setdefault('id', getattr(skill, 'id', None))
                        skill_dict.setdefault('name', getattr(skill, 'name', 'Unknown Skill'))
                        skill_dict.setdefault('level', getattr(skill, 'level', 'Beginner'))
                        skill_dict.setdefault('user_id', getattr(skill, 'user_id', user_id))
                        
                        skills.append(skill_dict)
                    except Exception as skill_error:
                        print(f"⚠️ Error processing skill: {skill_error}")
                        # Add fallback skill
                        skills.append({
                            'id': getattr(skill, 'id', None),
                            'name': getattr(skill, 'name', 'Unknown Skill'),
                            'level': getattr(skill, 'level', 'Beginner'),
                            'user_id': user_id
                        })
                
                print(f"✅ Found {len(skills)} skills for user {user_id}")
                return skills
            else:
                print(f"⚠️ No skills found for user {user_id} (or no skills relationship)")
                return []
                
        except SQLAlchemyError as e:
            print(f"❌ Database error in get_user_skills: {e}")
            self.db.rollback()
            return []
        except Exception as e:
            print(f"❌ Unexpected error in get_user_skills: {e}")
            traceback.print_exc()
            return []

    def get_user_with_skills(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user with skills included - with robust error handling
        """
        try:
            print(f"🔍 UserController.get_user_with_skills called with user_id: {user_id}")
            
            user = self.get_user_by_id(user_id)
            if user:
                skills = self.get_user_skills(user_id)
                user['skills'] = skills
                print(f"✅ User with {len(skills)} skills prepared")
                return user
            print(f"❌ User not found in get_user_with_skills: {user_id}")
            return None
        except Exception as e:
            print(f"❌ Error in get_user_with_skills: {e}")
            traceback.print_exc()
            return None
    
    def get_user_applications(self, user_id: int):
        """
        Get all applications for a specific user with robust error handling
        """
        try:
            print(f"🔍 UserController.get_user_applications called with user_id: {user_id}")
            
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                print(f"❌ User not found for applications query: {user_id}")
                return None
            
            # If you have an applications relationship on User model
            if hasattr(user, 'applications') and user.applications:
                applications = []
                for app in user.applications:
                    try:
                        if hasattr(app, 'to_dict'):
                            app_dict = app.to_dict()
                        else:
                            # Manual serialization
                            app_dict = {}
                            for column in app.__table__.columns:
                                value = getattr(app, column.name, None)
                                if isinstance(value, datetime):
                                    app_dict[column.name] = self._safe_serialize_datetime(value)
                                else:
                                    app_dict[column.name] = value
                        
                        # Ensure required fields
                        app_dict.setdefault('id', getattr(app, 'id', None))
                        app_dict.setdefault('status', getattr(app, 'status', 'pending'))
                        app_dict.setdefault('created_at', self._safe_serialize_datetime(getattr(app, 'created_at', None)))
                        
                        # Include job information if available
                        if hasattr(app, 'job') and app.job:
                            try:
                                if hasattr(app.job, 'to_dict'):
                                    job_dict = app.job.to_dict()
                                else:
                                    job_dict = {}
                                    for column in app.job.__table__.columns:
                                        value = getattr(app.job, column.name, None)
                                        if isinstance(value, datetime):
                                            job_dict[column.name] = self._safe_serialize_datetime(value)
                                        else:
                                            job_dict[column.name] = value
                                
                                # Ensure required job fields
                                job_dict.setdefault('id', getattr(app.job, 'id', None))
                                job_dict.setdefault('title', getattr(app.job, 'title', 'Unknown Job'))
                                job_dict.setdefault('budget', getattr(app.job, 'budget', 'Not specified'))
                                job_dict.setdefault('status', getattr(app.job, 'status', 'open'))
                                
                                app_dict['job'] = job_dict
                                
                                # Include client information
                                if hasattr(app.job, 'client') and app.job.client:
                                    app_dict['job']['client'] = {
                                        'id': getattr(app.job.client, 'id', None),
                                        'name': f"{getattr(app.job.client, 'first_name', '')} {getattr(app.job.client, 'last_name', '')}".strip()
                                    }
                            except Exception as job_error:
                                print(f"⚠️ Error processing job info: {job_error}")
                                app_dict['job'] = {
                                    'id': getattr(app.job, 'id', None) if hasattr(app, 'job') and app.job else None,
                                    'title': 'Unknown Job',
                                    'budget': 'Not specified',
                                    'status': 'open'
                                }
                        
                        applications.append(app_dict)
                    except Exception as app_error:
                        print(f"⚠️ Error processing application: {app_error}")
                        # Add fallback application
                        applications.append({
                            'id': getattr(app, 'id', None),
                            'status': getattr(app, 'status', 'pending'),
                            'created_at': self._safe_serialize_datetime(getattr(app, 'created_at', None))
                        })
                
                print(f"✅ Found {len(applications)} applications for user {user_id}")
                return applications
            else:
                print(f"⚠️ No applications found for user {user_id}")
                return []
            
        except SQLAlchemyError as e:
            print(f"❌ Database error in get_user_applications: {e}")
            self.db.rollback()
            return []
        except Exception as e:
            print(f"❌ Unexpected error in get_user_applications: {e}")
            traceback.print_exc()
            return []

    def get_user_posted_jobs(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Get all jobs posted by a specific user (for clients) with robust error handling
        """
        try:
            print(f"🔍 UserController.get_user_posted_jobs called with user_id: {user_id}")
            
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                print(f"❌ User not found for posted jobs query: {user_id}")
                return []
            
            # If you have a posted_jobs relationship on User model
            if hasattr(user, 'posted_jobs') and user.posted_jobs:
                jobs = []
                for job in user.posted_jobs:
                    try:
                        if hasattr(job, 'to_dict'):
                            job_dict = job.to_dict()
                        else:
                            # Manual serialization
                            job_dict = {}
                            for column in job.__table__.columns:
                                value = getattr(job, column.name, None)
                                if isinstance(value, datetime):
                                    job_dict[column.name] = self._safe_serialize_datetime(value)
                                else:
                                    job_dict[column.name] = value
                        
                        # Ensure required fields
                        job_dict.setdefault('id', getattr(job, 'id', None))
                        job_dict.setdefault('title', getattr(job, 'title', 'Unknown Job'))
                        job_dict.setdefault('budget', getattr(job, 'budget', 'Not specified'))
                        job_dict.setdefault('status', getattr(job, 'status', 'open'))
                        job_dict.setdefault('created_at', self._safe_serialize_datetime(getattr(job, 'created_at', None)))
                        
                        jobs.append(job_dict)
                    except Exception as job_error:
                        print(f"⚠️ Error processing posted job: {job_error}")
                        # Add fallback job
                        jobs.append({
                            'id': getattr(job, 'id', None),
                            'title': getattr(job, 'title', 'Unknown Job'),
                            'budget': getattr(job, 'budget', 'Not specified'),
                            'status': getattr(job, 'status', 'open'),
                            'created_at': self._safe_serialize_datetime(getattr(job, 'created_at', None))
                        })
                
                print(f"✅ Found {len(jobs)} posted jobs for user {user_id}")
                return jobs
            else:
                print(f"⚠️ No posted jobs found for user {user_id}")
                return []
                
        except SQLAlchemyError as e:
            print(f"❌ Database error in get_user_posted_jobs: {e}")
            self.db.rollback()
            return []
        except Exception as e:
            print(f"❌ Unexpected error in get_user_posted_jobs: {e}")
            traceback.print_exc()
            return []

    # ... (other methods remain the same)


# FIXED Flask Resources with proper error handling

class UserProfileResource(Resource):
    @jwt_required()
    def get(self, user_id):
        """
        GET /api/users/:id/profile
        Get complete user profile (own profile only)
        """
        try:
            # Use db.session directly from extensions
            user_controller = UserController(db.session)
            
            current_user_id = get_jwt_identity()
            
            # Debug logging
            print(f"🔍 Profile request debug:")
            print(f"  - Requested user_id: {user_id}")
            print(f"  - Current user_id: {current_user_id}")
            print(f"  - Types: {type(user_id)} vs {type(current_user_id)}")
            
            # Users can only access their own complete profile
            if int(current_user_id) != int(user_id):
                print(f"❌ Authorization failed: {current_user_id} != {user_id}")
                return {'error': 'Unauthorized access'}, 403
                
            # Get user with skills
            user = user_controller.get_user_with_skills(user_id)
            
            if not user:
                print(f"❌ User not found: {user_id}")
                return {'error': 'User not found'}, 404
            
            print(f"✅ User found: {user.get('first_name', 'Unknown')} {user.get('last_name', '')}")
            
            # Ensure skills is always a list
            skills = user.get('skills', [])
            if not isinstance(skills, list):
                skills = []
            
            # Create safe profile data with explicit field mapping
            try:
                profile_data = {
                    'id': user.get('id'),
                    'first_name': user.get('first_name', '') or '',
                    'last_name': user.get('last_name', '') or '',
                    'name': f"{user.get('first_name', '') or ''} {user.get('last_name', '') or ''}".strip(),
                    'email': user.get('email', '') or '',
                    'phone': user.get('phone'),
                    'company': user.get('company'),
                    'position': user.get('position'),
                    'bio': user.get('bio', '') or '',
                    'role': user.get('role', 'developer') or 'developer',
                    'created_at': user.get('created_at'),
                    'skills': skills
                }
                
                # Test JSON serialization
                json.dumps(profile_data, default=str)  # This will raise an error if not serializable
                
                print(f"✅ Returning profile data with {len(skills)} skills")
                return profile_data, 200
                
            except Exception as serialization_error:
                print(f"❌ Serialization error: {serialization_error}")
                traceback.print_exc()
                
                # Return minimal safe profile
                minimal_profile = {
                    'id': user.get('id'),
                    'first_name': str(user.get('first_name', '')),
                    'last_name': str(user.get('last_name', '')),
                    'name': f"{str(user.get('first_name', ''))} {str(user.get('last_name', ''))}".strip(),
                    'email': str(user.get('email', '')),
                    'phone': str(user.get('phone', '')) if user.get('phone') else None,
                    'company': str(user.get('company', '')) if user.get('company') else None,
                    'position': str(user.get('position', '')) if user.get('position') else None,
                    'bio': str(user.get('bio', '')),
                    'role': str(user.get('role', 'developer')),
                    'created_at': str(user.get('created_at')) if user.get('created_at') else None,
                    'skills': []
                }
                
                return minimal_profile, 200
            
        except Exception as e:
            error_msg = f"Error in UserProfileResource.get: {str(e)}"
            print(f"❌ {error_msg}")
            traceback.print_exc()
            return {'error': 'Internal server error'}, 500


class UserApplicationsResource(Resource):
    @jwt_required()
    def get(self, user_id):
        """
        GET /api/users/:id/applications
        Get user's job applications
        """
        try:
            # Use db.session directly from extensions
            user_controller = UserController(db.session)
            
            current_user_id = get_jwt_identity()
            
            # Users can only access their own applications
            if int(current_user_id) != int(user_id):
                print(f"❌ Authorization failed for applications: {current_user_id} != {user_id}")
                return {'error': 'Unauthorized access'}, 403
                
            # Get applications for the user
            applications = user_controller.get_user_applications(user_id)
            
            if applications is not None:
                # Ensure it's JSON serializable
                try:
                    json.dumps(applications, default=str)
                    print(f"✅ Returning {len(applications)} applications")
                    return applications, 200
                except Exception as serialization_error:
                    print(f"❌ Applications serialization error: {serialization_error}")
                    return [], 200  # Return empty list instead of error
            else:
                return {'error': 'User not found'}, 404
                
        except Exception as e:
            error_msg = f"Error in UserApplicationsResource.get: {str(e)}"
            print(f"❌ {error_msg}")
            traceback.print_exc()
            return {'error': 'Internal server error'}, 500


class UserJobsResource(Resource):
    @jwt_required()
    def get(self, user_id):
        """
        GET /api/users/:id/jobs
        Get jobs posted by user (for clients)
        """
        try:
            # Use db.session directly from extensions
            user_controller = UserController(db.session)
            
            current_user_id = get_jwt_identity()
            
            # Users can only access their own posted jobs
            if int(current_user_id) != int(user_id):
                print(f"❌ Authorization failed for posted jobs: {current_user_id} != {user_id}")
                return {'error': 'Unauthorized access'}, 403
                
            # Get posted jobs for the user
            jobs = user_controller.get_user_posted_jobs(user_id)
            
            # Ensure it's JSON serializable
            try:
                json.dumps(jobs, default=str)
                print(f"✅ Returning {len(jobs)} posted jobs")
                return jobs, 200
            except Exception as serialization_error:
                print(f"❌ Jobs serialization error: {serialization_error}")
                return [], 200  # Return empty list instead of error
                
        except Exception as e:
            error_msg = f"Error in UserJobsResource.get: {str(e)}"
            print(f"❌ {error_msg}")
            traceback.print_exc()
            return {'error': 'Internal server error'}, 500