"""
Pydantic schemas for request/response validation.
"""

from .user import *
from .campaign import *
from .recipient import *
from .template import *
from .analytics import *
from .subscription import *
from .notification import *
from .auth import *
from .common import *

__all__ = [
    # User schemas
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserList",
    
    # Campaign schemas
    "CampaignCreate",
    "CampaignUpdate",
    "CampaignResponse",
    "CampaignList",
    "CampaignStats",
    
    # Recipient schemas
    "RecipientCreate",
    "RecipientUpdate",
    "RecipientResponse",
    "RecipientList",
    "RecipientListCreate",
    "RecipientListUpdate",
    "RecipientListResponse",
    
    # Template schemas
    "TemplateCreate",
    "TemplateUpdate",
    "TemplateResponse",
    "TemplateList",
    
    # Analytics schemas
    "CampaignAnalyticsResponse",
    "UserAnalyticsResponse",
    "EmailEventResponse",
    
    # Subscription schemas
    "SubscriptionCreate",
    "SubscriptionResponse",
    "InvoiceResponse",
    
    # Notification schemas
    "NotificationCreate",
    "NotificationResponse",
    "NotificationList",
    
    # Auth schemas
    "LoginRequest",
    "RegisterRequest",
    "TokenResponse",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    
    # Common schemas
    "ApiResponse",
    "PaginatedResponse",
    "ErrorResponse",
]
