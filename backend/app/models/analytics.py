"""
Analytics model for tracking campaign performance and user analytics.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base


class CampaignAnalytics(Base):
    """Campaign analytics model for tracking campaign performance."""
    
    __tablename__ = "campaign_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=False)
    
    # Delivery statistics
    total_sent = Column(Integer, default=0, nullable=False)
    total_delivered = Column(Integer, default=0, nullable=False)
    total_bounced = Column(Integer, default=0, nullable=False)
    total_opened = Column(Integer, default=0, nullable=False)
    total_clicked = Column(Integer, default=0, nullable=False)
    total_unsubscribed = Column(Integer, default=0, nullable=False)
    total_complained = Column(Integer, default=0, nullable=False)
    
    # Rate calculations
    delivery_rate = Column(Float, default=0.0, nullable=False)
    open_rate = Column(Float, default=0.0, nullable=False)
    click_rate = Column(Float, default=0.0, nullable=False)
    bounce_rate = Column(Float, default=0.0, nullable=False)
    unsubscribe_rate = Column(Float, default=0.0, nullable=False)
    complaint_rate = Column(Float, default=0.0, nullable=False)
    
    # Engagement metrics
    unique_opens = Column(Integer, default=0, nullable=False)
    unique_clicks = Column(Integer, default=0, nullable=False)
    total_clicks = Column(Integer, default=0, nullable=False)
    
    # Geographic and device data
    geographic_data = Column(JSON, default=dict, nullable=False)
    device_data = Column(JSON, default=dict, nullable=False)
    client_data = Column(JSON, default=dict, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="analytics")
    
    def __repr__(self) -> str:
        return f"<CampaignAnalytics(campaign_id={self.campaign_id})>"
    
    def calculate_rates(self) -> None:
        """Calculate all rate metrics."""
        if self.total_sent > 0:
            self.delivery_rate = (self.total_delivered / self.total_sent) * 100
            self.open_rate = (self.unique_opens / self.total_delivered) * 100 if self.total_delivered > 0 else 0
            self.click_rate = (self.unique_clicks / self.total_delivered) * 100 if self.total_delivered > 0 else 0
            self.bounce_rate = (self.total_bounced / self.total_sent) * 100
            self.unsubscribe_rate = (self.total_unsubscribed / self.total_delivered) * 100 if self.total_delivered > 0 else 0
            self.complaint_rate = (self.total_complained / self.total_delivered) * 100 if self.total_delivered > 0 else 0


class UserAnalytics(Base):
    """User analytics model for tracking user behavior and usage."""
    
    __tablename__ = "user_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Usage statistics
    total_campaigns_created = Column(Integer, default=0, nullable=False)
    total_campaigns_sent = Column(Integer, default=0, nullable=False)
    total_emails_sent = Column(Integer, default=0, nullable=False)
    total_recipients = Column(Integer, default=0, nullable=False)
    
    # Engagement metrics
    total_opens = Column(Integer, default=0, nullable=False)
    total_clicks = Column(Integer, default=0, nullable=False)
    average_open_rate = Column(Float, default=0.0, nullable=False)
    average_click_rate = Column(Float, default=0.0, nullable=False)
    
    # AI usage
    total_ai_requests = Column(Integer, default=0, nullable=False)
    ai_requests_today = Column(Integer, default=0, nullable=False)
    ai_requests_this_month = Column(Integer, default=0, nullable=False)
    
    # Subscription and billing
    current_plan = Column(String(50), nullable=True)
    plan_start_date = Column(DateTime, nullable=True)
    plan_end_date = Column(DateTime, nullable=True)
    total_spent = Column(Float, default=0.0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self) -> str:
        return f"<UserAnalytics(user_id={self.user_id})>"


class EmailEvent(Base):
    """Email event model for tracking individual email events."""
    
    __tablename__ = "email_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=False)
    recipient_id = Column(UUID(as_uuid=True), ForeignKey("recipients.id"), nullable=False)
    
    # Event information
    event_type = Column(String(50), nullable=False)  # sent, delivered, opened, clicked, bounced, unsubscribed, complained
    event_data = Column(JSON, default=dict, nullable=False)
    
    # Event details
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    location = Column(JSON, default=dict, nullable=False)
    
    # Timestamps
    event_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    campaign = relationship("Campaign")
    recipient = relationship("Recipient")
    
    def __repr__(self) -> str:
        return f"<EmailEvent(id={self.id}, event_type={self.event_type})>"
