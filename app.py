from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models.user import Base
from datetime import datetime
import enum

class ApplicationStatus(enum.Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class Application(Base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    applicant_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    cover_letter = Column(Text)
    resume_url = Column(String(500))
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    notes = Column(Text)
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", back_populates="applications")
    applicant = relationship("User", back_populates="applications")
    
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