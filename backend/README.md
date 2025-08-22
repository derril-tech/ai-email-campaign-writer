# AI Email Campaign Writer - Backend

A FastAPI-based backend for the AI Email Campaign Writer application, providing RESTful APIs for campaign management, AI content generation, user authentication, and email delivery.

## 🚀 Features

- **FastAPI** with async/await support for high performance
- **PostgreSQL** with SQLAlchemy 2.0 for data persistence
- **Redis** for caching, sessions, and background task queues
- **JWT Authentication** with refresh tokens
- **AI Integration** with OpenAI GPT-4 and Anthropic Claude
- **Email Delivery** via SMTP and SendGrid
- **Background Tasks** with Celery
- **Real-time Updates** with WebSocket support
- **File Upload** with cloud storage support
- **Comprehensive Analytics** and reporting
- **Subscription Management** with Stripe integration
- **Rate Limiting** and security features
- **Monitoring** with Sentry integration

## 🛠 Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with pgvector
- **ORM**: SQLAlchemy 2.0 (async)
- **Cache**: Redis
- **Authentication**: JWT with Python-Jose
- **AI**: OpenAI GPT-4, Anthropic Claude, LangChain
- **Email**: SendGrid, SMTP
- **Background Tasks**: Celery
- **File Storage**: AWS S3, Cloudinary, Local
- **Payments**: Stripe
- **Monitoring**: Sentry, Loguru
- **Testing**: Pytest, HTTPX
- **Code Quality**: Black, isort, mypy, flake8

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Node.js 18+ (for development tools)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-email-campaign-writer/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ai_email_campaign

# AI Services
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Email
SENDGRID_API_KEY=your-sendgrid-api-key
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Security
SECRET_KEY=your-super-secret-key-here
```

### 5. Database Setup

```bash
# Create database
createdb ai_email_campaign

# Run migrations (if using Alembic)
alembic upgrade head
```

### 6. Start the Application

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 7. Access the API

- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── campaigns.py
│   │       │   ├── recipients.py
│   │       │   ├── templates.py
│   │       │   ├── ai.py
│   │       │   ├── analytics.py
│   │       │   ├── subscriptions.py
│   │       │   └── notifications.py
│   │       └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   │   ├── user.py
│   │   ├── campaign.py
│   │   ├── recipient.py
│   │   ├── template.py
│   │   ├── analytics.py
│   │   ├── subscription.py
│   │   ├── notification.py
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── campaign.py
│   │   ├── recipient.py
│   │   ├── template.py
│   │   ├── analytics.py
│   │   ├── subscription.py
│   │   ├── notification.py
│   │   ├── ai.py
│   │   ├── common.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── ai.py
│   │   ├── email.py
│   │   ├── user.py
│   │   ├── campaign.py
│   │   ├── analytics.py
│   │   └── storage.py
│   ├── utils/
│   │   ├── email_templates.py
│   │   └── validators.py
│   └── main.py
├── tests/
├── alembic/
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `false` |
| `SECRET_KEY` | JWT secret key | Required |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `ANTHROPIC_API_KEY` | Anthropic API key | Required |
| `SENDGRID_API_KEY` | SendGrid API key | Optional |
| `STRIPE_SECRET_KEY` | Stripe secret key | Optional |

### Database Configuration

The application uses PostgreSQL with the following extensions:
- `pgvector` for AI embeddings
- `uuid-ossp` for UUID generation

### Redis Configuration

Redis is used for:
- Session storage
- Cache
- Background task queues
- WebSocket message queues

## 🔌 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Refresh access token
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/forgot-password` - Password reset request
- `POST /api/v1/auth/reset-password` - Password reset confirmation
- `POST /api/v1/auth/verify-email` - Email verification
- `POST /api/v1/auth/resend-verification` - Resend verification email

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update user profile
- `PUT /api/v1/users/me/password` - Change password
- `GET /api/v1/users/me/stats` - Get user statistics

### Campaigns
- `GET /api/v1/campaigns` - List campaigns
- `POST /api/v1/campaigns` - Create campaign
- `GET /api/v1/campaigns/{id}` - Get campaign details
- `PUT /api/v1/campaigns/{id}` - Update campaign
- `DELETE /api/v1/campaigns/{id}` - Delete campaign
- `POST /api/v1/campaigns/{id}/send` - Send campaign
- `POST /api/v1/campaigns/{id}/pause` - Pause campaign
- `POST /api/v1/campaigns/{id}/resume` - Resume campaign
- `POST /api/v1/campaigns/{id}/duplicate` - Duplicate campaign

### Recipients
- `GET /api/v1/recipients` - List recipients
- `POST /api/v1/recipients` - Create recipient
- `GET /api/v1/recipients/{id}` - Get recipient details
- `PUT /api/v1/recipients/{id}` - Update recipient
- `DELETE /api/v1/recipients/{id}` - Delete recipient
- `POST /api/v1/recipients/import` - Import recipients
- `GET /api/v1/recipients/export` - Export recipients

### Templates
- `GET /api/v1/templates` - List templates
- `POST /api/v1/templates` - Create template
- `GET /api/v1/templates/{id}` - Get template details
- `PUT /api/v1/templates/{id}` - Update template
- `DELETE /api/v1/templates/{id}` - Delete template

### AI
- `POST /api/v1/ai/generate` - Generate content
- `POST /api/v1/ai/analyze` - Analyze content
- `POST /api/v1/ai/template` - Generate template
- `GET /api/v1/ai/usage` - Get AI usage statistics

### Analytics
- `GET /api/v1/analytics/campaigns/{id}` - Campaign analytics
- `GET /api/v1/analytics/user` - User analytics
- `GET /api/v1/analytics/events` - Email events

### Subscriptions
- `GET /api/v1/subscriptions` - List subscriptions
- `POST /api/v1/subscriptions` - Create subscription
- `GET /api/v1/subscriptions/{id}` - Get subscription details
- `PUT /api/v1/subscriptions/{id}` - Update subscription
- `DELETE /api/v1/subscriptions/{id}` - Cancel subscription

### Notifications
- `GET /api/v1/notifications` - List notifications
- `PUT /api/v1/notifications/{id}/read` - Mark notification as read
- `DELETE /api/v1/notifications/{id}` - Delete notification

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── conftest.py
├── test_auth.py
├── test_users.py
├── test_campaigns.py
├── test_recipients.py
├── test_templates.py
├── test_ai.py
├── test_analytics.py
└── test_integration.py
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build image
docker build -t ai-email-campaign-backend .

# Run container
docker run -p 8000:8000 ai-email-campaign-backend
```

### Production Checklist

- [ ] Set `DEBUG=false`
- [ ] Configure production database
- [ ] Set up Redis cluster
- [ ] Configure email service
- [ ] Set up monitoring (Sentry)
- [ ] Configure SSL/TLS
- [ ] Set up load balancer
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline

## 🔒 Security

- JWT token authentication
- Password hashing with bcrypt
- Rate limiting
- CORS configuration
- Input validation
- SQL injection protection
- XSS protection
- CSRF protection

## 📊 Monitoring

- Request logging with Loguru
- Error tracking with Sentry
- Performance monitoring
- Health check endpoints
- Metrics collection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run linting and tests
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Contact the development team

## 🔄 Changelog

### v1.0.0
- Initial release
- Core API functionality
- AI integration
- Email campaign management
- User authentication
- Analytics and reporting
