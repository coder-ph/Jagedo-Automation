from .base import BaseModel
from .enums import JobStatus
from app import db

class Job(BaseModel):
    __tablename__ = 'jobs'
    
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum(JobStatus), default=JobStatus.OPEN, nullable=False)
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
    
    def to_dict(self, include_details=False):
        result = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'status': self.status.value if self.status else None,
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
