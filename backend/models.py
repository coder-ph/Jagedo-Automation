from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class UserRole(str, Enum):
    CUSTOMER = 'customer'
    PROFESSIONAL = 'professional'

class JobStatus(str, Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

class BidStatus(str, Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255))
    profile_description = db.Column(db.Text)
    location = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    jobs = db.relationship('Job', backref='customer')
    bids = db.relationship('Bid', backref='professional')
    skills = db.relationship('ProfessionalSkill', backref='professional')

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role.value,
            'email': self.email,
            'name': self.name
        }

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(JobStatus), default=JobStatus.OPEN, nullable=False)
    budget = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship('Category', backref='jobs')
    bids = db.relationship('Bid', backref='job')

class Bid(db.Model):
    __tablename__ = 'bids'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    proposed_timeline = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(BidStatus), default=BidStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('job_id', 'professional_id', name='uq_job_professional'),
    )

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    parent = db.relationship('Category', remote_side=[id], backref='children')

class ProfessionalSkill(db.Model):
    __tablename__ = 'professional_skills'
    
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)
    certified = db.Column(db.Boolean, default=False)
    years_experience = db.Column(db.Integer)
    nca_ratings = db.Column(db.String(255))

class Skill(db.Model):
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), unique=True, nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))

class Attachment(db.Model):
    __tablename__ = 'attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    bid_id = db.Column(db.Integer, db.ForeignKey('bids.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)