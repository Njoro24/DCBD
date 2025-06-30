from extensions import db

# Define both association tables
job_skill_association = db.Table(
    'job_skill_association',
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'))
)

user_skills = db.Table(
    'user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'), primary_key=True)
)

class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    level = db.Column(db.String(50), nullable=True)  # Optional: used in Profile Page

    # Relationships
    jobs = db.relationship("Job", secondary=job_skill_association, back_populates="skills")
    users = db.relationship("User", secondary=user_skills, back_populates="skills")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level
        }
