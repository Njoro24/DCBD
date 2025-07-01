from extensions import db

# Import all models — ORDER MATTERS
from .user import User
from .skill import Skill  # Must come before job so skills table exists
from .job import Job
from .application import Application

__all__ = ["User", "Skill", "Job", "Application", "db"]
