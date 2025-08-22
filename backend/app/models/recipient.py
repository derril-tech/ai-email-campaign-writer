"""
Recipient model for managing email recipients and lists.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base


class Recipient(Base):
    """Recipient model for managing email recipients."""
    
    __tablename__ = "recipients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Contact information
    email = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    company = Column(String(200), nullable=True)
    job_title = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Status and preferences
    is_active = Column(Boolean, default=True, nullable=False)
    is_subscribed = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Subscription preferences
    subscription_source = Column(String(100), nullable=True)  # website, import, api, etc.
    subscription_date = Column(DateTime, nullable=True)
    unsubscription_date = Column(DateTime, nullable=True)
    
    # Custom fields
    custom_fields = Column(JSON, default=dict, nullable=False)
    
    # Tags and lists
    tags = Column(JSON, default=list, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="recipients")
    campaigns = relationship("CampaignRecipient", back_populates="recipient", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Recipient(id={self.id}, email={self.email})>"
    
    @property
    def full_name(self) -> str:
        """Get recipient's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return ""


class RecipientList(Base):
    """Recipient list model for organizing recipients into groups."""
    
    __tablename__ = "recipient_lists"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # List information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # List settings
    is_active = Column(Boolean, default=True, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    
    # List metadata
    tags = Column(JSON, default=list, nullable=False)
    metadata = Column(JSON, default=dict, nullable=False)
    
    # Statistics
    total_recipients = Column(Integer, default=0, nullable=False)
    active_recipients = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User")
    recipients = relationship("RecipientListMember", back_populates="list", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<RecipientList(id={self.id}, name={self.name})>"


class RecipientListMember(Base):
    """Recipient list member model for managing list memberships."""
    
    __tablename__ = "recipient_list_members"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    list_id = Column(UUID(as_uuid=True), ForeignKey("recipient_lists.id"), nullable=False)
    recipient_id = Column(UUID(as_uuid=True), ForeignKey("recipients.id"), nullable=False)
    
    # Membership status
    is_active = Column(Boolean, default=True, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    left_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    list = relationship("RecipientList", back_populates="recipients")
    recipient = relationship("Recipient")
    
    def __repr__(self) -> str:
        return f"<RecipientListMember(list_id={self.list_id}, recipient_id={self.recipient_id})>"
