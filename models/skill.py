
from extensions import db

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    jobs = db.relationship("Job", secondary="job_skill_association", back_populates="skills")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
