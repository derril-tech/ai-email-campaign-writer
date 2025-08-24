# AI Email Campaign Writer - API Specification

## 🔗 Base URL
```
Development: http://localhost:8000/api/v1
Production: https://api.aiemailcampaign.com/api/v1
```

## 🔐 Authentication

### JWT Token Authentication
All protected endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Token Endpoints
- **Access Token**: 15 minutes expiration
- **Refresh Token**: 7 days expiration
- **Auto-refresh**: Automatic token refresh on 401 responses

## 📋 API Endpoints

### 🔑 Authentication Endpoints

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "company_name": "Acme Corp",
  "industry": "technology"
}
```

**Response (201):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "Acme Corp",
    "industry": "technology",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  },
  "access_token": "jwt_token",
  "refresh_token": "refresh_token"
}
```

#### POST /auth/login
Authenticate user and get tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "user",
    "subscription": "premium"
  },
  "access_token": "jwt_token",
  "refresh_token": "refresh_token"
}
```

#### POST /auth/refresh
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "refresh_token"
}
```

**Response (200):**
```json
{
  "access_token": "new_jwt_token",
  "refresh_token": "new_refresh_token"
}
```

#### POST /auth/logout
Logout user and invalidate tokens.

**Request Body:**
```json
{
  "refresh_token": "refresh_token"
}
```

**Response (200):**
```json
{
  "message": "Successfully logged out"
}
```

#### POST /auth/forgot-password
Request password reset email.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200):**
```json
{
  "message": "Password reset email sent"
}
```

#### POST /auth/reset-password
Reset password using token.

**Request Body:**
```json
{
  "token": "reset_token",
  "new_password": "newpassword123"
}
```

**Response (200):**
```json
{
  "message": "Password successfully reset"
}
```

### 👤 User Management Endpoints

#### GET /users/me
Get current user profile.

**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "company_name": "Acme Corp",
  "industry": "technology",
  "role": "user",
  "subscription": "premium",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### PUT /users/me
Update current user profile.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "company_name": "New Corp",
  "industry": "marketing"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Smith",
  "company_name": "New Corp",
  "industry": "marketing",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### PUT /users/me/password
Change user password.

**Request Body:**
```json
{
  "current_password": "oldpassword",
  "new_password": "newpassword123"
}
```

**Response (200):**
```json
{
  "message": "Password successfully updated"
}
```

### 📧 Campaign Endpoints

#### GET /campaigns
Get all campaigns for the authenticated user.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `limit` (int): Items per page (default: 20)
- `status` (string): Filter by status (draft, scheduled, sending, completed, failed)
- `search` (string): Search by campaign name

**Response (200):**
```json
{
  "campaigns": [
    {
      "id": "uuid",
      "name": "Welcome Series",
      "subject": "Welcome to our platform!",
      "status": "scheduled",
      "scheduled_at": "2024-01-01T10:00:00Z",
      "created_at": "2024-01-01T00:00:00Z",
      "open_rate": 25.5,
      "click_rate": 3.2,
      "recipient_count": 1500
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

#### POST /campaigns
Create a new campaign.

**Request Body:**
```json
{
  "name": "Welcome Series",
  "subject": "Welcome to our platform!",
  "html_content": "<p>Hello {{first_name}}, welcome to our platform!</p>",
  "audience_id": "uuid",
  "scheduled_at": "2024-01-01T10:00:00Z",
  "template_variables": {
    "first_name": "string",
    "last_name": "string",
    "company": "string"
  }
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "name": "Welcome Series",
  "subject": "Welcome to our platform!",
  "status": "draft",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### GET /campaigns/{campaign_id}
Get campaign details.

**Response (200):**
```json
{
  "id": "uuid",
  "name": "Welcome Series",
  "subject": "Welcome to our platform!",
  "html_content": "<p>Hello {{first_name}}, welcome to our platform!</p>",
  "status": "scheduled",
  "scheduled_at": "2024-01-01T10:00:00Z",
  "created_at": "2024-01-01T00:00:00Z",
  "analytics": {
    "sent": 1500,
    "delivered": 1470,
    "opened": 375,
    "clicked": 48,
    "bounced": 30,
    "unsubscribed": 5
  }
}
```

#### PUT /campaigns/{campaign_id}
Update campaign.

**Request Body:**
```json
{
  "name": "Updated Welcome Series",
  "subject": "Updated subject line",
  "html_content": "<p>Updated content</p>"
}
```

#### DELETE /campaigns/{campaign_id}
Delete campaign.

**Response (204):** No content

#### POST /campaigns/{campaign_id}/send
Send campaign immediately.

**Response (200):**
```json
{
  "message": "Campaign queued for sending",
  "estimated_recipients": 1500
}
```

### 🤖 AI Generation Endpoints

#### POST /ai/generate
Generate email content using AI.

**Request Body:**
```json
{
  "task": "subject_line",
  "context": {
    "brand_voice": "professional",
    "target_audience": "B2B SaaS users",
    "campaign_goal": "onboarding",
    "key_message": "Welcome to our platform"
  },
  "constraints": {
    "max_tokens": 2000,
    "temperature": 0.7,
    "include_cta": true
  },
  "framework": "langchain"
}
```

**Response (200):**
```json
{
  "content": "Welcome to the Future of SaaS: Your Journey Starts Here",
  "variations": [
    "Transform Your Workflow: Welcome to [Platform Name]",
    "Your SaaS Success Story Begins Today"
  ],
  "confidence_score": 0.85,
  "framework_used": "langchain",
  "model_used": "gpt-4"
}
```

#### POST /ai/generate-advanced
Generate content using advanced AI frameworks.

**Request Body:**
```json
{
  "task": "campaign_strategy",
  "context": {
    "brand_guidelines": "professional, trustworthy, innovative",
    "target_audience": "enterprise_decision_makers",
    "campaign_goal": "lead_generation",
    "historical_performance": "high_open_rates_with_personalization"
  },
  "frameworks": {
    "primary": "crewai",
    "supporting": ["langgraph", "llamaindex"],
    "quality_gates": true,
    "human_review": false
  }
}
```

**Response (200):**
```json
{
  "strategy": {
    "subject_lines": [
      "Transform Your Enterprise with AI-Powered Solutions",
      "The Future of Enterprise: AI That Actually Works"
    ],
    "email_body": "<p>Dear {{first_name}},</p><p>In today's rapidly evolving business landscape...</p>",
    "cta_text": "Schedule Your Demo",
    "send_time_recommendation": "Tuesday 10:00 AM EST"
  },
  "quality_score": 0.92,
  "brand_voice_match": 0.89,
  "frameworks_used": ["crewai", "langgraph", "llamaindex"],
  "processing_time": "2.3s"
}
```

### 📚 Copy Corpus Endpoints (pgvector)

#### GET /copy-corpus
Get copy corpus entries with similarity search.

**Query Parameters:**
- `copy_type` (string): Filter by type (subject_line, email_body, cta, brand_voice, winning_copy)
- `similar_to` (string): Find similar content to this text
- `limit` (int): Number of results (default: 10)
- `min_score` (float): Minimum similarity score (0.0-1.0)

**Response (200):**
```json
{
  "entries": [
    {
      "id": "uuid",
      "label": "High-performing subject line",
      "content": "Transform Your Business with AI",
      "copy_type": "subject_line",
      "performance_score": "open_rate: 28.5%",
      "similarity_score": 0.87,
      "tags": "enterprise, ai, transformation",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 25
}
```

#### POST /copy-corpus
Add new copy corpus entry.

**Request Body:**
```json
{
  "label": "High-performing subject line",
  "content": "Transform Your Business with AI",
  "copy_type": "subject_line",
  "performance_score": "open_rate: 28.5%",
  "campaign_id": "uuid",
  "tags": "enterprise, ai, transformation"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "label": "High-performing subject line",
  "content": "Transform Your Business with AI",
  "copy_type": "subject_line",
  "embedding_generated": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### GET /copy-corpus/{entry_id}
Get specific copy corpus entry.

**Response (200):**
```json
{
  "id": "uuid",
  "label": "High-performing subject line",
  "content": "Transform Your Business with AI",
  "copy_type": "subject_line",
  "performance_score": "open_rate: 28.5%",
  "campaign_id": "uuid",
  "tags": "enterprise, ai, transformation",
  "similar_entries": [
    {
      "id": "uuid2",
      "content": "AI-Powered Business Transformation",
      "similarity_score": 0.92
    }
  ],
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### DELETE /copy-corpus/{entry_id}
Delete copy corpus entry.

**Response (204):** No content

### 🎨 Template Management (Mustache.js)

#### GET /templates
Get email templates.

**Query Parameters:**
- `category` (string): Filter by category
- `search` (string): Search by template name

**Response (200):**
```json
{
  "templates": [
    {
      "id": "uuid",
      "name": "Welcome Email",
      "category": "onboarding",
      "html_content": "<p>Hello {{first_name}},</p><p>Welcome to {{company_name}}!</p>",
      "variables": ["first_name", "company_name"],
      "preview_image": "https://example.com/preview.jpg",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

#### POST /templates
Create new template.

**Request Body:**
```json
{
  "name": "Welcome Email",
  "category": "onboarding",
  "html_content": "<p>Hello {{first_name}},</p><p>Welcome to {{company_name}}!</p>",
  "variables": ["first_name", "company_name"]
}
```

#### POST /templates/{template_id}/render
Render template with variables.

**Request Body:**
```json
{
  "variables": {
    "first_name": "John",
    "company_name": "Acme Corp"
  }
}
```

**Response (200):**
```json
{
  "rendered_html": "<p>Hello John,</p><p>Welcome to Acme Corp!</p>",
  "variables_used": ["first_name", "company_name"],
  "missing_variables": []
}
```

### 📊 Analytics Endpoints

#### GET /analytics/campaigns
Get campaign analytics.

**Query Parameters:**
- `start_date` (string): Start date (ISO format)
- `end_date` (string): End date (ISO format)
- `group_by` (string): Group by (day, week, month)

**Response (200):**
```json
{
  "summary": {
    "total_campaigns": 45,
    "total_sent": 67500,
    "total_opened": 16875,
    "total_clicked": 2160,
    "avg_open_rate": 25.0,
    "avg_click_rate": 3.2
  },
  "trends": [
    {
      "date": "2024-01-01",
      "campaigns": 3,
      "sent": 4500,
      "opened": 1125,
      "clicked": 144
    }
  ]
}
```

#### GET /analytics/campaigns/{campaign_id}
Get specific campaign analytics.

**Response (200):**
```json
{
  "campaign_id": "uuid",
  "name": "Welcome Series",
  "summary": {
    "sent": 1500,
    "delivered": 1470,
    "opened": 375,
    "clicked": 48,
    "bounced": 30,
    "unsubscribed": 5
  },
  "timeline": [
    {
      "timestamp": "2024-01-01T10:00:00Z",
      "event": "sent",
      "count": 1500
    }
  ],
  "segments": [
    {
      "segment": "enterprise",
      "open_rate": 28.5,
      "click_rate": 4.2
    }
  ]
}
```

### 🔄 A/B Testing Endpoints

#### POST /campaigns/{campaign_id}/ab-test
Create A/B test for campaign.

**Request Body:**
```json
{
  "test_type": "subject_line",
  "variants": [
    {
      "name": "Variant A",
      "content": "Welcome to our platform!"
    },
    {
      "name": "Variant B", 
      "content": "Transform your business with AI"
    }
  ],
  "test_size": 1000,
  "duration_hours": 24,
  "winning_criteria": "open_rate"
}
```

**Response (201):**
```json
{
  "test_id": "uuid",
  "status": "running",
  "variants": [
    {
      "id": "uuid1",
      "name": "Variant A",
      "content": "Welcome to our platform!",
      "sent": 500,
      "opened": 125,
      "open_rate": 25.0
    }
  ],
  "estimated_completion": "2024-01-02T10:00:00Z"
}
```

#### GET /campaigns/{campaign_id}/ab-test/{test_id}
Get A/B test results.

**Response (200):**
```json
{
  "test_id": "uuid",
  "status": "completed",
  "winning_variant": "uuid2",
  "confidence_level": 0.95,
  "statistical_significance": true,
  "variants": [
    {
      "id": "uuid1",
      "name": "Variant A",
      "sent": 500,
      "opened": 125,
      "open_rate": 25.0,
      "confidence_interval": [21.2, 28.8]
    }
  ]
}
```

### 🧪 Load Testing Endpoints

#### POST /load-test/burst
Run burst load test.

**Request Body:**
```json
{
  "scenario": "campaign_creation",
  "duration_minutes": 5,
  "target_users": 100,
  "ramp_up_minutes": 2
}
```

**Response (200):**
```json
{
  "test_id": "uuid",
  "status": "running",
  "scenario": "campaign_creation",
  "metrics": {
    "requests_per_second": 25.5,
    "average_response_time": 180,
    "p95_response_time": 250,
    "error_rate": 0.02
  },
  "estimated_completion": "2024-01-01T10:05:00Z"
}
```

#### GET /load-test/{test_id}
Get load test results.

**Response (200):**
```json
{
  "test_id": "uuid",
  "status": "completed",
  "scenario": "campaign_creation",
  "summary": {
    "total_requests": 7650,
    "successful_requests": 7497,
    "failed_requests": 153,
    "average_response_time": 180,
    "p95_response_time": 250,
    "p99_response_time": 350
  },
  "thresholds": {
    "p95_response_time": 200,
    "error_rate": 0.05,
    "passed": false
  }
}
```

### 🔧 System Endpoints

#### GET /health
Health check endpoint.

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "redis": "healthy",
    "email_service": "healthy",
    "ai_service": "healthy"
  }
}
```

#### GET /config
Get application configuration.

**Response (200):**
```json
{
  "features": {
    "ai_generation": true,
    "a_b_testing": true,
    "advanced_analytics": true,
    "pgvector": true,
    "load_testing": true
  },
  "limits": {
    "max_campaigns": 100,
    "max_subscribers": 10000,
    "max_ai_generations": 1000
  },
  "supported_providers": {
    "email": ["sendgrid", "smtp", "ses"],
    "ai": ["openai", "anthropic"],
    "vector_db": ["pgvector"]
  },
  "ai_frameworks": {
    "langchain": true,
    "langgraph": true,
    "crewai": true,
    "llamaindex": true,
    "autogen": true
  }
}
```

## 📝 Error Responses

### Standard Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  }
}
```

### Common Error Codes
- `VALIDATION_ERROR`: Request validation failed
- `AUTHENTICATION_ERROR`: Invalid or missing authentication
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INTERNAL_ERROR`: Server error
- `AI_GENERATION_ERROR`: AI service error
- `VECTOR_SEARCH_ERROR`: pgvector search error

## 🔄 WebSocket Events

### Connection
```
ws://localhost:8000/ws
```

### Authentication
```json
{
  "type": "auth",
  "token": "jwt_token"
}
```

### Real-time Events
```json
{
  "type": "campaign_progress",
  "data": {
    "campaign_id": "uuid",
    "sent": 500,
    "total": 1500,
    "percentage": 33.33
  }
}
```

```json
{
  "type": "ai_generation_progress",
  "data": {
    "task_id": "uuid",
    "status": "processing",
    "progress": 75,
    "estimated_completion": "2024-01-01T00:00:30Z"
  }
}
```

```json
{
  "type": "ab_test_update",
  "data": {
    "test_id": "uuid",
    "variant_id": "uuid1",
    "sent": 250,
    "opened": 62,
    "open_rate": 24.8
  }
}
```

## 📋 Rate Limits

- **Authentication endpoints**: 5 requests per minute
- **AI generation**: 10 requests per minute
- **Campaign sending**: 1 request per minute
- **Copy corpus operations**: 20 requests per minute
- **Load testing**: 2 requests per hour
- **General API**: 100 requests per minute per user

## 🔐 Security Headers

All responses include security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

## 🤖 AI Framework Integration

### Framework Selection
The API automatically selects the appropriate AI framework based on the request:

- **Simple generation**: LangChain
- **Complex workflows**: LangGraph
- **Multi-agent tasks**: CrewAI
- **RAG operations**: LlamaIndex
- **Human-in-the-loop**: AutoGen
- **Vector similarity**: pgvector

### Quality Gates
All AI-generated content passes through automated quality gates:
1. **Brand voice consistency** (pgvector similarity)
2. **Compliance checks** (CAN-SPAM, GDPR)
3. **Content validation** (fact checking, URL validation)
4. **Performance optimization** (A/B testing integration)

This API specification provides comprehensive documentation for all endpoints, request/response formats, and authentication mechanisms for the AI Email Campaign Writer backend, including the latest pgvector, AI framework, and load testing capabilities.

---

**Last Updated**: December 2024
**Version**: 2.0.0 - Updated to reflect current infrastructure with pgvector, AI frameworks, and load testing
