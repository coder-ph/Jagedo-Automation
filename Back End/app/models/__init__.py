from ..extensions import db

# Import all models to ensure they are registered with SQLAlchemy
from .base import BaseModel
from .user import User, UserRole
from .job import Job, JobStatus
from .bid import Bid, BidStatus, BidTeamMember
from .message import Message, Review
from .notification import Notification, ProjectStatusHistory
from .category import Category, Skill, ProfessionalSkill
from .attachment import Attachment
from .payment import PaymentTransaction, PaymentStatus, PaymentMethod

# Import enums
from .enums import UserRole, JobStatus, BidStatus, NotificationType

__all__ = [
    'db',
    'BaseModel',
    'User', 'UserRole',
    'Job', 'JobStatus',
    'Bid', 'BidStatus', 'BidTeamMember',
    'Message', 'Review',
    'Notification', 'ProjectStatusHistory',
    'Category', 'Skill', 'ProfessionalSkill',
    'Attachment',
    'PaymentTransaction', 'PaymentStatus', 'PaymentMethod',
    'UserRole', 'JobStatus', 'BidStatus', 'NotificationType'
]