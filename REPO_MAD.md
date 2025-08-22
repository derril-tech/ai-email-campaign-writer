# AI Email Campaign Writer - Repository Documentation

## 🏗️ Project Architecture

This is a full-stack AI Email Campaign Writer application built with modern technologies and best practices.

### Frontend Architecture (Next.js 14)
```
frontend/
├── app/                    # Next.js App Router (Pages & Layouts)
│   ├── (auth)/            # Authentication routes
│   ├── (dashboard)/       # Protected dashboard routes
│   ├── api/               # API routes (if needed)
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Landing page
├── components/            # Reusable React components
│   ├── ui/               # Base UI components
│   ├── forms/            # Form components
│   ├── layout/           # Layout components
│   ├── dashboard/        # Dashboard-specific components
│   └── auth/             # Authentication components
├── hooks/                # Custom React hooks
├── lib/                  # Utility libraries & configurations
├── types/                # TypeScript type definitions
├── store/                # Zustand state management
└── styles/               # Additional styles
```

### Backend Architecture (FastAPI)
```
backend/
├── app/
│   ├── api/              # API routes & endpoints
│   │   ├── v1/          # API version 1
│   │   │   ├── auth/    # Authentication endpoints
│   │   │   ├── campaigns/ # Campaign management
│   │   │   ├── ai/      # AI content generation
│   │   │   ├── users/   # User management
│   │   │   └── analytics/ # Analytics & reporting
│   ├── core/            # Core configurations
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic services
│   ├── utils/           # Utility functions
│   └── main.py          # FastAPI application entry
├── alembic/             # Database migrations
└── tests/               # Test files
```

## 🚀 Key Features Implementation

### 1. Authentication System
- **JWT-based authentication** with refresh tokens
- **Role-based access control** (Admin, User, Premium)
- **Social login integration** (Google, GitHub)
- **Password reset functionality**

### 2. Campaign Management
- **Campaign creation wizard** with step-by-step guidance
- **Template library** with customizable email templates
- **Audience segmentation** and targeting
- **Campaign scheduling** and automation
- **A/B testing** capabilities

### 3. AI Content Generation
- **Multi-AI provider support** (OpenAI GPT-4, Anthropic Claude)
- **Context-aware content generation** based on:
  - Target audience demographics
  - Industry/niche
  - Campaign goals
  - Brand voice and tone
- **Content optimization** for email deliverability
- **Subject line generation** with A/B testing
- **Personalization tokens** and dynamic content

### 4. Email Delivery System
- **Multi-provider support** (SendGrid, SMTP, AWS SES)
- **Email validation** and verification
- **Bounce handling** and list cleaning
- **Delivery tracking** and analytics
- **Compliance** (CAN-SPAM, GDPR)

### 5. Analytics & Reporting
- **Real-time campaign metrics**
- **Email performance tracking**
- **Audience engagement analytics**
- **ROI calculation** and reporting
- **Export capabilities** (PDF, CSV, Excel)

## 🛠️ Technology Stack Details

### Frontend Technologies
- **Next.js 14** with App Router for optimal performance and SEO
- **TypeScript** for type safety and better developer experience
- **Tailwind CSS** for utility-first styling with custom design system
- **Framer Motion** for smooth animations and micro-interactions
- **Zustand** for lightweight state management
- **React Query** for server state management and caching
- **React Hook Form** for performant form handling
- **Socket.io Client** for real-time updates
- **React Dropzone** for file uploads
- **React Select** for advanced select components
- **Date-fns** for date manipulation
- **React Markdown** for content rendering

### Backend Technologies
- **FastAPI** with async/await for high-performance API
- **SQLAlchemy 2.0** with async support for database operations
- **PostgreSQL** with pgvector for vector similarity search
- **Redis** for caching, sessions, and background task queues
- **Celery** with Redis for background task processing
- **JWT** with Python-Jose for secure authentication
- **Pydantic** for data validation and serialization
- **Alembic** for database migrations
- **OpenAI & Anthropic** for AI content generation
- **LangChain** for AI workflow orchestration
- **SendGrid** for email delivery
- **Stripe** for payment processing
- **AWS S3** for file storage
- **Sentry** for error monitoring
- **Loguru** for structured logging

## 📊 Database Schema

### Core Tables
1. **users** - User accounts and profiles
2. **campaigns** - Email campaign definitions
3. **campaign_templates** - Reusable email templates
4. **audiences** - Target audience segments
5. **email_sends** - Individual email sends
6. **email_events** - Email events (open, click, bounce)
7. **ai_generations** - AI-generated content history
8. **analytics** - Campaign performance metrics

### Relationships
- Users can have multiple campaigns
- Campaigns belong to users and can use templates
- Audiences can be used across multiple campaigns
- Email sends are linked to campaigns and audiences
- Events are linked to email sends for tracking

## 🔐 Security Implementation

### Authentication & Authorization
- **JWT tokens** with short expiration (15 minutes)
- **Refresh tokens** with longer expiration (7 days)
- **Role-based permissions** with granular access control
- **Rate limiting** on API endpoints
- **CORS configuration** for frontend-backend communication

### Data Protection
- **Password hashing** with bcrypt
- **Input validation** with Pydantic schemas
- **SQL injection prevention** with SQLAlchemy ORM
- **XSS protection** with proper content sanitization
- **CSRF protection** for form submissions

## 🎨 Design System

### Color Palette
- **Primary**: Blue gradient (#3B82F6 to #2563EB)
- **Secondary**: Green gradient (#22C55E to #16A34A)
- **Accent**: Purple gradient (#8B5CF6 to #7C3AED)
- **Neutral**: Gray scale (#F9FAFB to #111827)
- **Success**: Green (#10B981)
- **Warning**: Yellow (#F59E0B)
- **Error**: Red (#EF4444)

### Typography
- **Headings**: Inter font family
- **Body**: Inter font family
- **Monospace**: JetBrains Mono for code

### Component Library
- **Button variants**: Primary, Secondary, Ghost, Destructive
- **Input components**: Text, Email, Password, Select, Textarea
- **Card components**: Default, Interactive, Elevated
- **Modal components**: Dialog, Drawer, Popover
- **Navigation**: Sidebar, Topbar, Breadcrumbs

## 🔄 State Management

### Frontend State (Zustand)
- **Auth Store**: User authentication state
- **Campaign Store**: Campaign creation and editing
- **UI Store**: Theme, sidebar, modals
- **Notification Store**: Toast notifications

### Backend State (Redis)
- **Session storage**: User sessions and tokens
- **Cache**: Frequently accessed data
- **Task queues**: Background job processing
- **Rate limiting**: API request tracking

## 📱 Responsive Design

### Breakpoints
- **Mobile**: 320px - 768px
- **Tablet**: 768px - 1024px
- **Desktop**: 1024px - 1440px
- **Large Desktop**: 1440px+

### Mobile-First Approach
- **Touch-friendly** interface elements
- **Swipe gestures** for navigation
- **Optimized forms** for mobile input
- **Progressive enhancement** for advanced features

## 🧪 Testing Strategy

### Frontend Testing
- **Unit tests**: Component testing with Jest + React Testing Library
- **Integration tests**: Page and feature testing
- **E2E tests**: User journey testing with Playwright
- **Visual regression**: Component visual testing

### Backend Testing
- **Unit tests**: Service and utility function testing
- **Integration tests**: API endpoint testing
- **Database tests**: Model and migration testing
- **Performance tests**: Load and stress testing

## 🚀 Deployment Architecture

### Development Environment
- **Docker Compose** for local development
- **Hot reload** for both frontend and backend
- **Database seeding** for development data
- **Environment-specific** configurations

### Production Environment
- **Containerized deployment** with Docker
- **Load balancing** with Nginx
- **CDN** for static assets
- **Database clustering** for high availability
- **Monitoring** with Prometheus and Grafana

## 📈 Performance Optimization

### Frontend Optimization
- **Code splitting** with dynamic imports
- **Image optimization** with Next.js Image component
- **Bundle analysis** and optimization
- **Lazy loading** for non-critical components
- **Service worker** for caching

### Backend Optimization
- **Database indexing** for query performance
- **Connection pooling** for database connections
- **Caching strategy** with Redis
- **Background processing** for heavy tasks
- **API response compression**

## 🔍 Monitoring & Analytics

### Application Monitoring
- **Error tracking** with Sentry
- **Performance monitoring** with APM tools
- **Log aggregation** with structured logging
- **Health checks** for all services

### Business Analytics
- **Campaign performance** metrics
- **User engagement** tracking
- **Conversion funnel** analysis
- **Revenue tracking** and reporting

## 🔧 Development Workflow

### Git Workflow
- **Feature branches** for new development
- **Pull request reviews** for code quality
- **Automated testing** on CI/CD pipeline
- **Semantic versioning** for releases

### Code Quality
- **ESLint** and **Prettier** for code formatting
- **TypeScript** strict mode for type safety
- **Black** and **isort** for Python formatting
- **Pre-commit hooks** for code quality checks

This documentation provides a comprehensive overview of the AI Email Campaign Writer project structure, architecture, and implementation details for Claude to understand and work with the codebase effectively.
