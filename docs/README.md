# AI Email Campaign Writer - PulseQuill

Legendary, enterprise-grade AI for writing, personalizing, and optimizing email at scale. **Write. Personalize. Ship. Learn — in real time.**

## 🎯 **Project Overview**

PulseQuill orchestrates GPT-4 + Claude for best-of-breed copy and brand consistency, enabling Fortune 500 growth, lifecycle, and CRM teams to create, personalize, and optimize email campaigns with real-time analytics and predictive optimization.

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
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0 + pgvector
- **Cache**: Redis (sessions, analytics, rate limiting)
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
- **Templating**: Mustache.js with dynamic variables
- **Real-time**: WebSocket (Socket.io) over ASGI

### **Infrastructure**
- **Deployment**: Vercel (Frontend), Render (Backend)
- **Database**: Managed PostgreSQL with pgvector
- **Cache**: Redis Cloud (sessions, analytics, rate limiting)
- **Monitoring**: Sentry, Prometheus, Grafana
- **Storage**: Cloud object storage for assets

## 📚 **Documentation**

### **Core Documentation**
- **[Product Brief](docs/PRODUCT_BRIEF.md)** - Product purpose, users, goals, and specifications
- **[Infrastructure Plan](docs/INFRASTRUCTURE_PLAN.md)** - 8-step infrastructure setup process
- **[API Specification](docs/API_SPEC.md)** - Complete API documentation
- **[Claude AI Guide](docs/CLAUDE.md)** - **SINGLE SOURCE OF TRUTH** for AI collaboration guidelines and rules

### **AI/ML Framework Documentation**
- **[AI Frameworks Specification](docs/AI_FRAMEWORKS_SPECIFICATION.md)** - **NEW**: Detailed framework usage and integration patterns
- **[Prompt Declaration](docs/PROMPT_DECLARATION.md)** - AI prompt engineering guidelines
- **[Repository Map](docs/REPO_MAP.md)** - File structure and editing boundaries

### **Development Documentation**
- **[Screen ↔ Endpoint ↔ DTO Matrix](docs/SCREEN_ENDPOINT_DTO_MATRIX.md)** - Frontend-backend mapping
- **[Baseline](BASELINE.md)** - Project baseline and requirements

## 🚀 **Quick Start**

### **Prerequisites**
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+ with pgvector extension
- Redis 7+

### **Development Setup**
```bash
# Clone repository
git clone <repository-url>
cd ai-email-campaign-writer

# Install dependencies
pnpm install

# Setup environment
cp .env.example .env.local
# Edit .env.local with your configuration

# Start development servers
pnpm dev  # Starts both frontend and backend
```

### **Environment Variables**
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

## 🎯 **Key Features**

### **AI-Powered Email Generation**
- **Multi-model orchestration**: GPT-4 + Claude for optimal content
- **Brand voice consistency**: pgvector embeddings for voice matching
- **Quality gates**: Automated compliance and brand checks
- **Human-in-the-loop**: Review and approval workflows

### **Real-time Analytics**
- **Live campaign tracking**: WebSocket-powered real-time updates
- **A/B testing**: Statistical significance testing with Wilson 95% CI
- **Predictive optimization**: ML-powered engagement prediction
- **Performance insights**: Comprehensive campaign analytics

### **Enterprise Features**
- **Compliance**: GDPR, CAN-SPAM, SOC 2 compliant
- **Scalability**: Production-ready infrastructure
- **Security**: JWT authentication, rate limiting, encryption
- **Integration**: SendGrid, webhooks, third-party APIs

## 📊 **Success Metrics**
- Copy production speed **+300%**
- Deliverability **>98%**
- Open rate **+15–30%**
- Time-to-ship **< 15 min** from brief to send

## 🤖 **AI/ML Framework Architecture**

PulseQuill uses a sophisticated multi-framework AI architecture to deliver enterprise-grade email campaign generation. Each framework serves a specific purpose in the AI pipeline:

### **🏗️ Framework Stack Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                    PulseQuill AI Stack                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   LangChain │  │   LangGraph │  │   CrewAI    │         │
│  │  (Core)     │  │  (Workflow) │  │ (Agents)    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │               │               │                  │
│         └───────────────┼───────────────┘                  │
│                         │                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  LlamaIndex │  │   AutoGen   │  │   pgvector  │         │
│  │   (RAG)     │  │ (Human-AI)  │  │ (Embedding) │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### **📋 Framework Purposes**

| Framework | Purpose | Use Cases |
|-----------|---------|-----------|
| **LangChain** | Core orchestration engine | Model selection, prompt management, basic AI operations |
| **LangGraph** | Complex workflow orchestration | Quality gates, A/B testing workflows, campaign lifecycle |
| **CrewAI** | Multi-agent collaboration | Strategist, writer, brand specialist agents |
| **LlamaIndex** | RAG (Retrieval-Augmented Generation) | Brand guidelines, historical data, compliance rules |
| **AutoGen** | Human-in-the-loop interactions | Content approval, strategy refinement, compliance review |
| **pgvector** | Vector embeddings & similarity | Brand voice matching, content similarity, performance prediction |

### **🔄 Workflow Integration Examples**

#### **Simple Email Generation** (LangChain Only)
```python
# Basic email generation using LangChain
async def simple_generation(request):
    model = choose_model(request.task, request.complexity)
    prompt = ChatPromptTemplate.from_template("Generate {task} for {audience}")
    chain = prompt | model | PydanticOutputParser()
    return await chain.ainvoke(request.data)
```

#### **Advanced Campaign Creation** (Multi-Framework)
```python
# Complex campaign using multiple frameworks
async def advanced_campaign_creation(request):
    # 1. RAG Context (LlamaIndex)
    brand_context = query_brand_context(request.brand_guidelines, knowledge_base)
    
    # 2. Multi-Agent Strategy (CrewAI)
    crew = create_campaign_crew()
    strategy_result = await crew.kickoff(request.data)
    
    # 3. Quality Gate Workflow (LangGraph)
    workflow = create_quality_gate_workflow()
    final_content = await workflow.ainvoke(strategy_result)
    
    # 4. Human Review (AutoGen) - if required
    if request.requires_human_review:
        approved_content = await human_review_workflow(final_content)
        final_content = approved_content
    
    return final_content
```

### **🎯 Framework Selection Matrix**

| Use Case | Primary Framework | Supporting Frameworks | Complexity |
|----------|------------------|---------------------|------------|
| Simple email generation | LangChain | - | Low |
| Brand voice matching | pgvector + LlamaIndex | LangChain | Medium |
| Multi-step quality gates | LangGraph | LangChain | Medium |
| Complex campaign strategy | CrewAI | LangChain, LlamaIndex | High |
| Human-in-the-loop review | AutoGen | LangChain | Medium |
| Historical performance analysis | pgvector | LlamaIndex | Low |

### **📚 Detailed Documentation**

- **[AI Frameworks Specification](docs/AI_FRAMEWORKS_SPECIFICATION.md)** - Complete framework usage guide with code examples
- **[Product Brief](docs/PRODUCT_BRIEF.md)** - AI content engine specifications
- **[API Specification](docs/API_SPEC.md)** - AI endpoints and integration patterns

## 🤝 **AI Collaboration**

This project follows the **80/20 rule**:
- **80%**: Infrastructure and scaffolding (completed)
- **20%**: AI implementation and business logic (for Claude)

See **[Claude AI Guide](docs/CLAUDE.md)** (single source of truth) for detailed collaboration guidelines and **[AI Frameworks Specification](docs/AI_FRAMEWORKS_SPECIFICATION.md)** for framework usage patterns.

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

---

**Ready to build PulseQuill?** Ship the five prompts above, and you'll generate a deployable, enterprise-grade AI email platform in hours—not months.
