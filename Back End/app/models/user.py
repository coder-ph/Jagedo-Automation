from werkzeug.security import generate_password_hash, check_password_hash
from .base import BaseModel
from .enums import UserRole
from app.extensions import db

class User(BaseModel):
    __tablename__ = 'users'
    
    role = db.Column(db.Enum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column('password', db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    company_name = db.Column(db.String(255))
    profile_description = db.Column(db.Text)
    location = db.Column(db.String(255), nullable=False)
    nca_level = db.Column(db.Integer, default=1)
    average_rating = db.Column(db.Float, default=0.0)
    total_ratings = db.Column(db.Integer, default=0)
    successful_bids = db.Column(db.Integer, default=0)
    total_bids = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    business_name = db.Column(db.String(255))
    business_description = db.Column(db.Text)
    business_address = db.Column(db.String(500))
    business_phone = db.Column(db.String(20))
    business_website = db.Column(db.String(255))
    business_logo = db.Column(db.String(500))
    business_banner = db.Column(db.String(500))

    # Relationships where user is the customer
    jobs = db.relationship('Job', foreign_keys='Job.customer_id', backref=db.backref('customer', lazy='joined'))
    
    # Relationships where user is the professional
    bids = db.relationship('Bid', back_populates='professional')
    skills = db.relationship('ProfessionalSkill', backref=db.backref('professional', lazy='joined'))
    notifications = db.relationship('Notification', backref=db.backref('user', lazy='joined'))
    
    # Relationships where user is the assigned contractor
    assigned_jobs = db.relationship('Job', foreign_keys='Job.assigned_contractor_id', backref=db.backref('assigned_contractor', lazy='joined'))
    
    # Relationships for messages
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)
    
    # Relationships for reviews
    reviews_received = db.relationship('Review', foreign_keys='Review.professional_id', backref='professional', lazy=True)
    reviews_given = db.relationship('Review', foreign_keys='Review.customer_id', backref='customer', lazy=True)
    
    # Relationships for attachments
    uploaded_attachments = db.relationship(
        'Attachment',
        foreign_keys='Attachment.uploaded_by',
        back_populates='uploader',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    user_attachments = db.relationship(
        'Attachment',
        foreign_keys='Attachment.user_id',
        back_populates='user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    # Relationships for payments
    payments = db.relationship('PaymentTransaction', back_populates='user')
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Set the password with hashing."""
        self._password = generate_password_hash(password)
    
    def verify_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self._password, password)
    
    @classmethod
    def create(cls, **kwargs):
        """Create a new user with hashed password."""
        if 'password' in kwargs:
            password = kwargs.pop('password')
            user = cls(**kwargs)
            user.password = password
            return user
        return cls(**kwargs)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'company_name': self.company_name if hasattr(self, 'company_name') else None,
            'role': self.role.value if hasattr(self, 'role') and self.role else None,
            'location': self.location if hasattr(self, 'location') else None,
            'phone': self.phone if hasattr(self, 'phone') else None,
            'is_verified': bool(self.is_verified) if hasattr(self, 'is_verified') and self.is_verified is not None else False,
            'is_active': bool(self.is_active) if hasattr(self, 'is_active') and self.is_active is not None else True,
            'average_rating': float(self.average_rating) if hasattr(self, 'average_rating') and self.average_rating is not None else 0.0,
            'total_ratings': int(self.total_ratings) if hasattr(self, 'total_ratings') and self.total_ratings is not None else 0,
            'successful_bids': int(self.successful_bids) if hasattr(self, 'successful_bids') and self.successful_bids is not None else 0,
            'total_bids': int(self.total_bids) if hasattr(self, 'total_bids') and self.total_bids is not None else 0,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') and self.created_at else None,
            'updated_at': self.updated_at.isoformat() if hasattr(self, 'updated_at') and self.updated_at else None,
            'profile_description': self.profile_description if hasattr(self, 'profile_description') else None,
            'nca_level': self.nca_level if hasattr(self, 'nca_level') else None,
            'business_name': self.business_name if hasattr(self, 'business_name') else None,
            'business_description': self.business_description if hasattr(self, 'business_description') else None,
            'business_address': self.business_address if hasattr(self, 'business_address') else None,
            'business_phone': self.business_phone if hasattr(self, 'business_phone') else None,
            'business_website': self.business_website if hasattr(self, 'business_website') else None
        }
