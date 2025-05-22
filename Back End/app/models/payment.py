from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

class PaymentStatus(PyEnum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class PaymentMethod(PyEnum):
    MPESA = 'mpesa'
    CARD = 'card'
    BANK_TRANSFER = 'bank_transfer'

class PaymentTransaction(db.Model):
    __tablename__ = 'payment_transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('jobs.id'), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default='KES')
    status = Column(db.Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    method = Column(db.Enum(PaymentMethod), nullable=True)
    reference = Column(String(100), unique=True, nullable=False)
    mpesa_receipt = Column(String(50), nullable=True)
    phone_number = Column(String(20), nullable=True)
    payment_metadata = Column('metadata', JSON, default=dict)  # Using JSON instead of JSONB for SQLite compatibility
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='payments')
    project = relationship('Job', back_populates='payments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status.value,
            'method': self.method.value,
            'reference': self.reference,
            'mpesa_receipt': self.mpesa_receipt,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'metadata': self.payment_metadata  # Using the renamed attribute
        }
