from enum import Enum, auto

class UserRole(str, Enum):
    CUSTOMER = 'customer'
    PROFESSIONAL = 'professional'
    ADMIN = 'admin'

class JobStatus(str, Enum):
    OPEN = 'open'                    # Job is open for bidding
    PENDING_PAYMENT = 'pending_payment'  # Bid accepted, waiting for payment
    ACTIVE = 'active'                # Payment received, job is active
    IN_PROGRESS = 'in_progress'      # Work has started
    COMPLETED = 'completed'          # Job is completed
    CANCELLED = 'cancelled'          # Job was cancelled
    AWARDED = 'awarded'              # Bid has been awarded (pre-payment)

class BidStatus(str, Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

class PaymentStatus(str, Enum):
    PENDING = 'pending'              # Payment initiated but not completed
    COMPLETED = 'completed'          # Payment successfully completed
    FAILED = 'failed'                # Payment failed
    CANCELLED = 'cancelled'          # Payment was cancelled by user
    REFUNDED = 'refunded'            # Payment was refunded
    EXPIRED = 'expired'              # Payment link/request expired

class NotificationType(str, Enum):
    BID_RECEIVED = 'bid_received'
    BID_ACCEPTED = 'bid_accepted'
    BID_REJECTED = 'bid_rejected'
    PROJECT_AWARDED = 'project_awarded'
    PROJECT_COMPLETED = 'project_completed'
    MESSAGE_RECEIVED = 'message_received'
    PAYMENT_RECEIVED = 'payment_received'
    PAYMENT_FAILED = 'payment_failed'
    PAYMENT_REMINDER = 'payment_reminder'
