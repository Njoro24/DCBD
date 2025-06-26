from extensions import db
from datetime import datetime



class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    budget = db.Column(db.Float)
    is_featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='open')  # open, closed, in_progress
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert Job object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'client_id': self.client_id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'budget': self.budget,
            'is_featured': self.is_featured,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
