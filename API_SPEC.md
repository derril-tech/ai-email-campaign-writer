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

### 📧 Campaign Management Endpoints

#### GET /campaigns
Get all campaigns for current user.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)
- `status`: Filter by status (draft, scheduled, sent, archived)
- `search`: Search by campaign name

**Response (200):**
```json
{
  "campaigns": [
    {
      "id": "uuid",
      "name": "Welcome Series",
      "subject": "Welcome to our platform!",
      "status": "draft",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "scheduled_at": null,
      "sent_at": null,
      "recipient_count": 0,
      "open_rate": 0,
      "click_rate": 0
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
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
  "audience_id": "uuid",
  "template_id": "uuid",
  "scheduled_at": "2024-01-15T10:00:00Z",
  "settings": {
    "from_name": "John Doe",
    "from_email": "john@company.com",
    "reply_to": "support@company.com"
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
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
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
  "content": "<html>...</html>",
  "status": "draft",
  "audience": {
    "id": "uuid",
    "name": "New Users",
    "count": 1500
  },
  "template": {
    "id": "uuid",
    "name": "Welcome Template"
  },
  "settings": {
    "from_name": "John Doe",
    "from_email": "john@company.com",
    "reply_to": "support@company.com"
  },
  "analytics": {
    "sent": 1500,
    "delivered": 1480,
    "opened": 740,
    "clicked": 222,
    "bounced": 20,
    "unsubscribed": 15
  },
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### PUT /campaigns/{campaign_id}
Update campaign.

**Request Body:**
```json
{
  "name": "Updated Welcome Series",
  "subject": "Updated subject line",
  "content": "<html>Updated content...</html>"
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "name": "Updated Welcome Series",
  "subject": "Updated subject line",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### DELETE /campaigns/{campaign_id}
Delete campaign.

**Response (204):**
No content

#### POST /campaigns/{campaign_id}/send
Send campaign immediately.

**Response (200):**
```json
{
  "message": "Campaign queued for sending",
  "estimated_recipients": 1500
}
```

#### POST /campaigns/{campaign_id}/schedule
Schedule campaign for later sending.

**Request Body:**
```json
{
  "scheduled_at": "2024-01-15T10:00:00Z"
}
```

**Response (200):**
```json
{
  "message": "Campaign scheduled successfully",
  "scheduled_at": "2024-01-15T10:00:00Z"
}
```

### 🎯 Audience Management Endpoints

#### GET /audiences
Get all audiences for current user.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)
- `search`: Search by audience name

**Response (200):**
```json
{
  "audiences": [
    {
      "id": "uuid",
      "name": "New Users",
      "description": "Users who signed up in the last 30 days",
      "count": 1500,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 5,
    "pages": 1
  }
}
```

#### POST /audiences
Create a new audience.

**Request Body:**
```json
{
  "name": "Premium Users",
  "description": "Users with premium subscription",
  "filters": {
    "subscription": "premium",
    "signup_date": {
      "operator": "gte",
      "value": "2024-01-01"
    }
  }
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "name": "Premium Users",
  "description": "Users with premium subscription",
  "count": 0,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### GET /audiences/{audience_id}
Get audience details.

**Response (200):**
```json
{
  "id": "uuid",
  "name": "Premium Users",
  "description": "Users with premium subscription",
  "filters": {
    "subscription": "premium",
    "signup_date": {
      "operator": "gte",
      "value": "2024-01-01"
    }
  },
  "subscribers": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "subscribed_at": "2024-01-01T00:00:00Z"
    }
  ],
  "count": 1500,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### PUT /audiences/{audience_id}
Update audience.

**Request Body:**
```json
{
  "name": "Updated Premium Users",
  "description": "Updated description",
  "filters": {
    "subscription": "premium"
  }
}
```

**Response (200):**
```json
{
  "id": "uuid",
  "name": "Updated Premium Users",
  "description": "Updated description",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### DELETE /audiences/{audience_id}
Delete audience.

**Response (204):**
No content

### 📝 Template Management Endpoints

#### GET /templates
Get all email templates.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)
- `category`: Filter by category
- `search`: Search by template name

**Response (200):**
```json
{
  "templates": [
    {
      "id": "uuid",
      "name": "Welcome Template",
      "category": "onboarding",
      "thumbnail": "https://example.com/thumbnail.jpg",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 20,
    "pages": 2
  }
}
```

#### GET /templates/{template_id}
Get template details.

**Response (200):**
```json
{
  "id": "uuid",
  "name": "Welcome Template",
  "category": "onboarding",
  "html_content": "<html>...</html>",
  "text_content": "Plain text version...",
  "variables": ["first_name", "company_name"],
  "thumbnail": "https://example.com/thumbnail.jpg",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### 🤖 AI Content Generation Endpoints

#### POST /ai/generate-content
Generate email content using AI.

**Request Body:**
```json
{
  "campaign_type": "welcome",
  "audience": {
    "industry": "technology",
    "demographics": "professionals",
    "interests": ["productivity", "automation"]
  },
  "brand_voice": "professional",
  "tone": "friendly",
  "call_to_action": "Sign up for free trial",
  "content_length": "medium",
  "include_subject_line": true
}
```

**Response (200):**
```json
{
  "subject_line": "Boost Your Productivity with AI-Powered Automation",
  "email_content": {
    "html": "<html>...</html>",
    "text": "Plain text version..."
  },
  "suggestions": [
    "Consider adding a personal story",
    "Include social proof",
    "Add urgency to the CTA"
  ],
  "generation_id": "uuid"
}
```

#### POST /ai/generate-subject-lines
Generate multiple subject line variations.

**Request Body:**
```json
{
  "campaign_topic": "Product launch",
  "target_audience": "existing customers",
  "tone": "excited",
  "count": 5
}
```

**Response (200):**
```json
{
  "subject_lines": [
    "🚀 You're First to See Our New Product!",
    "Breaking: Something Amazing Just Launched",
    "Your VIP Access to Our Latest Innovation",
    "Don't Miss Out - New Product Available Now",
    "Exclusive: Be the First to Experience This"
  ]
}
```

#### POST /ai/optimize-content
Optimize existing email content.

**Request Body:**
```json
{
  "content": "<html>Original content...</html>",
  "optimization_type": "engagement",
  "target_audience": "professionals",
  "industry": "technology"
}
```

**Response (200):**
```json
{
  "optimized_content": {
    "html": "<html>Optimized content...</html>",
    "text": "Optimized plain text..."
  },
  "improvements": [
    "Added more compelling headline",
    "Improved call-to-action clarity",
    "Enhanced personalization"
  ],
  "score": 85
}
```

#### GET /ai/generations
Get AI generation history.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)
- `type`: Filter by generation type

**Response (200):**
```json
{
  "generations": [
    {
      "id": "uuid",
      "type": "email_content",
      "prompt": "Generate welcome email...",
      "response": "Generated content...",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 50,
    "pages": 5
  }
}
```

### 📊 Analytics Endpoints

#### GET /analytics/campaigns/{campaign_id}
Get campaign analytics.

**Query Parameters:**
- `start_date`: Start date for analytics (ISO format)
- `end_date`: End date for analytics (ISO format)

**Response (200):**
```json
{
  "campaign_id": "uuid",
  "overview": {
    "sent": 1500,
    "delivered": 1480,
    "opened": 740,
    "clicked": 222,
    "bounced": 20,
    "unsubscribed": 15,
    "spam_reports": 2
  },
  "rates": {
    "delivery_rate": 98.67,
    "open_rate": 50.0,
    "click_rate": 15.0,
    "bounce_rate": 1.33,
    "unsubscribe_rate": 1.0
  },
  "timeline": [
    {
      "date": "2024-01-01",
      "sent": 500,
      "opened": 250,
      "clicked": 75
    }
  ],
  "top_links": [
    {
      "url": "https://example.com/cta",
      "clicks": 150,
      "unique_clicks": 120
    }
  ],
  "device_breakdown": {
    "desktop": 45,
    "mobile": 40,
    "tablet": 15
  }
}
```

#### GET /analytics/dashboard
Get dashboard analytics overview.

**Response (200):**
```json
{
  "total_campaigns": 25,
  "total_subscribers": 15000,
  "total_sent": 50000,
  "average_open_rate": 45.2,
  "average_click_rate": 12.8,
  "recent_campaigns": [
    {
      "id": "uuid",
      "name": "Welcome Series",
      "sent": 1500,
      "opened": 675,
      "clicked": 192,
      "open_rate": 45.0,
      "click_rate": 12.8
    }
  ],
  "growth_chart": [
    {
      "date": "2024-01-01",
      "subscribers": 15000,
      "sent": 5000
    }
  ]
}
```

#### GET /analytics/export/{campaign_id}
Export campaign analytics.

**Query Parameters:**
- `format`: Export format (csv, excel, pdf)
- `start_date`: Start date for export
- `end_date`: End date for export

**Response (200):**
File download with analytics data

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
    "email_service": "healthy"
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
    "advanced_analytics": true
  },
  "limits": {
    "max_campaigns": 100,
    "max_subscribers": 10000,
    "max_ai_generations": 1000
  },
  "supported_providers": {
    "email": ["sendgrid", "smtp", "ses"],
    "ai": ["openai", "anthropic"]
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

## 📋 Rate Limits

- **Authentication endpoints**: 5 requests per minute
- **AI generation**: 10 requests per minute
- **Campaign sending**: 1 request per minute
- **General API**: 100 requests per minute per user

## 🔐 Security Headers

All responses include security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

This API specification provides comprehensive documentation for all endpoints, request/response formats, and authentication mechanisms for the AI Email Campaign Writer backend.
