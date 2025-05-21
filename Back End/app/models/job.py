from datetime import datetime
from .base import BaseModel
from .enums import JobStatus, PaymentStatus
from app import db
from ..utils.helpers import generate_reference

class Job(BaseModel):
    __tablename__ = 'jobs'
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(JobStatus), default=JobStatus.OPEN, nullable=False)
    payment_status = db.Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    payment_reference = db.Column(db.String(50), unique=True, nullable=True)
    payment_date = db.Column(db.DateTime, nullable=True)
    assigned_contractor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    budget = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relationships
    category = db.relationship('Category', backref=db.backref('jobs', lazy=True))
    bids = db.relationship('Bid', back_populates='job', 
                         foreign_keys='Bid.job_id',
                         lazy='joined')
    job_documents = db.relationship('Attachment',
                                  foreign_keys='Attachment.job_id',
                                  back_populates='job',
                                  lazy=True)
    reviews = db.relationship('Review', 
                            foreign_keys='Review.job_id',
                            backref=db.backref('job', lazy='joined'),
                            lazy=True)
    status_history = db.relationship('ProjectStatusHistory', backref='project')
    payments = db.relationship('PaymentTransaction', back_populates='project')
    
    def mark_as_paid(self):
        """Mark the job as paid and update relevant fields."""
        self.payment_status = PaymentStatus.COMPLETED
        self.payment_date = datetime.utcnow()
        if not self.payment_reference:
            self.payment_reference = f"PAY-{generate_reference()}"
        if self.status == JobStatus.PENDING_PAYMENT:
            self.status = JobStatus.ACTIVE
        db.session.commit()

    def create_payment_intent(self, amount=None):
        """Create a payment intent for this job."""
        from ..services.payment_service import payment_service
        
        if not amount:
            amount = float(self.budget)
            
        # Create a payment record
        payment = payment_service.create_payment_record(
            user_id=self.customer_id,
            amount=amount,
            job_id=self.id,
            method='mpesa',
            description=f'Payment for job #{self.id}'
        )
        
        # Update job with payment reference
        self.payment_reference = payment.reference
        self.payment_status = PaymentStatus.PENDING
        db.session.commit()
        
        return payment

    def to_dict(self, include_details=False):
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'status': self.status.value if self.status else None,
            'payment_status': self.payment_status.value if self.payment_status else None,
            'payment_reference': self.payment_reference,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'budget': float(self.budget) if self.budget is not None else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'customer': self.customer.to_dict() if self.customer else None,
            'category': {
                'id': self.category.id,
                'name': self.category.name
            } if self.category else None
        }
        
        if include_details:
            result.update({
                'bids': [bid.to_dict() for bid in self.bids],
                'assigned_contractor': self.assigned_contractor.to_dict() if self.assigned_contractor else None,
                'documents': [doc.to_dict() for doc in self.job_documents],
                'reviews': [review.to_dict() for review in self.reviews],
                'status_history': [history.to_dict() for history in self.status_history]
            })
            
        return result
