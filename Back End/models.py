from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class UserRole(str, Enum):
    CUSTOMER = 'customer'
    PROFESSIONAL = 'professional'
    ADMIN = 'admin'

class JobStatus(str, Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    AWARDED = 'awarded'

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
    nca_level = db.Column(db.Integer, default=1)
    average_rating = db.Column(db.Float, default=0.0)
    total_ratings = db.Column(db.Integer, default=0)
    successful_bids = db.Column(db.Integer, default=0)
    total_bids = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships where user is the customer
    jobs = db.relationship('Job', foreign_keys='Job.customer_id', backref=db.backref('customer', lazy='joined'))
    
    # Relationships where user is the professional
    bids = db.relationship('Bid', backref=db.backref('professional', lazy='joined'))
    skills = db.relationship('ProfessionalSkill', backref=db.backref('professional', lazy='joined'))
    notifications = db.relationship('Notification', backref=db.backref('user', lazy='joined'))
    
    # Relationships where user is the assigned contractor
    assigned_jobs = db.relationship('Job', foreign_keys='Job.assigned_contractor_id', backref=db.backref('assigned_contractor', lazy='joined'))

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
    assigned_contractor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    budget = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = db.relationship('Category', backref=db.backref('jobs', lazy=True))
    bids = db.relationship('Bid', backref=db.backref('job', lazy='joined'), 
                          foreign_keys='Bid.job_id')
    job_documents = db.relationship('Attachment', 
                                  foreign_keys='Attachment.job_id',
                                  backref=db.backref('job_doc', lazy='joined'),
                                  lazy=True)
    reviews = db.relationship('Review', 
                            foreign_keys='Review.job_id',
                            backref=db.backref('job', lazy='joined'),
                            lazy=True)

class Bid(db.Model):
    __tablename__ = 'bids'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    proposal = db.Column(db.Text, nullable=False)
    timeline_weeks = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(BidStatus), default=BidStatus.PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    location_score = db.Column(db.Float, nullable=True)
    location_match_type = db.Column(db.String(50), nullable=True)

    # Relationships
    job_rel = db.relationship('Job', foreign_keys=[job_id], back_populates='bids')
    professional_rel = db.relationship('User', foreign_keys=[professional_id])
    bid_related_attachments = db.relationship('Attachment', 
                                           foreign_keys='Attachment.bid_id',
                                           backref=db.backref('related_bid', lazy='joined'),
                                           lazy=True)
    
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
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    bid_id = db.Column(db.Integer, db.ForeignKey('bids.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    uploader = db.relationship('User', foreign_keys=[uploaded_by], backref=db.backref('uploaded_attachments', lazy=True))
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('user_attachments', lazy=True))
    job_rel = db.relationship('Job', foreign_keys=[job_id], backref=db.backref('job_attachments', lazy=True))
    bid_rel = db.relationship('Bid', foreign_keys=[bid_id], backref=db.backref('bid_attachments', lazy=True))

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50))
    

class ProjectStatusHistory(db.Model):
    __tablename__ = 'project_status_history'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    from_status = db.Column(db.Enum(JobStatus), nullable=False)
    to_status = db.Column(db.Enum(JobStatus), nullable=False)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    project = db.relationship('Job', backref='status_history')
    changed_by_user = db.relationship('User')