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
- **Framework**: FastAPI (Python 3.11+) with async/await
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0 + pgvector
- **Cache**: Redis for sessions, caching, rate limiting
- **AI Integration**: Multi-model orchestration (GPT-4, Claude, LangChain, LangGraph, CrewAI, LlamaIndex, AutoGen)
- **Performance**: p95 < 200ms, complex queries < 50ms
- **Security**: JWT auth, bcrypt, rate limiting, CORS

### **Data Architecture**
- **Primary Database**: PostgreSQL with pgvector extension for embeddings
- **Caching Layer**: Redis with TTL policies
- **Background Jobs**: Celery with Redis broker
- **Real-time**: WebSocket connections for live analytics
- **Vector Storage**: pgvector for brand voice similarity search

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
- **LangChain**: Core workflow orchestration, model selection, prompt management
- **LangGraph**: Complex workflow management, quality gates, A/B testing orchestration
- **CrewAI**: Multi-agent collaboration (Strategist, Writer, Brand Specialist, Manager)
- **LlamaIndex**: Knowledge base and document processing, RAG for brand guidelines
- **AutoGen**: Human-in-the-loop interactions and approvals
- **pgvector**: Vector embeddings for brand voice similarity search

### **AI Framework Selection Matrix**
```python
# Framework selection based on task complexity
def select_framework(task: str, complexity: str, requires_rag: bool) -> dict:
    if complexity == "simple":
        return {"primary": "langchain", "supporting": []}
    elif complexity == "complex" and requires_rag:
        return {"primary": "crewai", "supporting": ["llamaindex", "langgraph"]}
    elif complexity == "workflow":
        return {"primary": "langgraph", "supporting": ["langchain"]}
    elif requires_human_review:
        return {"primary": "autogen", "supporting": ["langchain"]}
    else:
        return {"primary": "langchain", "supporting": []}
```

## 📚 **Copy Corpus & Vector Operations**

### **pgvector Integration**
- **Embedding Dimension**: 1536 (OpenAI embedding size)
- **Similarity Search**: Cosine similarity for brand voice matching
- **Performance**: < 100ms for similarity queries
- **Indexing**: HNSW index for fast approximate nearest neighbor search

### **Copy Corpus Management**
```python
# Copy corpus operations
class CopyCorpusService:
    async def add_entry(self, content: str, copy_type: str, performance_score: str = None):
        # Generate embedding using OpenAI
        embedding = await self.generate_embedding(content)
        # Store in pgvector with metadata
        return await self.store_with_embedding(content, embedding, copy_type, performance_score)
    
    async def find_similar(self, query: str, limit: int = 10, min_score: float = 0.7):
        # Generate query embedding
        query_embedding = await self.generate_embedding(query)
        # Search pgvector for similar content
        return await self.vector_search(query_embedding, limit, min_score)
```

### **Brand Voice Consistency**
- **Vector Similarity**: Match new content against historical high-performing copy
- **Performance Tracking**: Store engagement metrics with copy entries
- **Automatic Tagging**: Categorize copy by type, performance, and brand voice
- **Recommendation Engine**: Suggest similar high-performing content

## 🎨 **Template Management (Mustache.js)**

### **Dynamic Templating**
```javascript
// Template rendering with Mustache.js
const template = "Hello {{first_name}}, welcome to {{company_name}}!";
const variables = {
  first_name: "John",
  company_name: "Acme Corp"
};
const rendered = Mustache.render(template, variables);
```

### **Template Features**
- **Variable Validation**: Ensure all required variables are provided
- **Preview Mode**: Render templates with sample data
- **Category Management**: Organize templates by use case
- **Version Control**: Track template changes and performance

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

## 📊 **Performance & Scalability**

### **Frontend Performance**
- **Bundle Size**: < 500KB initial bundle
- **Time to Interactive**: < 3 seconds
- **Lighthouse Score**: ≥ 90 across all metrics
- **Core Web Vitals**: Optimized for LCP, FID, CLS

### **Backend Performance**
- **Response Time**: p95 < 200ms for API endpoints
- **Database Queries**: < 50ms for complex operations
- **AI Generation**: < 30 seconds for complex workflows
- **Vector Search**: < 100ms for similarity queries

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
- **Accessibility Tests**: Manual testing for WCAG compliance
- **Performance Tests**: Lighthouse CI for performance monitoring

### **Backend Testing**
- **Unit Tests**: Service layer, model validation, utility functions
- **Integration Tests**: API endpoints, database operations, external services
- **Performance Tests**: Load testing with k6, database query optimization
- **Security Tests**: Authentication, authorization, input validation
- **AI Tests**: Mock AI service responses, framework integration

### **Load Testing (k6)**
```javascript
// k6 load testing scenarios
export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up
    { duration: '5m', target: 100 }, // Sustained load
    { duration: '2m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200'],
    http_req_failed: ['rate<0.1'],
  },
};
```

### **Test Coverage Requirements**
- **Minimum Coverage**: ≥ 90% for both frontend and backend
- **Critical Paths**: 100% coverage for authentication, payment, email sending
- **Edge Cases**: Comprehensive error handling and boundary testing
- **Load Testing**: CI integration with k6 for performance validation

## 🚀 **Deployment & DevOps**

### **Frontend Deployment**
- **Platform**: Vercel with automatic deployments
- **Build Process**: Next.js build with optimization
- **Environment**: Production, staging, development environments
- **Monitoring**: Vercel Analytics, Sentry error tracking

### **Backend Deployment**
- **Platform**: Render with health checks
- **Container**: Docker with multi-stage builds
- **Database**: Managed PostgreSQL with pgvector extension
- **Monitoring**: Prometheus metrics, Grafana dashboards

### **CI/CD Pipeline**
- **GitHub Actions**: Automated testing, linting, building
- **Quality Gates**: Code coverage, security scanning, performance testing
- **Load Testing**: k6 integration for performance validation
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
- Template management system with Mustache.js
- A/B testing framework with statistical significance
- Campaign scheduling and automation

### **AI Content Generation**
- Multi-model content generation (GPT-4, Claude)
- Brand voice consistency enforcement with pgvector
- Subject line optimization
- Content personalization
- Performance prediction
- Copy corpus integration

### **Analytics & Reporting**
- Real-time campaign analytics
- Email event tracking (send, deliver, open, click, bounce)
- Performance dashboards
- ROI calculation
- Predictive analytics with vector similarity

### **Audience Management**
- Contact list management
- Audience segmentation
- Import/export functionality
- Subscription management
- GDPR compliance tools

### **Load Testing & Performance**
- k6 load testing scenarios (burst, sustained, webhook)
- Performance monitoring and alerting
- Capacity planning and scaling
- Performance regression detection

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
- **Vector Search**: < 100ms for similarity queries

### **Database Constraints**
- **Connection Pooling**: Max 20 connections per instance
- **Query Timeout**: 30 seconds maximum
- **Index Optimization**: B-tree, GIN, and vector indexes
- **Backup Strategy**: Daily automated backups
- **pgvector**: HNSW index for fast similarity search

### **Load Testing Constraints**
- **k6 Scenarios**: Burst, sustained, and webhook testing
- **Performance Thresholds**: p95 < 200ms, error rate < 5%
- **CI Integration**: Automated load testing on main branch
- **Monitoring**: Real-time performance metrics and alerting

## 🎯 **Success Criteria**

### **Performance Metrics**
- **Frontend**: Lighthouse ≥ 90, TTI < 3s, bundle < 500KB
- **Backend**: p95 < 200ms, AI generation < 30s, vector search < 100ms
- **Email**: Delivery rate > 98%, bounce rate < 2%
- **Load Testing**: All k6 scenarios pass performance thresholds

### **Quality Metrics**
- **Test Coverage**: ≥ 90% for frontend and backend
- **Security**: Pass security audits and compliance checks
- **Accessibility**: WCAG AA compliance
- **Reliability**: 99.9% uptime with graceful error handling

### **Business Metrics**
- **User Experience**: Intuitive interface with clear feedback
- **Feature Completeness**: All MVP features implemented
- **Scalability**: Support for enterprise-level usage
- **Compliance**: Full GDPR, CAN-SPAM, SOC 2 compliance

---

**Last Updated**: December 2024
**Version**: 2.0.0 - Updated to reflect current infrastructure with k6, pgvector, and advanced AI frameworks
