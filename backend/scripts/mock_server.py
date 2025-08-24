#!/usr/bin/env python3
"""
Mock server for AI Email Campaign Writer API
Used for development and testing when the real backend is not available
"""

import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import uvicorn

# Mock data storage
mock_users: Dict[str, Dict] = {}
mock_campaigns: Dict[str, Dict] = {}
mock_tokens: Dict[str, str] = {}  # token -> user_id

# Pydantic models
class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: Optional[str] = None
    industry: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenRefresh(BaseModel):
    refresh_token: str

class CampaignCreate(BaseModel):
    name: str
    subject: str
    content: str
    scheduled_at: Optional[datetime] = None

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None

class AIGenerationRequest(BaseModel):
    prompt: str
    context: Optional[str] = None
    tone: Optional[str] = "professional"
    length: Optional[str] = "medium"
    variables: Optional[Dict[str, str]] = None

class AIImprovementRequest(BaseModel):
    content: str
    improvement_type: Optional[str] = "clarity"
    suggestions: Optional[bool] = True

# FastAPI app setup
app = FastAPI(
    title="AI Email Campaign Writer - Mock API",
    description="Mock server for development and testing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """Get current user from token"""
    token = credentials.credentials
    user_id = mock_tokens.get(token)
    if not user_id or user_id not in mock_users:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return mock_users[user_id]

def generate_token() -> str:
    """Generate a mock JWT token"""
    return f"mock_token_{uuid.uuid4().hex}"

# Initialize with some mock data
def init_mock_data():
    """Initialize mock data for testing"""
    # Create a test user
    test_user = {
        "id": "1",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "company_name": "Test Company",
        "industry": "Technology",
        "role": "user",
        "subscription": "pro",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    mock_users["1"] = test_user
    
    # Create test campaigns
    test_campaigns = [
        {
            "id": "1",
            "user_id": "1",
            "name": "Welcome Campaign",
            "subject": "Welcome to AI Email Campaign Writer!",
            "content": "<h1>Welcome!</h1><p>Thank you for joining us.</p>",
            "status": "sent",
            "recipient_count": 500,
            "sent_count": 500,
            "opened_count": 125,
            "clicked_count": 25,
            "open_rate": 25.0,
            "click_rate": 5.0,
            "scheduled_at": None,
            "sent_at": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        },
        {
            "id": "2",
            "user_id": "1",
            "name": "Product Launch",
            "subject": "🚀 New Features Available Now!",
            "content": "<h1>New Features</h1><p>Check out our latest updates.</p>",
            "status": "scheduled",
            "recipient_count": 1200,
            "sent_count": 0,
            "opened_count": 0,
            "clicked_count": 0,
            "open_rate": 0.0,
            "click_rate": 0.0,
            "scheduled_at": (datetime.now() + timedelta(days=1)).isoformat(),
            "sent_at": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
    ]
    
    for campaign in test_campaigns:
        mock_campaigns[campaign["id"]] = campaign

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "mock"
    }

# Authentication endpoints
@app.post("/auth/register", status_code=201)
async def register(user_data: UserRegistration):
    # Check if user already exists
    for user in mock_users.values():
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )
    
    # Create new user
    user_id = str(len(mock_users) + 1)
    new_user = {
        "id": user_id,
        "email": user_data.email,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "company_name": user_data.company_name,
        "industry": user_data.industry,
        "role": "user",
        "subscription": "free",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    mock_users[user_id] = new_user
    
    # Generate tokens
    access_token = generate_token()
    refresh_token = generate_token()
    mock_tokens[access_token] = user_id
    
    return {
        "user": new_user,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@app.post("/auth/login")
async def login(login_data: UserLogin):
    # Find user by email
    user = None
    for u in mock_users.values():
        if u["email"] == login_data.email:
            user = u
            break
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Generate tokens
    access_token = generate_token()
    refresh_token = generate_token()
    mock_tokens[access_token] = user["id"]
    
    return {
        "user": user,
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@app.post("/auth/refresh")
async def refresh_token(refresh_data: TokenRefresh):
    # In a real implementation, you'd validate the refresh token
    # For mock purposes, we'll just generate a new token
    access_token = generate_token()
    # Assume user_id is "1" for mock purposes
    mock_tokens[access_token] = "1"
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_data.refresh_token
    }

# Campaign endpoints
@app.get("/campaigns")
async def list_campaigns(
    page: int = 1,
    limit: int = 10,
    status: Optional[str] = None,
    current_user: Dict = Depends(get_current_user)
):
    user_campaigns = [
        campaign for campaign in mock_campaigns.values()
        if campaign["user_id"] == current_user["id"]
    ]
    
    # Filter by status if provided
    if status:
        user_campaigns = [
            campaign for campaign in user_campaigns
            if campaign["status"] == status
        ]
    
    # Pagination
    start = (page - 1) * limit
    end = start + limit
    paginated_campaigns = user_campaigns[start:end]
    
    return {
        "items": paginated_campaigns,
        "total": len(user_campaigns),
        "page": page,
        "limit": limit,
        "total_pages": (len(user_campaigns) + limit - 1) // limit
    }

@app.post("/campaigns", status_code=201)
async def create_campaign(
    campaign_data: CampaignCreate,
    current_user: Dict = Depends(get_current_user)
):
    campaign_id = str(len(mock_campaigns) + 1)
    new_campaign = {
        "id": campaign_id,
        "user_id": current_user["id"],
        "name": campaign_data.name,
        "subject": campaign_data.subject,
        "content": campaign_data.content,
        "status": "draft",
        "recipient_count": 0,
        "sent_count": 0,
        "opened_count": 0,
        "clicked_count": 0,
        "open_rate": 0.0,
        "click_rate": 0.0,
        "scheduled_at": campaign_data.scheduled_at.isoformat() if campaign_data.scheduled_at else None,
        "sent_at": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    mock_campaigns[campaign_id] = new_campaign
    
    return new_campaign

@app.get("/campaigns/{campaign_id}")
async def get_campaign(
    campaign_id: str,
    current_user: Dict = Depends(get_current_user)
):
    if campaign_id not in mock_campaigns:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    campaign = mock_campaigns[campaign_id]
    if campaign["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    return campaign

@app.put("/campaigns/{campaign_id}")
async def update_campaign(
    campaign_id: str,
    campaign_data: CampaignUpdate,
    current_user: Dict = Depends(get_current_user)
):
    if campaign_id not in mock_campaigns:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    campaign = mock_campaigns[campaign_id]
    if campaign["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Update fields
    update_data = campaign_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "scheduled_at" and value:
            campaign[key] = value.isoformat()
        else:
            campaign[key] = value
    
    campaign["updated_at"] = datetime.now().isoformat()
    mock_campaigns[campaign_id] = campaign
    
    return campaign

@app.delete("/campaigns/{campaign_id}", status_code=204)
async def delete_campaign(
    campaign_id: str,
    current_user: Dict = Depends(get_current_user)
):
    if campaign_id not in mock_campaigns:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    campaign = mock_campaigns[campaign_id]
    if campaign["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    del mock_campaigns[campaign_id]

@app.post("/campaigns/{campaign_id}/send")
async def send_campaign(
    campaign_id: str,
    current_user: Dict = Depends(get_current_user)
):
    if campaign_id not in mock_campaigns:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    campaign = mock_campaigns[campaign_id]
    if campaign["user_id"] != current_user["id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found"
        )
    
    # Update campaign status
    campaign["status"] = "sent"
    campaign["sent_at"] = datetime.now().isoformat()
    campaign["updated_at"] = datetime.now().isoformat()
    mock_campaigns[campaign_id] = campaign
    
    return {
        "message": "Campaign sent successfully",
        "campaign_id": campaign_id
    }

# AI endpoints
@app.post("/ai/generate")
async def generate_content(
    request: AIGenerationRequest,
    current_user: Dict = Depends(get_current_user)
):
    # Mock AI generation
    mock_content = f"""
    <h1>AI Generated Email</h1>
    <p>Based on your prompt: "{request.prompt}"</p>
    <p>This is a {request.tone} email with {request.length} content.</p>
    <p>Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """
    
    mock_subject = f"AI Generated: {request.prompt[:50]}..."
    
    return {
        "content": mock_content,
        "subject": mock_subject,
        "suggestions": [
            "Add a clear call-to-action",
            "Include personalization tokens",
            "Consider A/B testing the subject line"
        ],
        "confidence": 0.85
    }

@app.post("/ai/improve")
async def improve_content(
    request: AIImprovementRequest,
    current_user: Dict = Depends(get_current_user)
):
    # Mock AI improvement
    improved_content = f"""
    <h1>Improved Email Content</h1>
    <p>Original content has been improved for {request.improvement_type}.</p>
    <p>Improved at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """
    
    suggestions = []
    if request.suggestions:
        suggestions = [
            "Consider adding more personalization",
            "Include a compelling subject line",
            "Add social proof elements"
        ]
    
    return {
        "content": improved_content,
        "subject": "Improved Subject Line",
        "suggestions": suggestions,
        "confidence": 0.90
    }

if __name__ == "__main__":
    # Initialize mock data
    init_mock_data()
    
    print("🚀 Starting Mock API Server...")
    print("📝 Available endpoints:")
    print("  - POST /auth/register")
    print("  - POST /auth/login")
    print("  - POST /auth/refresh")
    print("  - GET  /campaigns")
    print("  - POST /campaigns")
    print("  - GET  /campaigns/{id}")
    print("  - PUT  /campaigns/{id}")
    print("  - DELETE /campaigns/{id}")
    print("  - POST /campaigns/{id}/send")
    print("  - POST /ai/generate")
    print("  - POST /ai/improve")
    print("  - GET  /health")
    print("\n🔗 API Documentation: http://localhost:8000/docs")
    print("🌐 Mock server running on: http://localhost:8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
