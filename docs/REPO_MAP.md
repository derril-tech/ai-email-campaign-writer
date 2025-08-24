# 📁 Repository Map - AI Email Campaign Writer

## 🎯 **Project Overview**
This repository contains a full-stack AI-powered email campaign writer built with Next.js 14 (frontend) and FastAPI (backend). The application enables users to create, personalize, and optimize email campaigns using multiple AI models (GPT-4, Claude) with real-time analytics and predictive optimization.

## 🏗️ **Repository Structure**

### **Root Level**
```
ai-email-campaign-writer/
├── 📁 frontend/           # Next.js 14 frontend application
├── 📁 backend/            # FastAPI backend application  
├── 📁 packages/           # Shared packages (monorepo)
│   ├── 📁 ui/            # Shared UI components and design system
│   └── 📁 types/         # Shared TypeScript types
├── 📁 docs/               # Documentation and instructions
├── 📁 scripts/            # Development and testing scripts
├── 📁 .github/            # GitHub Actions CI/CD workflows
├── 📁 .devcontainer/      # VS Code Dev Container configuration
├── 📄 pnpm-workspace.yaml # Monorepo workspace configuration
├── 📄 package.json        # Root package.json with workspace scripts
├── 📄 .pre-commit-config.yaml # Pre-commit hooks configuration
├── 📄 docker-compose.dev.yml # Development Docker Compose
├── 📄 .nvmrc              # Node.js version specification
├── 📄 .editorconfig       # Editor configuration
├── 📄 .gitattributes      # Git attributes
├── 📄 README.md           # Main project documentation
├── 📄 BASELINE.md         # Project baseline and requirements
├── 📄 COMPLIANCE_AUDIT_REPORT.md # Compliance documentation
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
├── 📁 tests/              # Test files
│   ├── 📁 e2e/           # Playwright E2E tests
│   └── 📁 unit/          # Unit tests
├── 📄 package.json        # Frontend dependencies
├── 📄 tailwind.config.js  # Tailwind CSS configuration
├── 📄 tsconfig.json       # TypeScript configuration
├── 📄 playwright.config.ts # Playwright E2E testing configuration
└── 📄 .env.example        # Environment variables template
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
│   │   ├── 📄 campaign.py # Campaign model
│   │   ├── 📄 user.py     # User model
│   │   ├── 📄 copy_corpus.py # Copy corpus model (pgvector)
│   │   └── 📄 __init__.py
│   ├── 📁 schemas/        # Pydantic schemas
│   ├── 📁 services/       # Business logic services
│   │   ├── 📄 ai_service.py # AI framework orchestration
│   │   ├── 📄 email_service.py # Email sending service
│   │   └── 📄 analytics_service.py # Analytics service
│   ├── 📁 utils/          # Utility functions
│   └── 📄 main.py         # FastAPI application entry point
├── 📁 tests/              # Test files
│   ├── 📁 unit/           # Unit tests
│   ├── 📁 integration/    # Integration tests
│   └── 📁 fixtures/       # Test data
├── 📄 requirements.txt    # Python dependencies
├── 📄 pyproject.toml      # Project configuration
├── 📄 Dockerfile          # Docker configuration
├── 📄 docker-compose.yml  # Docker Compose setup
├── 📄 openapi.yaml        # OpenAPI specification
└── 📄 .env.example        # Environment variables template
```

### **Shared Packages Structure** (`packages/`)
```
packages/
├── 📁 ui/                 # Shared UI components
│   ├── 📁 src/            # Source code
│   │   ├── 📄 tokens.ts   # Design tokens and theme
│   │   ├── 📄 components/ # Shared components
│   │   └── 📄 utils/      # Utility functions
│   ├── 📄 package.json    # UI package dependencies
│   └── 📄 tsconfig.json   # TypeScript configuration
└── 📁 types/              # Shared TypeScript types
    ├── 📁 src/            # Source code
    │   ├── 📄 campaign.ts # Campaign types
    │   ├── 📄 user.ts     # User types
    │   └── 📄 api.ts      # API types
    ├── 📄 package.json    # Types package dependencies
    └── 📄 tsconfig.json   # TypeScript configuration
```

### **Scripts Structure** (`scripts/`)
```
scripts/
├── 📁 load-tests/         # k6 load testing scripts
│   ├── 📄 burst-sends.js  # Burst campaign creation tests
│   ├── 📄 sustained-sends.js # Sustained load tests
│   └── 📄 webhook-fan-in.js # Webhook processing tests
├── 📄 check-env.ts        # Environment variable validation
├── 📄 dev.sh              # Unix development script
└── 📄 dev.bat             # Windows development script
```

### **Documentation Structure** (`docs/`)
```
docs/
├── 📄 REPO_MAP.md         # This file - repository structure guide
├── 📄 API_SPEC.md         # Detailed API specification
├── 📄 CLAUDE.md           # Claude AI collaboration guidelines
├── 📄 PROMPT_DECLARATION.md # Project prompt for AI development
├── 📄 PRODUCT_BRIEF.md    # Product specifications and requirements
├── 📄 INFRASTRUCTURE_PLAN.md # 8-step infrastructure setup process
├── 📄 AI_FRAMEWORKS_SPECIFICATION.md # AI framework usage guide
├── 📄 SCREEN_ENDPOINT_DTO_MATRIX.md # Frontend-backend mapping
└── 📄 README.md           # Documentation overview
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
- **Testing**: Jest, React Testing Library, Playwright (E2E)

### **Backend Technologies**
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0 + pgvector
- **Cache**: Redis
- **AI Models**: OpenAI GPT-4, Anthropic Claude
- **AI Frameworks**: 
  - **LangChain**: Core orchestration, model selection, prompt management
  - **LangGraph**: Complex workflow orchestration, quality gates, A/B testing
  - **CrewAI**: Multi-agent collaboration (strategist, writer, brand specialist)
  - **LlamaIndex**: RAG for brand guidelines and historical data
  - **AutoGen**: Human-in-the-loop interactions and approvals
  - **pgvector**: Vector embeddings for brand voice similarity search
- **Authentication**: JWT with refresh tokens
- **Email**: SendGrid with retry + suppression handling
- **Background Tasks**: Celery + Redis
- **Templating**: Mustache.js (pystache) with dynamic variables
- **Real-time**: WebSocket (Socket.io) over ASGI
- **Testing**: pytest, pytest-asyncio

### **Infrastructure**
- **Deployment**: Vercel (Frontend), Render (Backend)
- **Database**: Managed PostgreSQL with pgvector extension
- **Cache**: Redis Cloud
- **Storage**: Cloud object storage
- **Monitoring**: Sentry, Prometheus, Grafana
- **CI/CD**: GitHub Actions with comprehensive testing
- **Load Testing**: k6 for performance testing
- **Development**: VS Code Dev Containers

## 🎯 **Key Features & Capabilities**

### **AI-Powered Content Generation**
- Multi-model AI orchestration (GPT-4, Claude)
- Brand voice consistency with pgvector embeddings
- Subject line optimization
- Content personalization
- A/B testing automation
- Copy corpus management

### **Campaign Management**
- Drag-and-drop email editor
- Template management with Mustache.js
- Audience segmentation
- Campaign scheduling
- Real-time analytics

### **Analytics & Optimization**
- Real-time performance tracking
- Predictive analytics with pgvector
- Engagement scoring
- ROI calculation
- Automated optimization

### **Enterprise Features**
- Multi-tenant architecture
- Role-based access control
- SOC 2 compliance
- GDPR compliance
- API rate limiting
- Load testing and performance monitoring

## 🚀 **Development Workflow**

### **Local Development**
1. **Monorepo Setup**: `pnpm install` (installs all packages)
2. **Frontend**: `pnpm dev:frontend` or `cd frontend && npm run dev`
3. **Backend**: `pnpm dev:backend` or `cd backend && python -m uvicorn app.main:app --reload`
4. **Database**: PostgreSQL + Redis (via Docker Compose)
5. **AI Services**: OpenAI + Anthropic API keys required

### **Testing**
- **Frontend Unit**: `pnpm test` (Jest + Testing Library)
- **Frontend E2E**: `pnpm test:e2e` (Playwright)
- **Backend**: `cd backend && pytest` (Unit + Integration tests)
- **Load Testing**: `k6 run scripts/load-tests/`

### **Quality Assurance**
- **Pre-commit Hooks**: Automatic linting, formatting, type checking
- **Environment Checks**: `pnpm check:env` validates all environment variables
- **Bundle Size**: CI checks for frontend bundle size limits
- **Load Testing**: CI runs k6 load tests on main branch

### **Deployment**
- **Frontend**: Vercel (automatic from main branch)
- **Backend**: Render (with health checks)
- **Database**: Managed PostgreSQL with automated backups
- **Monitoring**: Sentry for error tracking, Prometheus for metrics

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
- `packages/ui/src/components/` - Shared UI components
- `packages/types/src/` - Shared TypeScript types

### **⚠️ Review Required**
- `frontend/package.json` - Dependencies
- `backend/requirements.txt` - Python dependencies
- `frontend/tailwind.config.js` - Styling configuration
- `backend/app/core/config.py` - Application settings
- `packages/ui/package.json` - Shared UI dependencies
- `packages/types/package.json` - Shared types dependencies

### **🚫 Do Not Touch**
- `docs/` - Documentation files (except when explicitly requested)
- `README.md` - Main project documentation
- `API_SPEC.md` - API specification
- `CLAUDE.md` - Claude guidelines
- `.gitignore` - Git ignore rules
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose setup
- `.github/workflows/` - CI/CD configuration
- `.pre-commit-config.yaml` - Pre-commit hooks
- `pnpm-workspace.yaml` - Monorepo configuration

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
- **Base Unit**: 4px
- **Scale**: 0.25rem, 0.5rem, 0.75rem, 1rem, 1.25rem, 1.5rem, 2rem, 2.5rem, 3rem

### **Design Tokens**
All design tokens are centralized in `packages/ui/src/tokens.ts` and follow the product brief specifications.

## 🔄 **Monorepo Workflow**

### **Package Management**
- **Root**: `pnpm install` installs all workspace packages
- **Frontend**: `pnpm --filter frontend add <package>`
- **Backend**: `cd backend && pip install <package>`
- **UI Package**: `pnpm --filter @ai-email/ui add <package>`
- **Types Package**: `pnpm --filter @ai-email/types add <package>`

### **Development Scripts**
- **Start All**: `pnpm dev` (starts frontend and backend)
- **Frontend Only**: `pnpm dev:frontend`
- **Backend Only**: `pnpm dev:backend`
- **Build All**: `pnpm build`
- **Test All**: `pnpm test`
- **Lint All**: `pnpm lint`

### **Shared Dependencies**
- **UI Components**: Import from `@ai-email/ui`
- **Types**: Import from `@ai-email/types`
- **Design Tokens**: Import from `@ai-email/ui/tokens`

## 🧪 **Testing Strategy**

### **Frontend Testing**
- **Unit Tests**: Jest + React Testing Library for components
- **E2E Tests**: Playwright for critical user journeys
- **Visual Regression**: Playwright for UI consistency
- **Performance**: Lighthouse CI for performance monitoring

### **Backend Testing**
- **Unit Tests**: pytest for business logic
- **Integration Tests**: pytest-asyncio for API endpoints
- **Database Tests**: Test database models and migrations
- **AI Tests**: Mock AI service responses

### **Load Testing**
- **Burst Tests**: k6 scripts for sudden traffic spikes
- **Sustained Tests**: k6 scripts for continuous load
- **Webhook Tests**: k6 scripts for webhook processing
- **CI Integration**: Load tests run on main branch

### **Quality Gates**
- **Pre-commit**: Linting, formatting, type checking
- **CI/CD**: Full test suite, build verification, security scans
- **Performance**: Bundle size limits, load test thresholds
- **Security**: Dependency scanning, code analysis

---

**Last Updated**: December 2024
**Version**: 2.0.0 - Updated to reflect current monorepo infrastructure
