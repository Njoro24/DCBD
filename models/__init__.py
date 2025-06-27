# Import db so it is available in this module
from extensions import db

# Import all models
from .user import User
from .job import Job

# Export all models and db
__all__ = ["User", "Job", "db"]
