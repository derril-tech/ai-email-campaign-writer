"""
User schemas for user management and profile operations.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=100, description="User first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="User last name")
    company: Optional[str] = Field(None, max_length=200, description="User company")
    job_title: Optional[str] = Field(None, max_length=100, description="User job title")


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8, description="User password")
    accept_terms: bool = Field(..., description="Accept terms and conditions")
    marketing_emails: bool = Field(False, description="Subscribe to marketing emails")


class UserUpdate(BaseModel):
    """User update schema."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, description="User first name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, description="User last name")
    company: Optional[str] = Field(None, max_length=200, description="User company")
    job_title: Optional[str] = Field(None, max_length=100, description="User job title")
    avatar: Optional[str] = Field(None, description="User avatar URL")
    marketing_emails: Optional[bool] = Field(None, description="Marketing emails preference")


class UserResponse(UserBase):
    """User response schema."""
    id: str = Field(..., description="User ID")
    avatar: Optional[str] = Field(None, description="User avatar URL")
    role: str = Field(..., description="User role")
    is_active: bool = Field(..., description="User active status")
    is_email_verified: bool = Field(..., description="Email verification status")
    last_login: Optional[datetime] = Field(None, description="Last login date")
    login_count: int = Field(..., description="Total login count")
    created_at: datetime = Field(..., description="Account creation date")
    updated_at: datetime = Field(..., description="Last update date")
    
    class Config:
        from_attributes = True


class UserList(BaseModel):
    """User list response schema."""
    users: List[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of users per page")
    pages: int = Field(..., description="Total number of pages")


class UserProfile(BaseModel):
    """User profile schema."""
    id: str = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")
    company: Optional[str] = Field(None, description="User company")
    job_title: Optional[str] = Field(None, description="User job title")
    avatar: Optional[str] = Field(None, description="User avatar URL")
    role: str = Field(..., description="User role")
    is_email_verified: bool = Field(..., description="Email verification status")
    marketing_emails: bool = Field(..., description="Marketing emails preference")
    created_at: datetime = Field(..., description="Account creation date")
    last_login: Optional[datetime] = Field(None, description="Last login date")
    
    class Config:
        from_attributes = True


class UserStats(BaseModel):
    """User statistics schema."""
    total_campaigns: int = Field(..., description="Total campaigns created")
    total_emails_sent: int = Field(..., description="Total emails sent")
    total_recipients: int = Field(..., description="Total recipients")
    average_open_rate: float = Field(..., description="Average open rate")
    average_click_rate: float = Field(..., description="Average click rate")
    total_ai_requests: int = Field(..., description="Total AI requests made")
    current_plan: Optional[str] = Field(None, description="Current subscription plan")


class UserPreferences(BaseModel):
    """User preferences schema."""
    marketing_emails: bool = Field(..., description="Marketing emails preference")
    notification_emails: bool = Field(..., description="Notification emails preference")
    timezone: str = Field(..., description="User timezone")
    language: str = Field(..., description="User language preference")
    theme: str = Field(..., description="UI theme preference")
    email_signature: Optional[str] = Field(None, description="Email signature")
    default_sender_name: Optional[str] = Field(None, description="Default sender name")
    default_sender_email: Optional[EmailStr] = Field(None, description="Default sender email")


class UserPreferencesUpdate(BaseModel):
    """User preferences update schema."""
    marketing_emails: Optional[bool] = Field(None, description="Marketing emails preference")
    notification_emails: Optional[bool] = Field(None, description="Notification emails preference")
    timezone: Optional[str] = Field(None, description="User timezone")
    language: Optional[str] = Field(None, description="User language preference")
    theme: Optional[str] = Field(None, description="UI theme preference")
    email_signature: Optional[str] = Field(None, description="Email signature")
    default_sender_name: Optional[str] = Field(None, description="Default sender name")
    default_sender_email: Optional[EmailStr] = Field(None, description="Default sender email")
