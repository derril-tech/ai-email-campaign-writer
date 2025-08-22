# 📁 Repository Map - AI Email Campaign Writer

## 🎯 **Project Overview**
This repository contains a full-stack AI-powered email campaign writer built with Next.js 14 (frontend) and FastAPI (backend). The application enables users to create, personalize, and optimize email campaigns using multiple AI models (GPT-4, Claude) with real-time analytics and predictive optimization.

## 🏗️ **Repository Structure**

### **Root Level**
```
ai-email-campaign-writer/
├── 📁 frontend/           # Next.js 14 frontend application
├── 📁 backend/            # FastAPI backend application  
├── 📁 docs/               # Documentation and instructions
├── 📄 README.md           # Main project documentation
├── 📄 API_SPEC.md         # API specification and endpoints
├── 📄 CLAUDE_INSTRUCTIONS.md # Claude AI collaboration guidelines
└── 📄 REPO_MAD.md         # Repository management documentation
```

### **Frontend Structure** (`frontend/`)
```
frontend/
├── 📁 app/                # Next.js App Router pages
│   ├── 📄 globals.css     # Global styles
│   ├── 📄 layout.tsx      # Root layout component
│   └── 📄 page.tsx        # Home page
├── 📁 components/         # React components
│   ├── 📁 auth/           # Authentication components
│   ├── 📁 dashboard/      # Dashboard components
│   ├── 📁 forms/          # Form components
│   ├── 📁 layout/         # Layout components
│   ├── 📁 providers/      # Context providers
│   ├── 📁 sections/       # Page sections
│   └── 📁 ui/             # Reusable UI components
├── 📁 hooks/              # Custom React hooks
├── 📁 lib/                # Utility libraries
├── 📁 types/              # TypeScript type definitions
├── 📄 package.json        # Frontend dependencies
├── 📄 tailwind.config.js  # Tailwind CSS configuration
├── 📄 tsconfig.json       # TypeScript configuration
└── 📄 env.example         # Environment variables template
```

### **Backend Structure** (`backend/`)
```
backend/
├── 📁 app/                # Main application code
│   ├── 📁 api/            # API routes and endpoints
│   │   └── 📁 v1/         # API version 1
│   │       ├── 📁 endpoints/ # API endpoint modules
│   │       └── 📄 api.py  # API router configuration
│   ├── 📁 core/           # Core configurations
│   │   ├── 📄 config.py   # Application settings
│   │   ├── 📄 database.py # Database configuration
│   │   ├── 📄 dependencies.py # Dependency injection
│   │   ├── 📄 middleware.py # Custom middleware
│   │   ├── 📄 redis.py    # Redis configuration
│   │   └── 📄 security.py # Security utilities
│   ├── 📁 models/         # Database models
│   ├── 📁 schemas/        # Pydantic schemas
│   ├── 📁 services/       # Business logic services
│   ├── 📁 utils/          # Utility functions
│   └── 📄 main.py         # FastAPI application entry point
├── 📄 requirements.txt    # Python dependencies
├── 📄 pyproject.toml      # Project configuration
├── 📄 Dockerfile          # Docker configuration
├── 📄 docker-compose.yml  # Docker Compose setup
└── 📄 env.example         # Environment variables template
```

### **Documentation Structure** (`docs/`)
```
docs/
├── 📄 REPO_MAP.md         # This file - repository structure guide
├── 📄 API_SPEC.md         # Detailed API specification
├── 📄 CLAUDE.md           # Claude AI collaboration guidelines
└── 📄 PROMPT_DECLARATION.md # Project prompt for AI development
```

## 🔧 **Technology Stack**

### **Frontend Technologies**
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Data Fetching**: React Query
- **Forms**: React Hook Form
- **Animations**: Framer Motion
- **UI Components**: Headless UI, Radix UI
- **Real-time**: Socket.io Client

### **Backend Technologies**
- **Framework**: FastAPI (Python 3.9+)
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0
- **Cache**: Redis
- **AI Models**: OpenAI GPT-4, Anthropic Claude
- **AI Frameworks**: LangChain, CrewAI, LangGraph, AutoGen, LlamaIndex
- **Authentication**: JWT with refresh tokens
- **Email**: SendGrid
- **Background Tasks**: Celery
- **Monitoring**: Sentry, Loguru

### **Infrastructure**
- **Deployment**: Vercel (Frontend), Render (Backend)
- **Database**: Managed PostgreSQL
- **Cache**: Redis Cloud
- **Storage**: Cloud object storage
- **Monitoring**: Prometheus, Grafana

## 🎯 **Key Features & Capabilities**

### **AI-Powered Content Generation**
- Multi-model AI orchestration (GPT-4, Claude)
- Brand voice consistency
- Subject line optimization
- Content personalization
- A/B testing automation

### **Campaign Management**
- Drag-and-drop email editor
- Template management
- Audience segmentation
- Campaign scheduling
- Real-time analytics

### **Analytics & Optimization**
- Real-time performance tracking
- Predictive analytics
- Engagement scoring
- ROI calculation
- Automated optimization

### **Enterprise Features**
- Multi-tenant architecture
- Role-based access control
- SOC 2 compliance
- GDPR compliance
- API rate limiting

## 🚀 **Development Workflow**

### **Local Development**
1. **Frontend**: `cd frontend && npm run dev`
2. **Backend**: `cd backend && uvicorn app.main:app --reload`
3. **Database**: PostgreSQL + Redis
4. **AI Services**: OpenAI + Anthropic API keys required

### **Testing**
- **Frontend**: `npm test` (Jest + Testing Library)
- **Backend**: `pytest` (Unit + Integration tests)
- **E2E**: Playwright for end-to-end testing

### **Deployment**
- **Frontend**: Vercel (automatic from main branch)
- **Backend**: Render (with health checks)
- **Database**: Managed PostgreSQL with automated backups

## 📋 **File Ownership & Editing Rules**

### **✅ Editable by Claude**
- `frontend/components/` - React components
- `frontend/app/` - Next.js pages and layouts
- `frontend/hooks/` - Custom React hooks
- `frontend/lib/` - Utility functions
- `backend/app/api/` - API endpoints
- `backend/app/services/` - Business logic
- `backend/app/models/` - Database models
- `backend/app/schemas/` - Pydantic schemas

### **⚠️ Review Required**
- `frontend/package.json` - Dependencies
- `backend/requirements.txt` - Python dependencies
- `frontend/tailwind.config.js` - Styling configuration
- `backend/app/core/config.py` - Application settings

### **🚫 Do Not Touch**
- `docs/` - Documentation files (except when explicitly requested)
- `README.md` - Main project documentation
- `API_SPEC.md` - API specification
- `CLAUDE_INSTRUCTIONS.md` - Claude guidelines
- `.gitignore` - Git ignore rules
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose setup

## 🎨 **Design System**

### **Color Palette**
- **Primary**: #3B82F6 (Blue)
- **Secondary**: #8B5CF6 (Purple)
- **Success**: #10B981 (Green)
- **Warning**: #F59E0B (Orange)
- **Error**: #EF4444 (Red)

### **Typography**
- **Font**: Inter
- **Base Size**: 14px
- **Scale**: 1.25 modular scale

### **Spacing**
- **Grid**: 4px increments (4, 8, 16, 24, 32, 48, 64)

### **Breakpoints**
- **Mobile**: 320px
- **Tablet**: 768px
- **Desktop**: 1024px
- **Large**: 1440px

## 🔒 **Security & Compliance**

### **Authentication**
- JWT tokens (15-minute access, 7-day refresh)
- bcrypt password hashing (cost 12)
- Two-factor authentication support

### **API Security**
- Rate limiting (100/min, 1000/hr, 10000/day)
- CORS allowlist
- HSTS headers
- Input validation with Pydantic

### **Data Protection**
- AES-256 encryption at rest
- TLS 1.3 in transit
- GDPR-compliant data handling
- SOC 2 controls

### **Email Security**
- SPF, DKIM, DMARC configuration
- CAN-SPAM compliance
- Unsubscribe handling
- Suppression list management

## 📊 **Performance Targets**

### **Frontend**
- Lighthouse score ≥ 90
- Initial bundle < 500KB
- Time to Interactive < 3s
- Core Web Vitals compliance

### **Backend**
- p95 response time < 200ms
- Complex queries < 50ms
- Background job processing
- Database connection pooling

### **Email Delivery**
- Delivery rate > 98%
- Bounce rate < 2%
- Spam score < 3
- Automated retry logic

## 🤝 **Collaboration Guidelines**

### **Code Standards**
- **Frontend**: ESLint + Prettier
- **Backend**: Black + isort + flake8 + mypy
- **Testing**: ≥90% coverage
- **Documentation**: JSDoc + docstrings

### **Git Workflow**
- Feature branches from main
- Pull request reviews required
- Conventional commits
- Automated testing on PR

### **AI Collaboration**
- Clear TODO markers
- Folder-level instructions
- Contextual comments
- Progressive enhancement

---

**Last Updated**: December 2024
**Version**: 1.0.0
