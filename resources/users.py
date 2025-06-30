from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.user_controller import UserController
from extensions import db

class UserResource(Resource):
    def get(self, user_id):
        """
        GET /api/users/:id
        Get public user info (for job client details)
        """
        user_controller = UserController(db.session)  # Fixed: Added db.session
        
        try:
            user = user_controller.get_client_info(user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            # Return only public information
            public_user_info = {
                'id': user['id'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'company': user['company'],
                'position': user['position'],
                'bio': user['bio']
                # Email and phone are private
            }
            
            return public_user_info, 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500
    
    @jwt_required()
    def put(self, user_id):
        """
        PUT /api/users/:id
        Update user profile (only own profile)
        """
        user_controller = UserController(db.session)  # Fixed: Added db.session
        
        try:
            current_user_id = get_jwt_identity()
            
            # Users can only update their own profile
            if current_user_id != user_id:
                return {'error': 'Unauthorized to update this profile'}, 403
            
            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            # Remove sensitive fields that shouldn't be updated here
            sensitive_fields = ['id', 'password_hash', 'created_at']
            for field in sensitive_fields:
                data.pop(field, None)
            
            # Update user
            updated_user = user_controller.update_user(user_id, data)
            
            if updated_user:
                return {
                    'message': 'Profile updated successfully',
                    'user': updated_user
                }, 200
            else:
                return {'error': 'Failed to update profile'}, 500
                
        except Exception as e:
            return {'error': 'Internal server error'}, 500
    
    @jwt_required()
    def delete(self, user_id):
        """
        DELETE /api/users/:id
        Delete user account (only own account)
        """
        user_controller = UserController(db.session)  # Fixed: Added db.session
        
        try:
            current_user_id = get_jwt_identity()
            
            # Users can only delete their own account
            if current_user_id != user_id:
                return {'error': 'Unauthorized to delete this account'}, 403
            
            # Delete user
            success = user_controller.delete_user(user_id)
            
            if success:
                return {'message': 'Account deleted successfully'}, 200
            else:
                return {'error': 'Failed to delete account'}, 500
                
        except Exception as e:
            return {'error': 'Internal server error'}, 500

class UserListResource(Resource):
    @jwt_required()
    def get(self):
        """
        GET /api/users
        Get list of users (admin only or for search functionality)
        """
        user_controller = UserController(db.session)  # Fixed: Added db.session
        
        try:
            # Get query parameters for filtering/searching
            search = request.args.get('search', '')
            company = request.args.get('company', '')
            position = request.args.get('position', '')
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            users = user_controller.search_users(
                search=search,
                company=company,
                position=position,
                page=page,
                per_page=per_page
            )
            
            # Return only public information for each user
            public_users = []
            for user in users:
                public_user = {
                    'id': user['id'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'company': user['company'],
                    'position': user['position'],
                    'bio': user['bio']
                }
                public_users.append(public_user)
            
            return {
                'users': public_users
            }, 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500

class ChangePasswordResource(Resource):
    @jwt_required()
    def put(self):
        """
        PUT /api/users/change-password
        Change user password
        """
        from werkzeug.security import generate_password_hash, check_password_hash
        
        user_controller = UserController(db.session)  # Fixed: Added db.session
        
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            
            if not current_password or not new_password:
                return {'error': 'Current password and new password are required'}, 400
            
            # Get user with password hash
            user = user_controller.get_user_with_password(current_user_id)  # Fixed: Use method that includes password
            if not user:
                return {'error': 'User not found'}, 404
            
            # Verify current password
            if not check_password_hash(user['password_hash'], current_password):
                return {'error': 'Current password is incorrect'}, 400
            
            # Hash new password
            new_password_hash = generate_password_hash(new_password)
            
            # Update password
            success = user_controller.update_password(current_user_id, new_password_hash)
            
            if success:
                return {'message': 'Password changed successfully'}, 200
            else:
                return {'error': 'Failed to change password'}, 500
                
        except Exception as e:
            return {'error': 'Internal server error'}, 500

class UserStatsResource(Resource):
    @jwt_required()
    def get(self, user_id):
        """
        GET /api/users/:id/stats
        Get user statistics (jobs posted, applications sent, etc.)
        """
        user_controller = UserController(db.session)  # Fixed: Added db.session
        
        try:
            current_user_id = get_jwt_identity()
            
           
            if current_user_id == user_id:
                stats = user_controller.get_user_detailed_stats(user_id)
            else:
                stats = user_controller.get_user_public_stats(user_id)
            
            if stats:
                return stats, 200
            else:
                return {'error': 'User not found'}, 404
                
        except Exception as e:
            return {'error': 'Internal server error'}, 500

class TokenVerificationResource(Resource):
    @jwt_required()
    def get(self):
        """
        GET /api/verify-token
        Verify if the current token is valid
        """
        user_controller = UserController(db.session)  # Fixed: Added db.session
        
        try:
            current_user_id = get_jwt_identity()
            user = user_controller.get_user_by_id(current_user_id)
            
            if user:
                return {
                    'valid': True,
                    'user_id': current_user_id,
                    'first_name': user.get('first_name'),
                    'last_name': user.get('last_name'),
                    'email': user.get('email')
                }, 200
            else:
                return {'valid': False, 'message': 'User not found'}, 404
                
        except Exception as e:
            return {'valid': False, 'message': 'Invalid token'}, 401

class UserProfileResource(Resource):
    @jwt_required()
    def get(self, user_id):
        """
        GET /api/users/:id/profile
        Get complete user profile (own profile only)
        """
        user_controller = UserController(db.session)  # Fixed: Added db.session
        
        try:
            current_user_id = get_jwt_identity()
            
            # Users can only access their own complete profile
            if current_user_id != user_id:
                return {'error': 'Unauthorized access'}, 403
                
            user = user_controller.get_user_by_id(user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
            # Return complete profile information (excluding sensitive data)
            profile_data = {
                'id': user['id'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'phone': user.get('phone'),
                'company': user.get('company'),
                'position': user.get('position'),
                'bio': user.get('bio'),
                'created_at': user.get('created_at')
            }
            
            return profile_data, 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500

class UserApplicationsResource(Resource):
    @jwt_required()
    def get(self, user_id):
        """
        GET /api/users/:id/applications
        Get user's job applications
        """
        user_controller = UserController(db.session)  # Fixed: Added db.session
        
        try:
            current_user_id = get_jwt_identity()
            
            # Users can only access their own applications
            if current_user_id != user_id:
                return {'error': 'Unauthorized access'}, 403
                
            # Get applications for the user
            applications = user_controller.get_user_applications(user_id)
            
            if applications is not None:
                return applications, 200
            else:
                return {'error': 'User not found or no applications'}, 404
                
        except Exception as e:
            return {'error': 'Internal server error'}, 500

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        """
        POST /api/logout
        Logout user (token blacklisting could be implemented here)
        """
        try:
            # In a full implementation, you might want to blacklist the token
            # For now, just return success - the frontend will remove the token
            return {'message': 'Logged out successfully'}, 200
            
        except Exception as e:
            return {'error': 'Internal server error'}, 500