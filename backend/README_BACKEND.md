# Backend - AI Email Campaign Writer

FastAPI backend application for the AI Email Campaign Writer platform.

## Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Authentication**: JWT with Passlib
- **Email**: SendGrid integration
- **AI**: OpenAI API integration
- **Testing**: pytest
- **Linting**: Black, isort, flake8
- **Documentation**: OpenAPI/Swagger

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

## Quick Start

### Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Development

### Available Scripts

```bash
# Development
uvicorn app.main:app --reload    # Start development server
python -m pytest                 # Run tests
python -m pytest --cov=app       # Run tests with coverage

# Code Quality
black app/                       # Format code
isort app/                       # Sort imports
flake8 app/                      # Lint code
mypy app/                        # Type checking

# Database
alembic revision --autogenerate  # Generate migration
alembic upgrade head            # Apply migrations
alembic downgrade -1            # Rollback migration

# Utilities
python scripts/seed_data.py     # Seed database
python scripts/check_env.py     # Validate environment
```

### Environment Variables

Copy `env.example` to `.env` and configure:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/ai_email_campaign
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
OPENAI_API_KEY=your-openai-key
SENDGRID_API_KEY=your-sendgrid-key

# Email Configuration
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-key

# Application Settings
ENVIRONMENT=development
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1
ALLOWED_ORIGINS=http://localhost:3000
```

## Project Structure

```
backend/
├── app/
│   ├── api/                    # API routes
│   │   └── v1/
│   │       ├── endpoints/      # API endpoints
│   │       └── api.py          # API router
│   ├── core/                   # Core configuration
│   │   ├── config.py           # Settings
│   │   ├── database.py         # Database setup
│   │   ├── security.py         # Authentication
│   │   └── redis.py            # Redis setup
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   └── utils/                  # Utilities
├── alembic/                    # Database migrations
├── tests/                      # Test files
├── scripts/                    # Utility scripts
└── _INSTRUCTIONS.md            # Development instructions
```

## API Documentation

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### API Endpoints

#### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - User logout

#### Campaigns
- `GET /api/v1/campaigns` - List campaigns
- `POST /api/v1/campaigns` - Create campaign
- `GET /api/v1/campaigns/{id}` - Get campaign
- `PUT /api/v1/campaigns/{id}` - Update campaign
- `DELETE /api/v1/campaigns/{id}` - Delete campaign
- `POST /api/v1/campaigns/{id}/send` - Send campaign

#### AI Generation
- `POST /api/v1/ai/generate` - Generate email content
- `POST /api/v1/ai/improve` - Improve existing content

## Database

### Models

- **User**: User accounts and authentication
- **Campaign**: Email campaigns
- **Recipient**: Campaign recipients
- **Template**: Email templates
- **Analytics**: Campaign performance data

### Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# View migration history
alembic history
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_campaigns.py

# Run tests in parallel
pytest -n auto
```

### Test Structure

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_campaign():
    response = client.post(
        "/api/v1/campaigns",
        json={"name": "Test Campaign", "subject": "Test"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Campaign"
```

### Test Database

Tests use a separate test database:

```python
# conftest.py
@pytest.fixture
def test_db():
    # Setup test database
    yield
    # Cleanup test database
```

## Code Quality

### Black (Code Formatting)

```bash
# Format code
black app/

# Check formatting
black --check app/
```

### isort (Import Sorting)

```bash
# Sort imports
isort app/

# Check import sorting
isort --check-only app/
```

### flake8 (Linting)

```bash
# Run linter
flake8 app/

# Configuration in setup.cfg
```

### mypy (Type Checking)

```bash
# Run type checker
mypy app/

# Configuration in mypy.ini
```

## Performance

### Database Optimization

- Use database indexes for frequently queried fields
- Implement connection pooling
- Use async database operations where possible

### Caching Strategy

- Cache frequently accessed data in Redis
- Implement cache invalidation strategies
- Use cache headers for API responses

### Monitoring

- Use Sentry for error tracking
- Implement structured logging
- Monitor API response times

## Security

### Authentication

- JWT tokens with secure expiration
- Password hashing with bcrypt
- Rate limiting on authentication endpoints

### Data Protection

- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- XSS protection with proper content types

### Environment Security

- Secure environment variable handling
- No secrets in code or logs
- HTTPS enforcement in production

## Deployment

### Docker

```bash
# Build image
docker build -t ai-email-campaign-api .

# Run container
docker run -p 8000:8000 ai-email-campaign-api
```

### Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] SSL certificates installed
- [ ] Monitoring configured
- [ ] Backup strategy implemented
- [ ] Rate limiting configured
- [ ] CORS settings updated

## Troubleshooting

### Common Issues

1. **Database connection errors**
   ```bash
   # Check database status
   docker-compose ps postgres
   
   # View database logs
   docker-compose logs postgres
   ```

2. **Redis connection errors**
   ```bash
   # Check Redis status
   docker-compose ps redis
   
   # Test Redis connection
   redis-cli ping
   ```

3. **Import errors**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Check Python path
   echo $PYTHONPATH
   ```

## Contributing

1. Follow the coding standards in `_INSTRUCTIONS.md`
2. Write tests for new features
3. Update API documentation
4. Ensure all tests pass before submitting PR
