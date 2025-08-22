# AI Email Campaign Writer

A modern, full-stack email marketing platform powered by AI that helps you create engaging email campaigns in minutes, not hours.

## 🚀 Features

### 🤖 AI-Powered Content Generation
- **Smart Content Creation**: Generate compelling email content using GPT-4 and Claude
- **Subject Line Optimization**: Create multiple subject line variations with A/B testing
- **Personalization**: AI-driven content personalization based on audience segments
- **Brand Voice Consistency**: Maintain your brand voice across all campaigns

### 📧 Campaign Management
- **Drag-and-Drop Editor**: Beautiful, responsive email templates
- **Campaign Scheduling**: Schedule campaigns for optimal delivery times
- **A/B Testing**: Test subject lines, content, and send times
- **Audience Segmentation**: Target specific subscriber groups
- **Automation Workflows**: Set up automated email sequences

### 📊 Advanced Analytics
- **Real-time Tracking**: Monitor opens, clicks, and conversions
- **Performance Insights**: Detailed analytics and reporting
- **ROI Calculation**: Track campaign performance and revenue
- **Engagement Scoring**: Identify your most engaged subscribers

### 🔐 Enterprise Security
- **SOC 2 Compliance**: Bank-level security standards
- **GDPR Compliance**: Full data protection compliance
- **Two-Factor Authentication**: Enhanced account security
- **Role-Based Access**: Team collaboration with permissions

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Zustand** for state management
- **React Query** for data fetching
- **React Hook Form** for forms

### Backend
- **FastAPI** with async/await
- **PostgreSQL** with SQLAlchemy 2.0
- **Redis** for caching and sessions
- **Celery** for background tasks
- **JWT Authentication** with refresh tokens
- **OpenAI & Anthropic** for AI features
- **SendGrid** for email delivery

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.9+
- PostgreSQL 13+
- Redis 6+

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-email-campaign-writer
```

### 2. Frontend Setup
```bash
cd frontend
npm install
cp env.example .env.local
# Edit .env.local with your configuration
npm run dev
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with your configuration
```

### 4. Database Setup
```bash
# Create PostgreSQL database
createdb ai_email_campaign

# Run migrations
cd backend
alembic upgrade head
```

### 5. Environment Configuration

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

#### Backend (.env)
```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ai_email_campaign

# Security
SECRET_KEY=your-super-secret-key-change-in-production

# AI Services
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Email Services
SENDGRID_API_KEY=your-sendgrid-api-key
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Redis
REDIS_URL=redis://localhost:6379/0
```

## 🚀 Running the Application

### Development Mode
```bash
# Terminal 1 - Frontend
cd frontend
npm run dev

# Terminal 2 - Backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 3 - Redis
redis-server

# Terminal 4 - Celery (for background tasks)
cd backend
celery -A app.core.celery worker --loglevel=info
```

### Production Mode
```bash
# Build frontend
cd frontend
npm run build
npm start

# Run backend with gunicorn
cd backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📁 Project Structure

```
ai-email-campaign-writer/
├── frontend/                 # Next.js frontend application
│   ├── app/                 # Next.js App Router
│   ├── components/          # React components
│   ├── hooks/              # Custom React hooks
│   ├── lib/                # Utility libraries
│   ├── types/              # TypeScript type definitions
│   └── store/              # Zustand state management
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API routes and endpoints
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic services
│   │   └── utils/          # Utility functions
│   ├── alembic/            # Database migrations
│   └── tests/              # Test files
├── docs/                   # Documentation
├── docker/                 # Docker configuration
└── scripts/                # Deployment scripts
```

## 🔧 Configuration

### AI Models
The platform supports multiple AI providers:
- **OpenAI GPT-4**: For content generation and optimization
- **Anthropic Claude**: For creative content and analysis
- **Custom Models**: Integration with your own AI models

### Email Providers
- **SendGrid**: Primary email delivery service
- **SMTP**: Custom SMTP server configuration
- **AWS SES**: Amazon Simple Email Service

### Storage Options
- **Local Storage**: File storage on server
- **AWS S3**: Cloud storage for files and assets
- **Cloudinary**: Image optimization and storage

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app
```

### E2E Tests
```bash
npm run test:e2e
```

## 📊 Monitoring

### Application Monitoring
- **Sentry**: Error tracking and performance monitoring
- **Loguru**: Structured logging
- **Health Checks**: Service health monitoring

### Business Analytics
- **Campaign Performance**: Open rates, click rates, conversions
- **User Engagement**: User behavior and interaction patterns
- **Revenue Tracking**: ROI calculation and revenue attribution

## 🔒 Security

### Authentication & Authorization
- JWT tokens with short expiration (15 minutes)
- Refresh tokens with longer expiration (7 days)
- Role-based access control (Admin, User, Premium)
- Two-factor authentication support

### Data Protection
- Password hashing with bcrypt
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- XSS protection with content sanitization

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Cloud Deployment
- **AWS**: ECS, RDS, ElastiCache
- **Google Cloud**: GKE, Cloud SQL, Memorystore
- **Azure**: AKS, Azure Database, Redis Cache

### Environment Variables
See `env.example` files in both frontend and backend directories for all required environment variables.

## 📈 Performance

### Frontend Optimization
- Code splitting with dynamic imports
- Image optimization with Next.js Image
- Bundle analysis and optimization
- Service worker for caching

### Backend Optimization
- Database indexing for query performance
- Connection pooling for database connections
- Redis caching for frequently accessed data
- Background processing for heavy tasks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs.aiemailcampaign.com](https://docs.aiemailcampaign.com)
- **Email Support**: support@aiemailcampaign.com
- **Community**: [Discord](https://discord.gg/aiemailcampaign)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)

## 🎯 Roadmap

### Q1 2024
- [ ] Advanced AI content generation
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native)

### Q2 2024
- [ ] AI-powered audience segmentation
- [ ] Predictive analytics
- [ ] Advanced automation workflows
- [ ] White-label solution

### Q3 2024
- [ ] Enterprise SSO integration
- [ ] Advanced reporting and exports
- [ ] API rate limiting and quotas
- [ ] Multi-tenant architecture

---

**Built with ❤️ by the AI Email Campaign Writer Team**
