from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Enum, Float, Table
from sqlalchemy.orm import relationship
from models.user import Base
from datetime import datetime
import enum

# Association table for many-to-many relationship between jobs and skills
job_skill_association = Table(
    'job_skill_association',
    Base.metadata,
    Column('job_id', Integer, ForeignKey('jobs.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

class JobStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    PAUSED = "paused"

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    salary_min = Column(Float)
    salary_max = Column(Float)
    location = Column(String(200))
    job_type = Column(String(50))  # full-time, part-time, contract, etc.
    status = Column(Enum(JobStatus), default=JobStatus.OPEN)
    client_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship("User", back_populates="posted_jobs")
    applications = relationship("Application", back_populates="job")
    skills = relationship("Skill", secondary=job_skill_association, back_populates="jobs")
    
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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'client': self.client.to_dict() if self.client else None,
            'skills': [skill.to_dict() for skill in self.skills] if self.skills else []
        }
