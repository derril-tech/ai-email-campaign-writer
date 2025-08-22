# 🤖 Claude AI Collaboration Guide - AI Email Campaign Writer

## 🎯 **Project Overview**

**PulseQuill** is an enterprise-grade AI email campaign writer that orchestrates GPT-4 + Claude for best-of-breed copy and brand consistency. The platform enables Fortune 500 growth, lifecycle, and CRM teams to create, personalize, and optimize email campaigns at scale with real-time analytics and predictive optimization.

### **Core Value Proposition**
- **Multi-model AI orchestration** for optimal content generation
- **Real-time analytics** with predictive optimization
- **Enterprise compliance** (SOC 2, GDPR, CAN-SPAM)
- **Production-ready infrastructure** with 99.9% uptime SLA

### **Target Users**
- Fortune 500 marketing teams
- Growth and lifecycle teams
- CRM and sales teams
- High-volume email senders
- Marketing agencies

### **Success Metrics**
- Copy production speed **+300%**
- Deliverability **>98%**
- Open rate **+15–30%**
- Time-to-ship **< 15 min** from brief to send

## 🏗️ **Technology Stack**

### **Frontend**
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Data Fetching**: React Query
- **Forms**: React Hook Form
- **Animations**: Framer Motion
- **Real-time**: Socket.io Client

### **Backend**
- **Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0
- **Cache**: Redis
- **AI Models**: OpenAI GPT-4, Anthropic Claude
- **AI Frameworks**: LangChain, CrewAI, LangGraph, AutoGen, LlamaIndex
- **Authentication**: JWT with refresh tokens
- **Email**: SendGrid
- **Background Tasks**: Celery

### **Infrastructure**
- **Deployment**: Vercel (Frontend), Render (Backend)
- **Database**: Managed PostgreSQL
- **Cache**: Redis Cloud
- **Monitoring**: Sentry, Prometheus, Grafana

## 📁 **Folder & File Structure**

### **✅ Editable by Claude**
```
frontend/
├── app/                    # Next.js App Router pages
├── components/             # React components
├── hooks/                  # Custom React hooks
├── lib/                    # Utility functions
└── types/                  # TypeScript definitions

backend/
├── app/
│   ├── api/               # API endpoints
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
```

### **⚠️ Review Required**
```
frontend/
├── package.json           # Dependencies
├── tailwind.config.js     # Styling configuration
└── tsconfig.json          # TypeScript configuration

backend/
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
└── app/core/config.py     # Application settings
```

### **🚫 Do Not Touch**
```
docs/                      # Documentation files
README.md                  # Main project documentation
API_SPEC.md               # API specification
CLAUDE_INSTRUCTIONS.md    # Claude guidelines
.gitignore                # Git ignore rules
Dockerfile                # Docker configuration
docker-compose.yml        # Docker Compose setup
```

## 📝 **Coding Conventions**

### **Frontend (TypeScript/React)**
```typescript
// File naming: PascalCase for components, camelCase for utilities
// Component structure: functional components with hooks
// Props interface: IComponentNameProps
// State management: Zustand stores in /store directory

interface ICampaignFormProps {
  onSubmit: (data: CampaignData) => void;
  initialData?: Partial<CampaignData>;
}

const CampaignForm: React.FC<ICampaignFormProps> = ({ onSubmit, initialData }) => {
  // Component implementation
};

// Export pattern: named exports for components, default for pages
export { CampaignForm };
```

### **Backend (Python/FastAPI)**
```python
# File naming: snake_case
# Class naming: PascalCase
# Function naming: snake_case
# Constants: UPPER_SNAKE_CASE

# Import order: standard library, third-party, local
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.campaign import Campaign
from app.schemas.campaign import CampaignCreate, CampaignResponse

# Router definition
router = APIRouter(prefix="/campaigns", tags=["campaigns"])

# Function with type hints and docstrings
async def create_campaign(
    campaign_data: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CampaignResponse:
    """
    Create a new email campaign.
    
    Args:
        campaign_data: Campaign creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created campaign response
        
    Raises:
        HTTPException: If campaign creation fails
    """
    # Implementation
```

### **Database Models**
```python
# SQLAlchemy models with proper relationships
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="campaigns")
    events = relationship("EmailEvent", back_populates="campaign")
```

### **Pydantic Schemas**
```python
# Pydantic models for API validation
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

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

class CampaignResponse(BaseModel):
    id: str
    name: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## 🤝 **AI Collaboration Rules**

### **Response Format**
1. **Analysis**: Brief assessment of the request
2. **Implementation**: Code changes with clear explanations
3. **Testing**: Suggested test scenarios
4. **Documentation**: Update relevant documentation if needed

### **Edit Rules**
- **Full-file edits**: For new files or complete rewrites
- **Patch edits**: For specific function or component updates
- **Context preservation**: Always include surrounding context
- **Backward compatibility**: Maintain existing API contracts

### **Ambiguity Handling**
- **Ask clarifying questions** when requirements are unclear
- **Provide multiple options** when there are different approaches
- **Document assumptions** made during implementation
- **Suggest improvements** for better user experience

### **Code Quality Standards**
- **Type safety**: Full TypeScript/Python type coverage
- **Error handling**: Comprehensive error handling and validation
- **Performance**: Optimize for speed and efficiency
- **Accessibility**: WCAG AA compliance for all UI components
- **Security**: Follow security best practices

## 🔧 **Dependencies & Setup**

### **Required Environment Variables**
```bash
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Backend (.env)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
SENDGRID_API_KEY=your-sendgrid-key
```

### **Development Setup**
```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### **Database Setup**
```bash
# Create database
createdb ai_email_campaign

# Run migrations
cd backend
alembic upgrade head
```

## 🚀 **Workflow & Tools**

### **Development Workflow**
1. **Feature Development**: Create feature branch from main
2. **Implementation**: Follow coding conventions and patterns
3. **Testing**: Write unit and integration tests
4. **Documentation**: Update relevant documentation
5. **Review**: Create pull request with clear description

### **Frontend/Backend Boundary**
- **Frontend**: UI components, state management, API calls
- **Backend**: Business logic, database operations, external integrations
- **Shared**: Type definitions, validation schemas, constants

### **Deployment Notes**
- **Frontend**: Automatic deployment to Vercel on main branch
- **Backend**: Manual deployment to Render with health checks
- **Database**: Managed PostgreSQL with automated backups
- **Monitoring**: Sentry for error tracking, Prometheus for metrics

## 🧠 **Contextual Knowledge**

### **Business Logic Caveats**
- **Email Compliance**: All emails must include unsubscribe links
- **Rate Limiting**: Respect email provider rate limits
- **Data Privacy**: GDPR-compliant data handling required
- **Brand Consistency**: AI-generated content must match brand guidelines

### **Technical Constraints**
- **Token Limits**: AI models have 2000 token generation limits
- **API Rate Limits**: Respect OpenAI/Anthropic rate limits
- **Database Performance**: Optimize queries for large datasets
- **Real-time Updates**: WebSocket connections for live analytics

### **Domain Rules**
- **Campaign States**: draft → scheduled → sending → completed/failed
- **User Roles**: admin, user, premium with different permissions
- **Audience Segments**: Dynamic segmentation based on user behavior
- **A/B Testing**: Statistical significance required for winner selection

## 📚 **Examples**

### **Good AI Answer**
```typescript
// ✅ Clear, well-structured component with proper types
interface ICampaignCardProps {
  campaign: Campaign;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
}

const CampaignCard: React.FC<ICampaignCardProps> = ({ 
  campaign, 
  onEdit, 
  onDelete 
}) => {
  const { name, status, created_at, open_rate } = campaign;
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{name}</h3>
        <Badge variant={getStatusVariant(status)}>{status}</Badge>
      </div>
      
      <div className="space-y-2 text-sm text-gray-600">
        <p>Created: {formatDate(created_at)}</p>
        <p>Open Rate: {open_rate}%</p>
      </div>
      
      <div className="flex gap-2 mt-4">
        <Button onClick={() => onEdit(campaign.id)} size="sm">
          Edit
        </Button>
        <Button 
          onClick={() => onDelete(campaign.id)} 
          variant="destructive" 
          size="sm"
        >
          Delete
        </Button>
      </div>
    </div>
  );
};
```

### **Bad AI Answer**
```typescript
// ❌ Poor structure, no types, hardcoded values
const CampaignCard = ({ campaign }) => {
  return (
    <div>
      <h3>{campaign.name}</h3>
      <p>{campaign.status}</p>
      <button onClick={() => console.log('edit')}>Edit</button>
      <button onClick={() => console.log('delete')}>Delete</button>
    </div>
  );
};
```

### **Good Backend Answer**
```python
# ✅ Proper error handling, validation, and documentation
@router.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(
    campaign_data: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CampaignResponse:
    """
    Create a new email campaign for the authenticated user.
    
    Args:
        campaign_data: Validated campaign creation data
        db: Database session dependency
        current_user: Authenticated user from JWT token
        
    Returns:
        Created campaign with full details
        
    Raises:
        HTTPException: 400 if validation fails, 500 if creation fails
    """
    try:
        # Validate campaign data
        if not campaign_data.name.strip():
            raise HTTPException(
                status_code=400, 
                detail="Campaign name cannot be empty"
            )
        
        # Create campaign
        campaign = Campaign(
            name=campaign_data.name,
            subject=campaign_data.subject,
            html_content=campaign_data.html_content,
            owner_id=current_user.id
        )
        
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        
        return CampaignResponse.from_orm(campaign)
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create campaign: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to create campaign"
        )
```

### **Bad Backend Answer**
```python
# ❌ No error handling, no validation, poor structure
@router.post("/campaigns")
def create_campaign(campaign_data, db):
    campaign = Campaign(**campaign_data.dict())
    db.add(campaign)
    db.commit()
    return campaign
```

## 🎯 **Success Criteria**

### **Code Quality**
- **Type Safety**: 100% TypeScript/Python type coverage
- **Test Coverage**: ≥90% unit and integration test coverage
- **Performance**: Meet performance targets (p95 < 200ms)
- **Security**: Pass security audits and compliance checks

### **User Experience**
- **Accessibility**: WCAG AA compliance for all features
- **Performance**: Lighthouse score ≥ 90
- **Usability**: Intuitive interface with clear feedback
- **Reliability**: 99.9% uptime with graceful error handling

### **Business Impact**
- **Feature Completeness**: All MVP features implemented
- **Scalability**: Support for enterprise-level usage
- **Compliance**: Full GDPR, CAN-SPAM, SOC 2 compliance
- **Integration**: Seamless integration with existing workflows

---

**Last Updated**: December 2024
**Version**: 1.0.0
