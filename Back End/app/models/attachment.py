from .base import BaseModel
from app import db

class Attachment(BaseModel):
    __tablename__ = 'attachments'
    
    file_url = db.Column(db.String(255), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    bid_id = db.Column(db.Integer, db.ForeignKey('bids.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    job = db.relationship('Job', foreign_keys=[job_id], back_populates='job_documents')
    bid = db.relationship('Bid', foreign_keys=[bid_id], back_populates='bid_attachments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'file_url': self.file_url,
            'filename': self.filename,
            'uploaded_at': self.created_at.isoformat() if self.created_at else None,
            'uploaded_by': self.uploader.to_dict() if self.uploader else None,
            'job_id': self.job_id,
            'bid_id': self.bid_id,
            'user_id': self.user_id
        }
