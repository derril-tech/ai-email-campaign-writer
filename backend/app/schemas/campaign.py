"""
Campaign schemas for campaign management and operations.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class CampaignBase(BaseModel):
    """Base campaign schema."""
    name: str = Field(..., min_length=1, max_length=255, description="Campaign name")
    description: Optional[str] = Field(None, description="Campaign description")
    subject: str = Field(..., min_length=1, max_length=255, description="Email subject line")
    content: str = Field(..., min_length=1, description="Email content")
    type: str = Field(..., regex="^(newsletter|promotional|transactional|automated)$", description="Campaign type")
    sender_name: str = Field(..., min_length=1, max_length=100, description="Sender name")
    sender_email: EmailStr = Field(..., description="Sender email address")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled send time")
    tags: List[str] = Field(default_factory=list, description="Campaign tags")


class CampaignCreate(CampaignBase):
    """Campaign creation schema."""
    recipient_list_ids: List[str] = Field(..., description="List of recipient list IDs")
    template_id: Optional[str] = Field(None, description="Template ID to use")
    variables: Optional[Dict[str, Any]] = Field(None, description="Template variables")


class CampaignUpdate(BaseModel):
    """Campaign update schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Campaign name")
    description: Optional[str] = Field(None, description="Campaign description")
    subject: Optional[str] = Field(None, min_length=1, max_length=255, description="Email subject line")
    content: Optional[str] = Field(None, min_length=1, description="Email content")
    sender_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Sender name")
    sender_email: Optional[EmailStr] = Field(None, description="Sender email address")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled send time")
    tags: Optional[List[str]] = Field(None, description="Campaign tags")
    status: Optional[str] = Field(None, regex="^(draft|scheduled|sending|sent|paused)$", description="Campaign status")


class CampaignResponse(CampaignBase):
    """Campaign response schema."""
    id: str = Field(..., description="Campaign ID")
    user_id: str = Field(..., description="User ID")
    status: str = Field(..., description="Campaign status")
    html_content: Optional[str] = Field(None, description="HTML content")
    plain_text_content: Optional[str] = Field(None, description="Plain text content")
    
    # Statistics
    total_recipients: int = Field(..., description="Total recipients")
    sent_count: int = Field(..., description="Number of emails sent")
    opened_count: int = Field(..., description="Number of emails opened")
    clicked_count: int = Field(..., description="Number of emails clicked")
    bounced_count: int = Field(..., description="Number of emails bounced")
    unsubscribed_count: int = Field(..., description="Number of unsubscribes")
    
    # Calculated rates
    open_rate: float = Field(..., description="Open rate percentage")
    click_rate: float = Field(..., description="Click rate percentage")
    bounce_rate: float = Field(..., description="Bounce rate percentage")
    
    # Timestamps
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")
    sent_at: Optional[datetime] = Field(None, description="Send date")
    
    class Config:
        from_attributes = True


class CampaignList(BaseModel):
    """Campaign list response schema."""
    campaigns: List[CampaignResponse] = Field(..., description="List of campaigns")
    total: int = Field(..., description="Total number of campaigns")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of campaigns per page")
    pages: int = Field(..., description="Total number of pages")


class CampaignStats(BaseModel):
    """Campaign statistics schema."""
    campaign_id: str = Field(..., description="Campaign ID")
    total_sent: int = Field(..., description="Total emails sent")
    total_delivered: int = Field(..., description="Total emails delivered")
    total_bounced: int = Field(..., description="Total emails bounced")
    total_opened: int = Field(..., description="Total emails opened")
    total_clicked: int = Field(..., description="Total emails clicked")
    total_unsubscribed: int = Field(..., description="Total unsubscribes")
    total_complained: int = Field(..., description="Total complaints")
    
    # Rates
    delivery_rate: float = Field(..., description="Delivery rate percentage")
    open_rate: float = Field(..., description="Open rate percentage")
    click_rate: float = Field(..., description="Click rate percentage")
    bounce_rate: float = Field(..., description="Bounce rate percentage")
    unsubscribe_rate: float = Field(..., description="Unsubscribe rate percentage")
    complaint_rate: float = Field(..., description="Complaint rate percentage")
    
    # Engagement
    unique_opens: int = Field(..., description="Unique opens")
    unique_clicks: int = Field(..., description="Unique clicks")
    total_clicks: int = Field(..., description="Total clicks")
    
    # Geographic and device data
    geographic_data: Dict[str, Any] = Field(default_factory=dict, description="Geographic data")
    device_data: Dict[str, Any] = Field(default_factory=dict, description="Device data")
    client_data: Dict[str, Any] = Field(default_factory=dict, description="Client data")
    
    # Timestamps
    created_at: datetime = Field(..., description="Statistics creation date")
    updated_at: datetime = Field(..., description="Last update date")


class CampaignRecipientResponse(BaseModel):
    """Campaign recipient response schema."""
    id: str = Field(..., description="Campaign recipient ID")
    campaign_id: str = Field(..., description="Campaign ID")
    recipient_id: str = Field(..., description="Recipient ID")
    email: str = Field(..., description="Recipient email")
    first_name: Optional[str] = Field(None, description="Recipient first name")
    last_name: Optional[str] = Field(None, description="Recipient last name")
    
    # Status
    status: str = Field(..., description="Delivery status")
    sent_at: Optional[datetime] = Field(None, description="Sent date")
    delivered_at: Optional[datetime] = Field(None, description="Delivered date")
    opened_at: Optional[datetime] = Field(None, description="Opened date")
    clicked_at: Optional[datetime] = Field(None, description="Clicked date")
    bounced_at: Optional[datetime] = Field(None, description="Bounced date")
    unsubscribed_at: Optional[datetime] = Field(None, description="Unsubscribed date")
    
    # Tracking
    open_count: int = Field(..., description="Number of opens")
    click_count: int = Field(..., description="Number of clicks")
    last_opened_at: Optional[datetime] = Field(None, description="Last opened date")
    last_clicked_at: Optional[datetime] = Field(None, description="Last clicked date")
    
    class Config:
        from_attributes = True


class CampaignAction(BaseModel):
    """Campaign action schema."""
    action: str = Field(..., regex="^(send|pause|resume|cancel|duplicate)$", description="Action to perform")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled time for send action")


class CampaignDuplicate(BaseModel):
    """Campaign duplication schema."""
    name: str = Field(..., description="New campaign name")
    include_recipients: bool = Field(True, description="Include recipients in duplicated campaign")
    include_analytics: bool = Field(False, description="Include analytics in duplicated campaign")
