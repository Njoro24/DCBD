from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.user_controller import UserController
from database import get_db

class UserResource(Resource):
    def get(self, user_id):
   
        db = get_db()
        user_controller = UserController(db)
        
        try:
            user = user_controller.get_client_info(user_id)
            
            if not user:
                return {'error': 'User not found'}, 404
            
        
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
        finally:
            db.close()
    
    @jwt_required()
    def put(self, user_id):
        """
        PUT /api/users/:id
        Update user profile (only own profile)
        """
        db = get_db()
        user_controller = UserController(db)
        
        try:
            current_user_id = get_jwt_identity()
            
            
            if current_user_id != user_id:
                return {'error': 'Unauthorized to update this profile'}, 403
            
            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400
            
        
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
        finally:
            db.close()
    
    @jwt_required()
    def delete(self, user_id):
        """
        DELETE /api/users/:id
        Delete user account (only own account)
        """
        db = get_db()
        user_controller = UserController(db)
        
        try:
            current_user_id = get_jwt_identity()
            
        
            if current_user_id != user_id:
                return {'error': 'Unauthorized to delete this account'}, 403
            
        
            success = user_controller.delete_user(user_id)
            
            if success:
                return {'message': 'Account deleted successfully'}, 200
            else:
                return {'error': 'Failed to delete account'}, 500
                
        except Exception as e:
            return {'error': 'Internal server error'}, 500
        finally:
            db.close()

class UserListResource(Resource):
    @jwt_required()
    def get(self):
        """
        GET /api/users
        Get list of users (admin only or for search functionality)
        """
        db = get_db()
        user_controller = UserController(db)
        
        try:
    
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
        finally:
            db.close()

class ChangePasswordResource(Resource):
    @jwt_required()
    def put(self):
        """
        PUT /api/users/change-password
        Change user password
        """
        from werkzeug.security import generate_password_hash, check_password_hash
        
        db = get_db()
        user_controller = UserController(db)
        
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            
            if not current_password or not new_password:
                return {'error': 'Current password and new password are required'}, 400
            
            # Get user
            user = user_controller.get_user_by_id(current_user_id)
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
        finally:
            db.close()

class UserStatsResource(Resource):
    @jwt_required()
    def get(self, user_id):
        """
        GET /api/users/:id/stats
        Get user statistics (jobs posted, applications sent, etc.)
        """
        db = get_db()
        user_controller = UserController(db)
        
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
        finally:
            db.close()
