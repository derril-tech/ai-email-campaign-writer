# 🎯 AI Development Prompt Declaration - PulseQuill

## 🚀 **Project Mission**

Build **PulseQuill** - an enterprise-grade AI email campaign writer that orchestrates GPT-4 + Claude for best-of-breed copy and brand consistency. The platform enables Fortune 500 growth, lifecycle, and CRM teams to create, personalize, and optimize email campaigns at scale with real-time analytics and predictive optimization.

## 🏗️ **Architecture Requirements**

### **Frontend Architecture**
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript with strict mode
- **Styling**: Tailwind CSS with design tokens
- **State Management**: Zustand for global state, React Query for server state
- **Components**: Atomic design with WCAG AA accessibility
- **Performance**: Lighthouse ≥ 90, bundle < 500KB, TTI < 3s

### **Backend Architecture**
- **Framework**: FastAPI (Python 3.9+) with async/await
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0 + pgvector
- **Cache**: Redis for sessions, caching, rate limiting
- **AI Integration**: Multi-model orchestration (GPT-4, Claude, LangChain, CrewAI)
- **Performance**: p95 < 200ms, complex queries < 50ms
- **Security**: JWT auth, bcrypt, rate limiting, CORS

### **Data Architecture**
- **Primary Database**: PostgreSQL with proper indexing
- **Vector Store**: pgvector for embeddings and similarity search
- **Caching Layer**: Redis with TTL policies
- **Background Jobs**: Celery with Redis broker
- **Real-time**: WebSocket connections for live analytics

## 🎨 **Design System & UX**

### **Design Tokens**
- **Colors**: Primary #3B82F6, Secondary #8B5CF6, Success #10B981, Warning #F59E0B, Error #EF4444
- **Typography**: Inter font, 14px base, 1.25 modular scale
- **Spacing**: 4px grid system (4, 8, 16, 24, 32, 48, 64)
- **Breakpoints**: 320px, 768px, 1024px, 1440px

### **UX Principles**
- **Accessibility**: WCAG AA compliance, keyboard navigation, screen reader support
- **Performance**: Skeleton loading, optimistic updates, progressive enhancement
- **Error Handling**: User-friendly error messages, graceful degradation
- **Responsive Design**: Mobile-first approach with touch-friendly interactions

### **Interaction Patterns**
- **Forms**: React Hook Form with validation, real-time feedback
- **Navigation**: Breadcrumbs, clear hierarchy, consistent patterns
- **Feedback**: Toast notifications, loading states, progress indicators
- **Data Display**: Pagination, filtering, sorting, search functionality

## 🤖 **AI Integration Requirements**

### **Model Selection Logic**
```python
# Task-based model selection
def choose_model(task: str, complexity: str) -> str:
    if task in ["subject", "cta", "short_variant"]:
        return "gpt-4"  # Punchy creativity
    elif complexity == "high" or task == "brand_alignment":
        return "claude"  # Nuanced style control
    else:
        return "gpt-4"  # Default choice
```

### **Token Management**
- **Generation Limit**: ≤ 2000 tokens per generation
- **Dynamic Temperature**: 0.3 (compliance) → 0.9 (creative)
- **Auto-trimming**: Automatic content truncation to fit limits
- **Caching**: 24-hour cache for repeated generations

### **Quality Gates**
1. **LLM Draft** → 2. **Style Lint** → 3. **Fact/URL Validator** → 4. **Compliance Footer** → 5. **Human Preview**

### **AI Frameworks Integration**
- **LangChain**: Core workflow orchestration
- **CrewAI**: Multi-agent collaboration (Strategist, Writer, Specialist, Manager)
- **LangGraph**: Complex workflow management
- **AutoGen**: Human-in-the-loop interactions
- **LlamaIndex**: Knowledge base and document processing

## 🔒 **Security & Compliance**

### **Authentication & Authorization**
- **JWT Tokens**: 15-minute access, 7-day refresh
- **Password Security**: bcrypt with cost 12
- **Role-Based Access**: Admin, User, Premium permissions
- **Two-Factor Auth**: TOTP support for enhanced security

### **API Security**
- **Rate Limiting**: 100/min, 1000/hr, 10000/day per user
- **CORS**: Strict allowlist for production domains
- **Input Validation**: Pydantic schemas with comprehensive validation
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries

### **Data Protection**
- **Encryption**: AES-256 at rest, TLS 1.3 in transit
- **GDPR Compliance**: Data export, deletion, consent management
- **CAN-SPAM Compliance**: Unsubscribe links, sender identification
- **SOC 2 Controls**: Security, availability, processing integrity

### **Email Security**
- **Authentication**: SPF, DKIM, DMARC configuration
- **Deliverability**: Bounce handling, suppression lists
- **Compliance**: Unsubscribe management, opt-out tracking

## 📊 **Performance Requirements**

### **Frontend Performance**
- **Lighthouse Score**: ≥ 90 across all metrics
- **Bundle Size**: Initial bundle < 500KB
- **Time to Interactive**: < 3 seconds
- **Core Web Vitals**: LCP < 2.5s, FID < 100ms, CLS < 0.1

### **Backend Performance**
- **API Response Time**: p95 < 200ms
- **Database Queries**: Complex queries < 50ms
- **Background Jobs**: Celery worker processing
- **Caching**: Redis with appropriate TTL policies

### **Email Delivery Performance**
- **Delivery Rate**: > 98%
- **Bounce Rate**: < 2%
- **Spam Score**: < 3
- **Retry Logic**: Automated retry with exponential backoff

## 🧪 **Testing Strategy**

### **Frontend Testing**
- **Unit Tests**: Component rendering, user interactions, state changes
- **Integration Tests**: API integration, form submissions, navigation
- **E2E Tests**: Playwright for critical user journeys
- **Accessibility Tests**: axe-core for WCAG compliance

### **Backend Testing**
- **Unit Tests**: Service layer, model validation, utility functions
- **Integration Tests**: API endpoints, database operations, external services
- **Performance Tests**: Load testing with k6, database query optimization
- **Security Tests**: Authentication, authorization, input validation

### **Test Coverage Requirements**
- **Minimum Coverage**: ≥ 90% for both frontend and backend
- **Critical Paths**: 100% coverage for authentication, payment, email sending
- **Edge Cases**: Comprehensive error handling and boundary testing

## 🚀 **Deployment & DevOps**

### **Frontend Deployment**
- **Platform**: Vercel with automatic deployments
- **Build Process**: Next.js build with optimization
- **Environment**: Production, staging, development environments
- **Monitoring**: Vercel Analytics, Sentry error tracking

### **Backend Deployment**
- **Platform**: Render with health checks
- **Container**: Docker with multi-stage builds
- **Database**: Managed PostgreSQL with automated backups
- **Monitoring**: Prometheus metrics, Grafana dashboards

### **CI/CD Pipeline**
- **GitHub Actions**: Automated testing, linting, building
- **Quality Gates**: Code coverage, security scanning, performance testing
- **Deployment**: Blue/green deployment for zero downtime
- **Rollback**: Automatic rollback on health check failures

## 📋 **Core Features Implementation**

### **Authentication System**
- User registration with email verification
- JWT-based authentication with refresh tokens
- Password reset functionality
- Two-factor authentication (TOTP)
- Social login integration (Google, Microsoft)

### **Campaign Management**
- Campaign creation wizard with AI assistance
- Drag-and-drop email editor
- Template management system
- A/B testing framework
- Campaign scheduling and automation

### **AI Content Generation**
- Multi-model content generation (GPT-4, Claude)
- Brand voice consistency enforcement
- Subject line optimization
- Content personalization
- Performance prediction

### **Analytics & Reporting**
- Real-time campaign analytics
- Email event tracking (send, deliver, open, click, bounce)
- Performance dashboards
- ROI calculation
- Predictive analytics

### **Audience Management**
- Contact list management
- Audience segmentation
- Import/export functionality
- Subscription management
- GDPR compliance tools

## 🔧 **Technical Constraints**

### **Browser Support**
- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Chrome Mobile 90+
- **Accessibility**: Screen readers, keyboard navigation, high contrast

### **API Constraints**
- **Rate Limits**: Respect OpenAI/Anthropic API limits
- **Token Limits**: 2000 tokens per generation
- **Response Time**: < 30 seconds for AI generation
- **Error Handling**: Graceful degradation on API failures

### **Database Constraints**
- **Connection Pooling**: Max 20 connections per instance
- **Query Timeout**: 30 seconds maximum
- **Index Optimization**: B-tree, GIN, and vector indexes
- **Backup Strategy**: Daily automated backups

## 🎯 **Success Criteria**

### **Business Metrics**
- **Copy Production Speed**: +300% improvement
- **Email Deliverability**: > 98% success rate
- **Open Rate Improvement**: +15-30% increase
- **Time to Ship**: < 15 minutes from brief to send

### **Technical Metrics**
- **System Uptime**: 99.9% availability
- **API Performance**: p95 < 200ms response time
- **Test Coverage**: ≥ 90% code coverage
- **Security Score**: A+ rating on security scans

### **User Experience Metrics**
- **Lighthouse Score**: ≥ 90 across all metrics
- **Accessibility**: WCAG AA compliance
- **User Satisfaction**: > 4.5/5 rating
- **Feature Adoption**: > 80% of users use AI features

## 📝 **Development Guidelines**

### **Code Quality Standards**
- **TypeScript**: Strict mode with comprehensive types
- **Python**: Type hints, docstrings, comprehensive error handling
- **Testing**: Unit, integration, and E2E tests
- **Documentation**: Inline comments, API documentation, README files

### **Git Workflow**
- **Branch Strategy**: Feature branches from main
- **Commit Messages**: Conventional commits format
- **Pull Requests**: Required reviews, automated testing
- **Release Process**: Semantic versioning, changelog generation

### **Code Review Process**
- **Review Requirements**: At least one approval required
- **Quality Gates**: Automated testing, linting, security scanning
- **Documentation**: Updated documentation for new features
- **Performance**: Performance impact assessment

---

**This prompt declaration serves as the comprehensive guide for AI development of PulseQuill. All implementations must adhere to these specifications to ensure consistency, quality, and alignment with the project's enterprise-grade requirements.**
