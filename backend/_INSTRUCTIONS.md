# 🐍 Backend Development Instructions

## 📁 **Backend Structure Overview**

This directory contains the FastAPI backend application for PulseQuill - AI Email Campaign Writer.

### **Key Directories**
- `app/api/` - API routes and endpoints
- `app/core/` - Core configurations and utilities
- `app/models/` - Database models (SQLAlchemy)
- `app/schemas/` - Pydantic schemas for validation
- `app/services/` - Business logic services
- `app/utils/` - Utility functions

## 🎯 **Development Guidelines**

### **API Structure**
- RESTful API design
- Versioned endpoints (/v1/)
- Proper HTTP status codes
- Comprehensive error handling
- OpenAPI documentation

### **Database Design**
- SQLAlchemy 2.0 with async support
- PostgreSQL with pgvector for embeddings
- Proper relationships and constraints
- Migration management with Alembic
- Connection pooling

### **AI Integration**
- Multi-model orchestration (GPT-4, Claude)
- LangChain for workflow management
- CrewAI for multi-agent collaboration
- Vector embeddings for similarity search
- Rate limiting and caching

### **Security**
- JWT authentication with refresh tokens
- bcrypt password hashing
- Input validation with Pydantic
- Rate limiting and CORS
- Environment variable management

## 🚀 **TODO: Implementation Tasks**

### **High Priority**
- [ ] Complete authentication system (JWT + refresh)
- [ ] Implement campaign CRUD operations
- [ ] Build AI content generation service
- [ ] Create email delivery system (SendGrid)
- [ ] Add real-time analytics with WebSockets

### **Medium Priority**
- [ ] Implement audience management
- [ ] Build template system with Mustache.js
- [ ] Add A/B testing framework
- [ ] Create notification system
- [ ] Implement file upload and storage

### **Low Priority**
- [ ] Add advanced reporting APIs
- [ ] Implement team collaboration features
- [ ] Build webhook system
- [ ] Add multi-tenant support
- [ ] Create API rate limiting

## 🔧 **Technical Requirements**

### **Dependencies**
- FastAPI with async/await
- SQLAlchemy 2.0 for database
- PostgreSQL with pgvector
- Redis for caching and sessions
- Celery for background tasks
- OpenAI and Anthropic APIs

### **Code Quality**
- Black + isort + flake8 + mypy
- Type hints for all functions
- Comprehensive docstrings
- Unit and integration tests
- Performance monitoring

### **Performance Targets**
- p95 response time < 200ms
- Complex queries < 50ms
- Background job processing
- Database connection pooling

## 📝 **Coding Standards**

### **File Naming**
- Files: snake_case (e.g., `campaign_service.py`)
- Classes: PascalCase (e.g., `CampaignService`)
- Functions: snake_case (e.g., `create_campaign`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_RETRY_ATTEMPTS`)

### **Import Order**
```python
# Standard library imports
from typing import Optional, List
from datetime import datetime
import uuid

# Third-party imports
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Local imports
from app.core.database import get_db
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate
```

### **API Endpoint Structure**
```python
@router.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(
    campaign_data: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CampaignResponse:
    """
    Create a new email campaign.
    
    Args:
        campaign_data: Validated campaign data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created campaign response
        
    Raises:
        HTTPException: If creation fails
    """
    try:
        # Implementation
        pass
    except Exception as e:
        logger.error(f"Failed to create campaign: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### **Database Model Structure**
```python
class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="campaigns")
    events = relationship("EmailEvent", back_populates="campaign")
```

### **Pydantic Schema Structure**
```python
class CampaignCreate(BaseModel):
    name: str
    subject: str
    html_content: str
    audience_id: Optional[str] = None
    
    @validator('name')
    def validate_name(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Campaign name must be at least 3 characters')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Welcome Campaign",
                "subject": "Welcome to our platform!",
                "html_content": "<h1>Welcome!</h1>",
                "audience_id": "uuid-string"
            }
        }
```

## 🤖 **AI Service Integration**

### **Model Selection Logic**
```python
def choose_model(task: str, complexity: str) -> str:
    """Select appropriate AI model based on task and complexity."""
    if task in ["subject", "cta", "short_variant"]:
        return "gpt-4"
    elif complexity == "high" or task == "brand_alignment":
        return "claude"
    else:
        return "gpt-4"
```

### **Token Management**
```python
def calculate_tokens(text: str) -> int:
    """Calculate token count for text."""
    # Implementation for token counting
    pass

def truncate_to_token_limit(text: str, max_tokens: int = 2000) -> str:
    """Truncate text to fit within token limits."""
    # Implementation for token limiting
    pass
```

## 🔒 **Security Implementation**

### **Authentication**
```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### **Password Hashing**
```python
def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)
```

## 📊 **Database Design**

### **Core Tables**
- `users` - User accounts and authentication
- `campaigns` - Email campaigns
- `audiences` - Email lists and segments
- `email_events` - Email tracking events
- `templates` - Email templates
- `analytics` - Performance metrics

### **Indexes**
- Primary keys on all tables
- Foreign key indexes
- Composite indexes for common queries
- GIN indexes for JSONB fields
- Vector indexes for embeddings

## 🚀 **Background Tasks**

### **Celery Configuration**
```python
# Celery app configuration
celery_app = Celery(
    "ai_email_campaign",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.email", "app.tasks.ai"]
)
```

### **Task Structure**
```python
@celery_app.task(bind=True, max_retries=3)
def send_campaign_emails(self, campaign_id: str):
    """Send emails for a campaign."""
    try:
        # Implementation
        pass
    except Exception as exc:
        self.retry(countdown=60, exc=exc)
```

## 📈 **Monitoring & Logging**

### **Structured Logging**
```python
import structlog

logger = structlog.get_logger()

def log_campaign_creation(campaign_id: str, user_id: str):
    logger.info(
        "campaign_created",
        campaign_id=campaign_id,
        user_id=user_id,
        timestamp=datetime.utcnow()
    )
```

### **Performance Monitoring**
```python
from prometheus_client import Counter, Histogram

campaign_creation_counter = Counter('campaign_creations_total', 'Total campaigns created')
campaign_creation_duration = Histogram('campaign_creation_duration_seconds', 'Campaign creation time')
```

## 🧪 **Testing Strategy**

### **Unit Tests**
- Service layer testing
- Model validation
- Utility function testing
- Mock external dependencies

### **Integration Tests**
- API endpoint testing
- Database integration
- External service integration
- Authentication flow testing

### **Performance Tests**
- Load testing with k6
- Database query optimization
- API response time testing
- Background task performance

## 🚀 **Deployment**

### **Docker Configuration**
- Multi-stage builds
- Security scanning
- Health checks
- Environment-specific configs

### **Environment Variables**
- Database connections
- API keys and secrets
- Feature flags
- Monitoring configuration

---

**Last Updated**: December 2024
**Version**: 1.0.0
