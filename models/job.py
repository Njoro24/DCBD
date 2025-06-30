from extensions import db
from datetime import datetime
import enum

from .skill import job_skill_association  # Import association table

class JobStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    PAUSED = "paused"

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    salary_min = db.Column(db.Float)
    salary_max = db.Column(db.Float)
    location = db.Column(db.String(200))
    job_type = db.Column(db.String(50))  # full-time, part-time, contract, etc.
    status = db.Column(db.Enum(JobStatus), default=JobStatus.OPEN)
    is_featured = db.Column(db.Boolean, default=False)

    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client = db.relationship("User", back_populates="posted_jobs")
    applications = db.relationship("Application", back_populates="job")
    skills = db.relationship("Skill", secondary=job_skill_association, back_populates="jobs")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'location': self.location,
            'job_type': self.job_type,
            'status': self.status.value if self.status else None,
            'client_id': self.client_id,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'skills': [skill.to_dict() for skill in self.skills] if self.skills else []
        }
