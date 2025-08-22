"""
Notification model for user notifications and alerts.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base


class Notification(Base):
    """Notification model for user notifications and alerts."""
    
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Notification information
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # info, success, warning, error
    category = Column(String(50), nullable=False)  # campaign, billing, system, ai
    
    # Notification settings
    is_read = Column(Boolean, default=False, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)
    priority = Column(String(20), default="normal", nullable=False)  # low, normal, high, urgent
    
    # Action and metadata
    action_url = Column(String(500), nullable=True)
    action_text = Column(String(100), nullable=True)
    metadata = Column(JSON, default=dict, nullable=False)
    
    # Delivery settings
    email_sent = Column(Boolean, default=False, nullable=False)
    email_sent_at = Column(DateTime, nullable=True)
    push_sent = Column(Boolean, default=False, nullable=False)
    push_sent_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    read_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self) -> str:
        return f"<Notification(id={self.id}, type={self.notification_type}, title={self.title})>"
    
    @property
    def is_expired(self) -> bool:
        """Check if notification is expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_actionable(self) -> bool:
        """Check if notification has an action."""
        return bool(self.action_url and self.action_text)
    
    def mark_as_read(self) -> None:
        """Mark notification as read."""
        self.is_read = True
        self.read_at = datetime.utcnow()
    
    def archive(self) -> None:
        """Archive notification."""
        self.is_archived = True


class NotificationTemplate(Base):
    """Notification template model for predefined notification templates."""
    
    __tablename__ = "notification_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Template information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    title_template = Column(String(255), nullable=False)
    message_template = Column(Text, nullable=False)
    
    # Template settings
    notification_type = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    priority = Column(String(20), default="normal", nullable=False)
    
    # Template variables
    variables = Column(JSON, default=list, nullable=False)
    
    # Delivery settings
    send_email = Column(Boolean, default=True, nullable=False)
    send_push = Column(Boolean, default=False, nullable=False)
    
    # Template metadata
    is_active = Column(Boolean, default=True, nullable=False)
    tags = Column(JSON, default=list, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<NotificationTemplate(id={self.id}, name={self.name})>"
    
    def render(self, **kwargs) -> dict:
        """Render template with provided variables."""
        title = self.title_template
        message = self.message_template
        
        for key, value in kwargs.items():
            title = title.replace(f"{{{key}}}", str(value))
            message = message.replace(f"{{{key}}}", str(value))
        
        return {
            "title": title,
            "message": message,
            "notification_type": self.notification_type,
            "category": self.category,
            "priority": self.priority,
            "send_email": self.send_email,
            "send_push": self.send_push,
        }
