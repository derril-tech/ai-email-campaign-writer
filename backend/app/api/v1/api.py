from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, campaigns, audiences, templates, ai, analytics

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["Campaigns"])
api_router.include_router(audiences.router, prefix="/audiences", tags=["Audiences"])
api_router.include_router(templates.router, prefix="/templates", tags=["Templates"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Generation"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
