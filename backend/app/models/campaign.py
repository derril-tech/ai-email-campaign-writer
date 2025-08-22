"""
Campaign model for email campaign management.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer, JSON, Enum, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
import uuid

from app.core.database import Base

class CampaignStatus(str, enum.Enum):
    """Campaign status enumeration"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"

class CampaignType(str, enum.Enum):
    """Campaign type enumeration"""
    WELCOME = "welcome"
    NEWSLETTER = "newsletter"
    PROMOTIONAL = "promotional"
    ABANDONED_CART = "abandoned_cart"
    RE_ENGAGEMENT = "re_engagement"
    CUSTOM = "custom"

class Campaign(Base):
    """Campaign model for email campaign management"""
    
    __tablename__ = "campaigns"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    audience_id = Column(UUID(as_uuid=True), ForeignKey("audiences.id"), nullable=True)
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id"), nullable=True)
    
    # Basic campaign info
    name = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    preview_text = Column(String(255), nullable=True)
    
    # Content
    html_content = Column(Text, nullable=True)
    text_content = Column(Text, nullable=True)
    
    # Campaign settings
    campaign_type = Column(Enum(CampaignType), default=CampaignType.CUSTOM, nullable=False)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT, nullable=False)
    
    # Sending settings
    from_name = Column(String(255), nullable=False)
    from_email = Column(String(255), nullable=False)
    reply_to = Column(String(255), nullable=True)
    
    # Scheduling
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    
    # Campaign settings
    settings = Column(JSON, nullable=True)  # {
        # tracking_enabled: bool,
        # unsubscribe_enabled: bool,
        # resend_to_unopened: bool,
        # resend_delay_hours: int,
        # a_b_testing: bool,
        # a_b_test_percentage: int
    # }
    
    # Analytics
    recipient_count = Column(Integer, default=0, nullable=False)
    sent_count = Column(Integer, default=0, nullable=False)
    delivered_count = Column(Integer, default=0, nullable=False)
    opened_count = Column(Integer, default=0, nullable=False)
    clicked_count = Column(Integer, default=0, nullable=False)
    bounced_count = Column(Integer, default=0, nullable=False)
    unsubscribed_count = Column(Integer, default=0, nullable=False)
    spam_reports = Column(Integer, default=0, nullable=False)
    
    # Calculated metrics
    delivery_rate = Column(Float, default=0.0, nullable=False)
    open_rate = Column(Float, default=0.0, nullable=False)
    click_rate = Column(Float, default=0.0, nullable=False)
    bounce_rate = Column(Float, default=0.0, nullable=False)
    unsubscribe_rate = Column(Float, default=0.0, nullable=False)
    
    # AI generation info
    ai_generated = Column(Boolean, default=False, nullable=False)
    ai_generation_id = Column(UUID(as_uuid=True), ForeignKey("ai_generations.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="campaigns")
    audience = relationship("Audience", back_populates="campaigns")
    template = relationship("Template", back_populates="campaigns")
    ai_generation = relationship("AIGeneration", back_populates="campaigns")
    email_sends = relationship("EmailSend", back_populates="campaign", cascade="all, delete-orphan")
    email_events = relationship("EmailEvent", back_populates="campaign", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Campaign(id={self.id}, name='{self.name}', status='{self.status}')>"
    
    @property
    def is_sent(self) -> bool:
        """Check if campaign has been sent"""
        return self.status == CampaignStatus.SENT
    
    @property
    def is_scheduled(self) -> bool:
        """Check if campaign is scheduled"""
        return self.status == CampaignStatus.SCHEDULED
    
    @property
    def is_draft(self) -> bool:
        """Check if campaign is in draft status"""
        return self.status == CampaignStatus.DRAFT
    
    @property
    def can_be_sent(self) -> bool:
        """Check if campaign can be sent"""
        return (
            self.status in [CampaignStatus.DRAFT, CampaignStatus.SCHEDULED] and
            self.recipient_count > 0 and
            self.html_content is not None
        )
    
    @property
    def progress_percentage(self) -> float:
        """Get campaign sending progress percentage"""
        if self.recipient_count == 0:
            return 0.0
        return (self.sent_count / self.recipient_count) * 100
    
    def update_analytics(self):
        """Update calculated analytics metrics"""
        if self.recipient_count > 0:
            self.delivery_rate = (self.delivered_count / self.recipient_count) * 100
            self.open_rate = (self.opened_count / self.delivered_count) * 100 if self.delivered_count > 0 else 0
            self.click_rate = (self.clicked_count / self.opened_count) * 100 if self.opened_count > 0 else 0
            self.bounce_rate = (self.bounced_count / self.recipient_count) * 100
            self.unsubscribe_rate = (self.unsubscribed_count / self.recipient_count) * 100
    
    def get_analytics_summary(self) -> dict:
        """Get campaign analytics summary"""
        return {
            "recipient_count": self.recipient_count,
            "sent_count": self.sent_count,
            "delivered_count": self.delivered_count,
            "opened_count": self.opened_count,
            "clicked_count": self.clicked_count,
            "bounced_count": self.bounced_count,
            "unsubscribed_count": self.unsubscribed_count,
            "spam_reports": self.spam_reports,
            "delivery_rate": self.delivery_rate,
            "open_rate": self.open_rate,
            "click_rate": self.click_rate,
            "bounce_rate": self.bounce_rate,
            "unsubscribe_rate": self.unsubscribe_rate,
            "progress_percentage": self.progress_percentage
        }


class CampaignRecipient(Base):
    """Campaign recipient model for tracking individual recipients."""
    
    __tablename__ = "campaign_recipients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=False)
    recipient_id = Column(UUID(as_uuid=True), ForeignKey("recipients.id"), nullable=False)
    
    # Delivery status
    status = Column(String(20), default="pending", nullable=False)  # pending, sent, delivered, opened, clicked, bounced, unsubscribed
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)
    opened_at = Column(DateTime, nullable=True)
    clicked_at = Column(DateTime, nullable=True)
    bounced_at = Column(DateTime, nullable=True)
    unsubscribed_at = Column(DateTime, nullable=True)
    
    # Tracking
    open_count = Column(Integer, default=0, nullable=False)
    click_count = Column(Integer, default=0, nullable=False)
    last_opened_at = Column(DateTime, nullable=True)
    last_clicked_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="recipients")
    recipient = relationship("Recipient", back_populates="campaigns")
    
    def __repr__(self) -> str:
        return f"<CampaignRecipient(campaign_id={self.campaign_id}, recipient_id={self.recipient_id})>"
