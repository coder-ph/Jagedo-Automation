from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
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
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default='KES')
    status = Column(db.Enum(PaymentStatus), default=PaymentStatus.PENDING)
    method = Column(db.Enum(PaymentMethod), nullable=False)
    reference = Column(String(100), unique=True, nullable=False)
    mpesa_receipt = Column(String(50), nullable=True)
    phone_number = Column(String(20), nullable=True)
    payment_metadata = Column('metadata', JSONB, default={})  # Using payment_metadata as the attribute name to avoid conflict
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', back_populates='payments')
    project = relationship('Project', back_populates='payments')
    
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
