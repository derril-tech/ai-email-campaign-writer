"""
API v1 package for the AI Email Campaign Writer backend.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, campaigns, recipients, templates, ai, analytics, subscriptions, notifications

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["Campaigns"])
api_router.include_router(recipients.router, prefix="/recipients", tags=["Recipients"])
api_router.include_router(templates.router, prefix="/templates", tags=["Templates"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
