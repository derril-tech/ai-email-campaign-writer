"""
Subscription model for user subscription and billing management.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base


class Subscription(Base):
    """Subscription model for user subscription and billing management."""
    
    __tablename__ = "subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Subscription information
    plan_name = Column(String(100), nullable=False)  # free, pro, enterprise
    plan_type = Column(String(50), nullable=False)  # monthly, yearly
    status = Column(String(50), nullable=False)  # active, cancelled, expired, past_due
    
    # Billing information
    stripe_subscription_id = Column(String(255), nullable=True)
    stripe_customer_id = Column(String(255), nullable=True)
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    cancel_at_period_end = Column(Boolean, default=False, nullable=False)
    
    # Pricing
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    interval = Column(String(20), nullable=False)  # month, year
    
    # Usage limits
    email_limit = Column(Integer, nullable=False)
    recipient_limit = Column(Integer, nullable=False)
    campaign_limit = Column(Integer, nullable=False)
    ai_request_limit = Column(Integer, nullable=False)
    
    # Current usage
    emails_sent_this_period = Column(Integer, default=0, nullable=False)
    recipients_this_period = Column(Integer, default=0, nullable=False)
    campaigns_this_period = Column(Integer, default=0, nullable=False)
    ai_requests_this_period = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    cancelled_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    invoices = relationship("Invoice", back_populates="subscription", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Subscription(id={self.id}, plan={self.plan_name}, status={self.status})>"
    
    @property
    def is_active(self) -> bool:
        """Check if subscription is active."""
        return self.status == "active"
    
    @property
    def is_cancelled(self) -> bool:
        """Check if subscription is cancelled."""
        return self.status == "cancelled" or self.cancel_at_period_end
    
    def get_usage_percentage(self, usage_type: str) -> float:
        """Get usage percentage for a specific type."""
        limits = {
            "emails": self.email_limit,
            "recipients": self.recipient_limit,
            "campaigns": self.campaign_limit,
            "ai_requests": self.ai_request_limit,
        }
        
        usage = {
            "emails": self.emails_sent_this_period,
            "recipients": self.recipients_this_period,
            "campaigns": self.campaigns_this_period,
            "ai_requests": self.ai_requests_this_period,
        }
        
        limit = limits.get(usage_type, 0)
        current_usage = usage.get(usage_type, 0)
        
        if limit == 0:
            return 0.0
        
        return (current_usage / limit) * 100


class Invoice(Base):
    """Invoice model for billing and payment tracking."""
    
    __tablename__ = "invoices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Invoice information
    stripe_invoice_id = Column(String(255), nullable=True)
    invoice_number = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)  # draft, open, paid, void, uncollectible
    
    # Billing details
    amount_due = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    
    # Billing period
    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)
    
    # Payment information
    payment_intent_id = Column(String(255), nullable=True)
    payment_status = Column(String(50), nullable=False)  # pending, paid, failed, cancelled
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    
    # Relationships
    subscription = relationship("Subscription", back_populates="invoices")
    user = relationship("User")
    
    def __repr__(self) -> str:
        return f"<Invoice(id={self.id}, number={self.invoice_number}, status={self.status})>"
    
    @property
    def is_paid(self) -> bool:
        """Check if invoice is paid."""
        return self.status == "paid" and self.payment_status == "paid"
    
    @property
    def is_overdue(self) -> bool:
        """Check if invoice is overdue."""
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and not self.is_paid
