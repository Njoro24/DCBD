from extensions import db

# Define the association table here (before Job or Skill uses it)
job_skill_association = db.Table(
    'job_skill_association',
    db.Column('job_id', db.Integer, db.ForeignKey('jobs.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skills.id'))
)

class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    jobs = db.relationship("Job", secondary=job_skill_association, back_populates="skills")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
