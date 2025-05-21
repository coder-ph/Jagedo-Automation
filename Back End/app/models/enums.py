from enum import Enum, auto

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

class NotificationType(str, Enum):
    BID_RECEIVED = 'bid_received'
    BID_ACCEPTED = 'bid_accepted'
    BID_REJECTED = 'bid_rejected'
    PROJECT_AWARDED = 'project_awarded'
    PROJECT_COMPLETED = 'project_completed'
    MESSAGE_RECEIVED = 'message_received'
