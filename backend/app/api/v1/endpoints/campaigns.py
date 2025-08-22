"""
Campaign API endpoints for managing email campaigns.
"""

from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from loguru import logger
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.campaign import Campaign
from app.models.recipient import Recipient
from app.models.analytics import CampaignAnalytics
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignList,
    CampaignStats,
    AIGenerationRequest,
    AIGenerationResponse
)
from app.schemas.common import PaginationParams, PaginatedResponse
from app.services.ai_service import get_ai_service, AIService
from app.services.email_service import get_email_service, EmailService
from app.core.redis import get_redis, RedisClient


router = APIRouter()


@router.post("/", response_model=CampaignResponse)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """Create a new email campaign."""
    try:
        # Check user's campaign limit
        existing_campaigns = await db.execute(
            select(Campaign).where(Campaign.user_id == current_user.id)
        )
        if existing_campaigns.scalars().count() >= 100:  # Limit per user
            raise HTTPException(
                status_code=400,
                detail="Campaign limit reached. Please upgrade your plan."
            )
        
        # Create campaign
        campaign = Campaign(
            user_id=current_user.id,
            name=campaign_data.name,
            subject=campaign_data.subject,
            content=campaign_data.content,
            type=campaign_data.type,
            status="draft",
            scheduled_at=campaign_data.scheduled_at,
            sender_name=campaign_data.sender_name,
            sender_email=campaign_data.sender_email,
            tags=campaign_data.tags or []
        )
        
        db.add(campaign)
        await db.commit()
        await db.refresh(campaign)
        
        logger.info(f"Campaign created: {campaign.id} by user {current_user.id}")
        
        return CampaignResponse.from_orm(campaign)
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating campaign: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create campaign")


@router.get("/", response_model=PaginatedResponse[CampaignList])
async def list_campaigns(
    pagination: PaginationParams = Depends(),
    status: Optional[str] = Query(None, description="Filter by campaign status"),
    type: Optional[str] = Query(None, description="Filter by campaign type"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's campaigns with pagination and filtering."""
    try:
        # Build query
        query = select(Campaign).where(Campaign.user_id == current_user.id)
        
        if status:
            query = query.where(Campaign.status == status)
        if type:
            query = query.where(Campaign.type == type)
        
        # Add ordering
        query = query.order_by(Campaign.created_at.desc())
        
        # Get total count
        count_query = select(Campaign).where(Campaign.user_id == current_user.id)
        if status:
            count_query = count_query.where(Campaign.status == status)
        if type:
            count_query = count_query.where(Campaign.type == type)
        
        total = await db.scalar(select(func.count()).select_from(count_query.subquery()))
        
        # Apply pagination
        query = query.offset(pagination.offset).limit(pagination.limit)
        
        # Execute query
        result = await db.execute(query)
        campaigns = result.scalars().all()
        
        # Convert to response models
        campaign_list = [CampaignList.from_orm(campaign) for campaign in campaigns]
        
        return PaginatedResponse(
            items=campaign_list,
            total=total,
            page=pagination.page,
            size=pagination.limit,
            pages=(total + pagination.limit - 1) // pagination.limit
        )
        
    except Exception as e:
        logger.error(f"Error listing campaigns: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list campaigns")


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific campaign by ID."""
    try:
        result = await db.execute(
            select(Campaign)
            .where(Campaign.id == campaign_id, Campaign.user_id == current_user.id)
            .options(selectinload(Campaign.recipients))
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        return CampaignResponse.from_orm(campaign)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting campaign: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get campaign")


@router.put("/{campaign_id}", response_model=CampaignResponse)
async def update_campaign(
    campaign_id: str,
    campaign_data: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a campaign."""
    try:
        # Get campaign
        result = await db.execute(
            select(Campaign).where(
                Campaign.id == campaign_id,
                Campaign.user_id == current_user.id
            )
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Check if campaign can be updated
        if campaign.status in ["sending", "sent"]:
            raise HTTPException(
                status_code=400,
                detail="Cannot update campaign that is already sent or sending"
            )
        
        # Update fields
        update_data = campaign_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(campaign, field, value)
        
        await db.commit()
        await db.refresh(campaign)
        
        logger.info(f"Campaign updated: {campaign_id} by user {current_user.id}")
        
        return CampaignResponse.from_orm(campaign)
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating campaign: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update campaign")


@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a campaign."""
    try:
        # Get campaign
        result = await db.execute(
            select(Campaign).where(
                Campaign.id == campaign_id,
                Campaign.user_id == current_user.id
            )
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Check if campaign can be deleted
        if campaign.status in ["sending", "sent"]:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete campaign that is already sent or sending"
            )
        
        # Delete campaign
        await db.execute(delete(Campaign).where(Campaign.id == campaign_id))
        await db.commit()
        
        logger.info(f"Campaign deleted: {campaign_id} by user {current_user.id}")
        
        return {"message": "Campaign deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting campaign: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete campaign")


@router.post("/{campaign_id}/send")
async def send_campaign(
    campaign_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    email_service: EmailService = Depends(get_email_service)
):
    """Send a campaign immediately."""
    try:
        # Get campaign with recipients
        result = await db.execute(
            select(Campaign)
            .where(Campaign.id == campaign_id, Campaign.user_id == current_user.id)
            .options(selectinload(Campaign.recipients))
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        if campaign.status != "draft":
            raise HTTPException(
                status_code=400,
                detail="Only draft campaigns can be sent"
            )
        
        if not campaign.recipients:
            raise HTTPException(
                status_code=400,
                detail="Campaign has no recipients"
            )
        
        # Update campaign status
        campaign.status = "sending"
        campaign.sent_at = datetime.utcnow()
        await db.commit()
        
        # Send campaign in background
        background_tasks.add_task(
            send_campaign_background,
            campaign_id,
            current_user.id
        )
        
        logger.info(f"Campaign sending started: {campaign_id} by user {current_user.id}")
        
        return {"message": "Campaign sending started"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error sending campaign: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send campaign")


@router.post("/{campaign_id}/schedule")
async def schedule_campaign(
    campaign_id: str,
    scheduled_at: datetime,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Schedule a campaign for later sending."""
    try:
        # Get campaign
        result = await db.execute(
            select(Campaign).where(
                Campaign.id == campaign_id,
                Campaign.user_id == current_user.id
            )
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        if campaign.status != "draft":
            raise HTTPException(
                status_code=400,
                detail="Only draft campaigns can be scheduled"
            )
        
        # Update campaign
        campaign.status = "scheduled"
        campaign.scheduled_at = scheduled_at
        await db.commit()
        
        logger.info(f"Campaign scheduled: {campaign_id} for {scheduled_at}")
        
        return {"message": "Campaign scheduled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error scheduling campaign: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to schedule campaign")


@router.post("/{campaign_id}/pause")
async def pause_campaign(
    campaign_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Pause a sending campaign."""
    try:
        # Get campaign
        result = await db.execute(
            select(Campaign).where(
                Campaign.id == campaign_id,
                Campaign.user_id == current_user.id
            )
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        if campaign.status != "sending":
            raise HTTPException(
                status_code=400,
                detail="Only sending campaigns can be paused"
            )
        
        # Update campaign
        campaign.status = "paused"
        await db.commit()
        
        logger.info(f"Campaign paused: {campaign_id}")
        
        return {"message": "Campaign paused successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error pausing campaign: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to pause campaign")


@router.post("/{campaign_id}/resume")
async def resume_campaign(
    campaign_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Resume a paused campaign."""
    try:
        # Get campaign
        result = await db.execute(
            select(Campaign).where(
                Campaign.id == campaign_id,
                Campaign.user_id == current_user.id
            )
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        if campaign.status != "paused":
            raise HTTPException(
                status_code=400,
                detail="Only paused campaigns can be resumed"
            )
        
        # Update campaign
        campaign.status = "sending"
        await db.commit()
        
        # Resume sending in background
        background_tasks.add_task(
            send_campaign_background,
            campaign_id,
            current_user.id
        )
        
        logger.info(f"Campaign resumed: {campaign_id}")
        
        return {"message": "Campaign resumed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error resuming campaign: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to resume campaign")


@router.post("/{campaign_id}/ai-generate", response_model=AIGenerationResponse)
async def generate_campaign_content(
    campaign_id: str,
    generation_request: AIGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    ai_service: AIService = Depends(get_ai_service)
):
    """Generate campaign content using AI."""
    try:
        # Get campaign
        result = await db.execute(
            select(Campaign).where(
                Campaign.id == campaign_id,
                Campaign.user_id == current_user.id
            )
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Generate content based on request type
        if generation_request.type == "content":
            result = await ai_service.generate_email_content(
                campaign_type=generation_request.campaign_type or campaign.type,
                target_audience=generation_request.target_audience,
                key_points=generation_request.key_points,
                tone=generation_request.tone,
                length=generation_request.length,
                language=generation_request.language
            )
            
            # Update campaign with generated content
            campaign.subject = result["subject"]
            campaign.content = result["body"]
            
        elif generation_request.type == "subject":
            result = await ai_service.generate_subject_line(
                email_content=campaign.content,
                campaign_type=generation_request.campaign_type or campaign.type,
                target_audience=generation_request.target_audience,
                tone=generation_request.tone,
                max_length=generation_request.max_length or 60
            )
            
            # Update campaign with generated subject
            campaign.subject = result["recommended"]
        
        await db.commit()
        
        logger.info(f"AI content generated for campaign: {campaign_id}")
        
        return AIGenerationResponse(
            success=True,
            content=result,
            campaign_id=campaign_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error generating AI content: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate content")


@router.get("/{campaign_id}/stats", response_model=CampaignStats)
async def get_campaign_stats(
    campaign_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    email_service: EmailService = Depends(get_email_service)
):
    """Get campaign statistics and analytics."""
    try:
        # Get campaign
        result = await db.execute(
            select(Campaign).where(
                Campaign.id == campaign_id,
                Campaign.user_id == current_user.id
            )
        )
        campaign = result.scalar_one_or_none()
        
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        # Get email delivery stats
        delivery_stats = await email_service.get_campaign_stats(campaign_id)
        
        # Get analytics data
        analytics_result = await db.execute(
            select(CampaignAnalytics).where(CampaignAnalytics.campaign_id == campaign_id)
        )
        analytics = analytics_result.scalar_one_or_none()
        
        # Build stats response
        stats = CampaignStats(
            campaign_id=campaign_id,
            total_recipients=len(campaign.recipients),
            sent=delivery_stats["successful"],
            failed=delivery_stats["failed"],
            open_rate=analytics.open_rate if analytics else 0.0,
            click_rate=analytics.click_rate if analytics else 0.0,
            bounce_rate=analytics.bounce_rate if analytics else 0.0,
            unsubscribe_rate=analytics.unsubscribe_rate if analytics else 0.0,
            revenue=analytics.revenue if analytics else 0.0
        )
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting campaign stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get campaign stats")


async def send_campaign_background(campaign_id: str, user_id: str):
    """Background task to send campaign emails."""
    try:
        # This would be implemented as a Celery task in production
        # For now, we'll simulate the sending process
        logger.info(f"Starting background campaign send: {campaign_id}")
        
        # Get campaign and recipients from database
        # Send emails in batches
        # Update campaign status when complete
        
        logger.info(f"Campaign send completed: {campaign_id}")
        
    except Exception as e:
        logger.error(f"Error in background campaign send: {str(e)}")
        # Update campaign status to failed
