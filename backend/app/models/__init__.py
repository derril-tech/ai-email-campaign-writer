"""
Database models for the AI Email Campaign Writer application.
"""

from .user import User
from .campaign import Campaign, CampaignRecipient
from .recipient import Recipient, RecipientList, RecipientListMember
from .template import Template, TemplateVariable
from .analytics import CampaignAnalytics, UserAnalytics, EmailEvent
from .subscription import Subscription, Invoice
from .notification import Notification, NotificationTemplate

__all__ = [
    "User",
    "Campaign",
    "CampaignRecipient",
    "Recipient",
    "RecipientList",
    "RecipientListMember",
    "Template",
    "TemplateVariable",
    "CampaignAnalytics",
    "UserAnalytics",
    "EmailEvent",
    "Subscription",
    "Invoice",
    "Notification",
    "NotificationTemplate",
]
