from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.user import Base

class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    
    jobs = relationship("Job", secondary="job_skill_association", back_populates="skills")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
