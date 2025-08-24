# API Directory

This directory contains the FastAPI application structure and API endpoints.

## Structure

### v1/
- **api.py**: Main API router that includes all endpoint routers
- **endpoints/**: Individual endpoint modules
  - **auth.py**: Authentication endpoints (login, register, refresh)
  - **campaigns.py**: Campaign management endpoints
  - **templates.py**: Email template endpoints
  - **analytics.py**: Analytics and reporting endpoints
  - **ai.py**: AI generation endpoints

## Guidelines

1. **Versioning**: All endpoints are under `/api/v1/`
2. **Authentication**: Use dependency injection for auth checks
3. **Validation**: Use Pydantic schemas for request/response validation
4. **Error Handling**: Use consistent error response format
5. **Documentation**: Include OpenAPI documentation for all endpoints

## TODO: Implementation Tasks

### Authentication Endpoints
- [ ] Implement user registration with email verification
- [ ] Add password reset functionality
- [ ] Implement refresh token rotation
- [ ] Add rate limiting for auth endpoints
- [ ] Create user profile management endpoints

### Campaign Endpoints
- [ ] Implement campaign CRUD operations
- [ ] Add campaign scheduling functionality
- [ ] Create campaign sending endpoints
- [ ] Implement campaign analytics endpoints
- [ ] Add campaign template management

### Template Endpoints
- [ ] Create template CRUD operations
- [ ] Add template variable validation
- [ ] Implement template sharing functionality
- [ ] Create template versioning system

### Analytics Endpoints
- [ ] Implement real-time analytics
- [ ] Add campaign performance metrics
- [ ] Create export functionality for reports
- [ ] Implement dashboard data endpoints

### AI Endpoints
- [ ] Create content generation endpoints
- [ ] Add content improvement functionality
- [ ] Implement A/B testing suggestions
- [ ] Add content optimization endpoints

## Error Handling

Use consistent error response format:

```python
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {}
}
```

## Rate Limiting

Implement rate limiting for:
- Authentication endpoints: 5 requests per minute
- AI generation: 10 requests per minute
- Campaign sending: 1 request per minute
- General endpoints: 100 requests per minute
