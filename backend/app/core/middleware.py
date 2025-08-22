"""
Middleware for the FastAPI application.
"""

import time
import json
from typing import Callable, Dict, Any
from fastapi import Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
from app.core.config import settings
from app.core.security import verify_token


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} - "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response: {response.status_code} - "
                f"Process Time: {process_time:.4f}s"
            )
            
            # Add process time header
            response.headers["X-Process-Time"] = str(process_time)
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Error: {str(e)} - "
                f"Process Time: {process_time:.4f}s"
            )
            raise


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Middleware for JWT token authentication."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip authentication for certain paths
        skip_paths = {
            "/docs", "/redoc", "/openapi.json", "/health",
            "/api/v1/auth/login", "/api/v1/auth/register",
            "/api/v1/auth/forgot-password", "/api/v1/auth/reset-password",
            "/api/v1/auth/verify-email"
        }
        
        if request.url.path in skip_paths:
            return await call_next(request)
        
        # Check for Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return await call_next(request)
        
        token = auth_header.split(" ")[1]
        user_id = verify_token(token)
        
        if user_id:
            request.state.user_id = user_id
        else:
            # Token is invalid but we don't block the request
            # Let individual endpoints handle authentication
            pass
        
        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting requests."""
    
    def __init__(self, app, redis_client):
        super().__init__(app)
        self.redis = redis_client
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Create rate limit keys
        minute_key = f"rate_limit:{client_ip}:minute"
        hour_key = f"rate_limit:{client_ip}:hour"
        
        try:
            # Check minute rate limit
            minute_count = await self.redis.get(minute_key)
            if minute_count and int(minute_count) >= settings.RATE_LIMIT_PER_MINUTE:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded. Please try again later."}
                )
            
            # Check hour rate limit
            hour_count = await self.redis.get(hour_key)
            if hour_count and int(hour_count) >= settings.RATE_LIMIT_PER_HOUR:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Hourly rate limit exceeded. Please try again later."}
                )
            
            # Increment counters
            pipe = self.redis.pipeline()
            pipe.incr(minute_key)
            pipe.expire(minute_key, 60)
            pipe.incr(hour_key)
            pipe.expire(hour_key, 3600)
            await pipe.execute()
            
        except Exception as e:
            logger.error(f"Rate limiting error: {str(e)}")
            # Continue without rate limiting if Redis is unavailable
        
        return await call_next(request)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware for handling and logging errors."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except HTTPException as e:
            # Log HTTP exceptions
            logger.warning(
                f"HTTP Exception: {e.status_code} - {e.detail} - "
                f"Path: {request.url.path}"
            )
            raise
        except Exception as e:
            # Log unexpected exceptions
            logger.error(
                f"Unexpected error: {str(e)} - "
                f"Path: {request.url.path} - "
                f"Method: {request.method}"
            )
            
            # Return 500 error in production, detailed error in development
            if settings.DEBUG:
                return JSONResponse(
                    status_code=500,
                    content={
                        "detail": "Internal server error",
                        "error": str(e),
                        "type": type(e).__name__
                    }
                )
            else:
                return JSONResponse(
                    status_code=500,
                    content={"detail": "Internal server error"}
                )


def setup_middleware(app):
    """Setup all middleware for the FastAPI application."""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"] if settings.DEBUG else ["localhost", "127.0.0.1"]
    )
    
    # Custom middleware
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(AuthenticationMiddleware)
    app.add_middleware(ErrorHandlingMiddleware)
    
    # Rate limiting middleware (requires Redis)
    # app.add_middleware(RateLimitMiddleware, redis_client=redis_client)
