from .base import BaseModel
from app import db

class Message(BaseModel):
    __tablename__ = 'messages'
    
    message = db.Column(db.Text, nullable=False)
    read_at = db.Column(db.DateTime)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    
    # Relationships
    job = db.relationship('Job', backref='messages')
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sender': self.sender.to_dict() if self.sender else None,
            'receiver': self.receiver.to_dict() if self.receiver else None,
            'job_id': self.job_id
        }


class Review(BaseModel):
    __tablename__ = 'reviews'
    
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), unique=True, nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('job_id', 'professional_id', name='uq_job_professional_review'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'job_id': self.job_id,
            'professional': self.professional.to_dict() if self.professional else None,
            'customer': self.customer.to_dict() if self.customer else None
        }
