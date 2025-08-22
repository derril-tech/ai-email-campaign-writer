"""
Main FastAPI application entry point.
"""

import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
import logging

from app.core.config import settings
from app.core.database import init_db, close_db
from app.api.v1 import api_router
from app.services.ai import AIService
from app.services.email import EmailService
from app.core.security import get_current_user_optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger.add("logs/app.log", rotation="500 MB", retention="10 days", level="INFO")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting AI Email Campaign Writer API...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized successfully")
    
    # Initialize services
    await AIService.initialize()
    await EmailService.initialize()
    logger.info("Services initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Email Campaign Writer API...")
    await close_db()
    logger.info("Database connection closed")


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="AI-powered email campaign creation and management platform",
        version=settings.VERSION,
        docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
        openapi_url="/openapi.json" if settings.ENVIRONMENT == "development" else None,
        lifespan=lifespan
    )

    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request timing middleware
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url}")
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
        
        return response

    # Exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": exc.errors()
                }
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An internal server error occurred"
                }
            }
        )

    # Include API routes
    app.include_router(api_router, prefix="/api/v1")

    # TODO: Implement comprehensive health check
    # This should check:
    # - Database connectivity and query performance
    # - Redis connectivity and cache operations
    # - External API health (OpenAI, Anthropic, SendGrid)
    # - Background job queue status
    # - Disk space and memory usage
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "services": {
                "database": "healthy",
                "redis": "healthy",
                "email_service": "healthy"
            }
        }

    # Configuration endpoint
    @app.get("/config")
    async def get_config():
        return {
            "features": {
                "ai_generation": True,
                "a_b_testing": True,
                "advanced_analytics": True
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

    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "AI Email Campaign Writer API",
            "version": settings.VERSION,
            "docs": "/docs" if settings.ENVIRONMENT == "development" else None
        }

    return app

app = create_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    )
