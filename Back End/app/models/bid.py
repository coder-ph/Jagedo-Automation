from .base import BaseModel
from .enums import BidStatus
from app import db

class Bid(BaseModel):
    __tablename__ = 'bids'
    
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    proposal = db.Column(db.Text, nullable=False)
    timeline_weeks = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(BidStatus), default=BidStatus.PENDING, nullable=False)
    location_score = db.Column(db.Float, nullable=True)
    location_match_type = db.Column(db.String(50), nullable=True)
    
    # Relationships
    job = db.relationship('Job', foreign_keys=[job_id], back_populates='bids')
    professional = db.relationship('User', foreign_keys=[professional_id], back_populates='bids')
    bid_attachments = db.relationship('Attachment', 
                                     foreign_keys='Attachment.bid_id',
                                     back_populates='bid',
                                     lazy=True)
    team_members = db.relationship('BidTeamMember', back_populates='bid', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('job_id', 'professional_id', name='uq_job_professional'),
    )
    
    def to_dict(self, include_details=False):
        result = {
            'id': self.id,
            'amount': float(self.amount) if self.amount is not None else None,
            'proposal': self.proposal,
            'timeline_weeks': self.timeline_weeks,
            'status': self.status.value if self.status else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'professional': self.professional.to_dict() if self.professional else None,
            'location_score': float(self.location_score) if self.location_score is not None else None,
            'location_match_type': self.location_match_type
        }
        
        if include_details:
            result.update({
                'attachments': [doc.to_dict() for doc in self.bid_attachments],
                'team_members': [member.to_dict() for member in self.team_members]
            })
            
        return result


class BidTeamMember(BaseModel):
    __tablename__ = 'bid_team_members'
    
    bid_id = db.Column(db.Integer, db.ForeignKey('bids.id', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    hours = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relationships
    bid = db.relationship('Bid', back_populates='team_members')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate is not None else None,
            'hours': float(self.hours) if self.hours is not None else None,
            'total_cost': float(self.total_cost) if self.total_cost is not None else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
