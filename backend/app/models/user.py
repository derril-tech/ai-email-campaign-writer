"""
User model for authentication and user management.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class UserRole(str, enum.Enum):
    """User roles enumeration"""
    USER = "user"
    ADMIN = "admin"
    PREMIUM = "premium"

class SubscriptionPlan(str, enum.Enum):
    """Subscription plans enumeration"""
    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class User(Base):
    """User model for authentication and profile management"""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Profile fields
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    company_name = Column(String(255), nullable=True)
    industry = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    website = Column(String(255), nullable=True)
    
    # Social links
    social_links = Column(JSON, nullable=True)  # {twitter, linkedin, github}
    
    # User preferences
    preferences = Column(JSON, nullable=True)  # {theme, timezone, notifications}
    
    # Role and subscription
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE, nullable=False)
    subscription_expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Stripe customer ID for payments
    stripe_customer_id = Column(String(255), nullable=True)
    
    # Usage tracking
    emails_sent_this_month = Column(Integer, default=0, nullable=False)
    ai_generations_this_month = Column(Integer, default=0, nullable=False)
    campaigns_created = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    campaigns = relationship("Campaign", back_populates="user", cascade="all, delete-orphan")
    audiences = relationship("Audience", back_populates="user", cascade="all, delete-orphan")
    templates = relationship("Template", back_populates="user", cascade="all, delete-orphan")
    ai_generations = relationship("AIGeneration", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def initials(self) -> str:
        """Get user's initials"""
        return f"{self.first_name[0]}{self.last_name[0]}".upper()
    
    @property
    def is_premium(self) -> bool:
        """Check if user has premium subscription"""
        return self.subscription_plan in [SubscriptionPlan.PREMIUM, SubscriptionPlan.ENTERPRISE]
    
    @property
    def can_create_campaign(self) -> bool:
        """Check if user can create a new campaign"""
        if self.role == UserRole.ADMIN:
            return True
        return self.campaigns_created < self.get_campaign_limit()
    
    @property
    def can_send_emails(self) -> bool:
        """Check if user can send emails"""
        if self.role == UserRole.ADMIN:
            return True
        return self.emails_sent_this_month < self.get_email_limit()
    
    @property
    def can_generate_ai_content(self) -> bool:
        """Check if user can generate AI content"""
        if self.role == UserRole.ADMIN:
            return True
        return self.ai_generations_this_month < self.get_ai_generation_limit()
    
    def get_campaign_limit(self) -> int:
        """Get campaign limit based on subscription"""
        limits = {
            SubscriptionPlan.FREE: 5,
            SubscriptionPlan.BASIC: 25,
            SubscriptionPlan.PREMIUM: 100,
            SubscriptionPlan.ENTERPRISE: 1000
        }
        return limits.get(self.subscription_plan, 5)
    
    def get_email_limit(self) -> int:
        """Get email limit based on subscription"""
        limits = {
            SubscriptionPlan.FREE: 1000,
            SubscriptionPlan.BASIC: 10000,
            SubscriptionPlan.PREMIUM: 50000,
            SubscriptionPlan.ENTERPRISE: 1000000
        }
        return limits.get(self.subscription_plan, 1000)
    
    def get_ai_generation_limit(self) -> int:
        """Get AI generation limit based on subscription"""
        limits = {
            SubscriptionPlan.FREE: 50,
            SubscriptionPlan.BASIC: 200,
            SubscriptionPlan.PREMIUM: 1000,
            SubscriptionPlan.ENTERPRISE: 10000
        }
        return limits.get(self.subscription_plan, 50)
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        if self.role == UserRole.ADMIN:
            return True
        
        permissions = {
            "create_campaign": self.can_create_campaign,
            "send_emails": self.can_send_emails,
            "generate_ai": self.can_generate_ai_content,
            "advanced_analytics": self.is_premium,
            "team_collaboration": self.is_premium,
            "api_access": self.is_premium,
            "white_label": self.subscription_plan == SubscriptionPlan.ENTERPRISE
        }
        
        return permissions.get(permission, False)
