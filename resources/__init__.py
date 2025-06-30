# resources/__init__.py
"""
Resources package for Flask RESTful API endpoints.

This package contains all the Flask-RESTful resource classes
that handle API endpoints for the application.
"""

from .users import (
    UserResource,
    UserListResource,
    ChangePasswordResource,
    UserStatsResource,
    TokenVerificationResource,
    UserProfileResource,
    UserApplicationsResource,
    LogoutResource
)

__all__ = [
    'UserResource',
    'UserListResource',
    'ChangePasswordResource',
    'UserStatsResource',
    'TokenVerificationResource',
    'UserProfileResource',
    'UserApplicationsResource',
    'LogoutResource'
]

__version__ = '1.0.0'
__author__ = 'Your Name'