from .base import BaseModel
from app import db
from sqlalchemy.orm import validates

class Attachment(BaseModel):
    __tablename__ = 'attachments'
    
    file_url = db.Column(db.String(255), nullable=False, comment='Cloudinary public_id or local file path')
    public_url = db.Column(db.String(512), nullable=True, comment='Publicly accessible URL for the file')
    filename = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(100), nullable=True)
    file_size = db.Column(db.Integer, nullable=True, comment='File size in bytes')
    
    # Foreign keys
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    bid_id = db.Column(db.Integer, db.ForeignKey('bids.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    job = db.relationship('Job', foreign_keys=[job_id], back_populates='job_documents')
    bid = db.relationship('Bid', foreign_keys=[bid_id], back_populates='bid_attachments')
    uploader = db.relationship('User', foreign_keys=[uploaded_by], back_populates='uploaded_attachments')
    user = db.relationship('User', foreign_keys=[user_id], back_populates='user_attachments')
    
    @validates('file_url')
    def validate_file_url(self, key, file_url):
        if not file_url:
            raise ValueError('File URL cannot be empty')
        return file_url
    
    def to_dict(self):
        """Convert the attachment to a dictionary."""
        return {
            'id': self.id,
            'file_url': self.file_url,
            'public_url': self.public_url,
            'filename': self.filename,
            'mime_type': self.mime_type,
            'file_size': self.file_size,
            'uploaded_at': self.created_at.isoformat() if self.created_at else None,
            'uploaded_by': self.uploader.to_dict() if self.uploader else None,
            'job_id': self.job_id,
            'bid_id': self.bid_id,
            'user_id': self.user_id
        }
    
    def get_download_url(self):
        """Get the download URL for this attachment."""
        from app import create_app
        from flask import current_app
        
        app = current_app or create_app()
        
        if app.config.get('STORAGE_PROVIDER') == 'cloudinary' and self.public_url:
            return self.public_url
        
        # Fallback to local file URL
        from flask import url_for
        return url_for('document.download_document', attachment_id=self.id, _external=True)
