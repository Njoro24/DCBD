from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

db = SQLAlchemy()

class ApplicationStatus(enum.Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cover_letter = db.Column(db.Text)
    resume_url = db.Column(db.String(500))
    status = db.Column(db.Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    notes = db.Column(db.Text)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = db.relationship("Job", back_populates="applications")
    applicant = db.relationship("User", back_populates="applications")
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'applicant_id': self.applicant_id,
            'cover_letter': self.cover_letter,
            'resume_url': self.resume_url,
            'status': self.status.value if self.status else None,
            'notes': self.notes,
            'applied_at': self.applied_at.isoformat() if self.applied_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'job': self.job.to_dict() if self.job else None,
            'applicant': self.applicant.to_dict() if self.applicant else None
        }