from datetime import datetime
import enum
from extensions import db

class ApplicationStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cover_letter = db.Column(db.Text)
    status = db.Column(db.Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    job = db.relationship('Job', back_populates='applications')
    applicant = db.relationship('User', back_populates='applications')

    def to_dict(self):
        return {
            "id": self.id,
            "job_id": self.job_id,
            "applicant_id": self.applicant_id,
            "cover_letter": self.cover_letter,
            "status": self.status.value if self.status else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
