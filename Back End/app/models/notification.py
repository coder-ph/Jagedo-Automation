from .base import BaseModel
from .enums import NotificationType
from app import db

class Notification(BaseModel):
    __tablename__ = 'notifications'
    
    content = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'content': self.content,
            'read': self.read,
            'notification_type': self.notification_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id
        }


class ProjectStatusHistory(BaseModel):
    __tablename__ = 'project_status_history'
    
    project_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    from_status = db.Column(db.Enum('open', 'in_progress', 'completed', 'awarded', name='job_status'), nullable=True)
    to_status = db.Column(db.Enum('open', 'in_progress', 'completed', 'awarded', name='job_status'), nullable=False)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notes = db.Column(db.Text)
    
    # Relationships
    changed_by_user = db.relationship('User')
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'from_status': self.from_status,
            'to_status': self.to_status,
            'changed_by': self.changed_by_user.to_dict() if self.changed_by_user else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
