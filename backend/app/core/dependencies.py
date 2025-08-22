"""
Common dependencies for FastAPI endpoints.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from app.core.database import get_db
from app.core.security import verify_token
from app.core.redis import get_redis, RedisClient
from app.services.ai_service import get_ai_service, AIService
from app.services.email_service import get_email_service, EmailService
from app.models.user import User
from app.core.config import settings

# Security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer token credentials
        db: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    try:
        # Verify token
        user_id = verify_token(credentials.credentials)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Current active user
        
    Raises:
        HTTPException: If user is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current admin user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Current admin user
        
    Raises:
        HTTPException: If user is not admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


async def get_optional_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, otherwise return None.
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        Optional[User]: Current user if authenticated, None otherwise
    """
    try:
        # Check for Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header.split(" ")[1]
        user_id = verify_token(token)
        
        if not user_id:
            return None
        
        # Get user from database
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            return None
        
        return user
        
    except Exception as e:
        logger.error(f"Error getting optional current user: {str(e)}")
        return None


def get_rate_limit_key(request: Request) -> str:
    """
    Get rate limit key for the request.
    
    Args:
        request: FastAPI request object
        
    Returns:
        str: Rate limit key
    """
    # Use client IP as rate limit key
    client_ip = request.client.host if request.client else "unknown"
    return f"rate_limit:{client_ip}"


async def check_rate_limit(
    request: Request,
    redis: RedisClient = Depends(get_redis)
) -> bool:
    """
    Check if request is within rate limits.
    
    Args:
        request: FastAPI request object
        redis: Redis client
        
    Returns:
        bool: True if within rate limits, False otherwise
    """
    try:
        rate_limit_key = get_rate_limit_key(request)
        
        # Check minute rate limit
        minute_count = await redis.get(f"{rate_limit_key}:minute")
        if minute_count and int(minute_count) >= settings.RATE_LIMIT_PER_MINUTE:
            return False
        
        # Check hour rate limit
        hour_count = await redis.get(f"{rate_limit_key}:hour")
        if hour_count and int(hour_count) >= settings.RATE_LIMIT_PER_HOUR:
            return False
        
        # Increment counters
        pipe = redis.client.pipeline()
        pipe.incr(f"{rate_limit_key}:minute")
        pipe.expire(f"{rate_limit_key}:minute", 60)
        pipe.incr(f"{rate_limit_key}:hour")
        pipe.expire(f"{rate_limit_key}:hour", 3600)
        await pipe.execute()
        
        return True
        
    except Exception as e:
        logger.error(f"Error checking rate limit: {str(e)}")
        # Allow request if rate limiting fails
        return True


async def require_rate_limit(
    request: Request,
    redis: RedisClient = Depends(get_redis)
):
    """
    Dependency to require rate limiting.
    
    Args:
        request: FastAPI request object
        redis: Redis client
        
    Raises:
        HTTPException: If rate limit exceeded
    """
    if not await check_rate_limit(request, redis):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )


async def get_user_from_request(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get user from request headers or query parameters.
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        Optional[User]: User if found, None otherwise
    """
    try:
        # Try to get user from Authorization header
        user = await get_optional_current_user(request, db)
        if user:
            return user
        
        # Try to get user from query parameter (for public endpoints)
        user_id = request.query_params.get("user_id")
        if user_id:
            from sqlalchemy import select
            result = await db.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()
        
        return None
        
    except Exception as e:
        logger.error(f"Error getting user from request: {str(e)}")
        return None


# Common service dependencies
async def get_ai_service_dependency() -> AIService:
    """Get AI service dependency."""
    return await get_ai_service()


async def get_email_service_dependency() -> EmailService:
    """Get email service dependency."""
    return await get_email_service()


async def get_redis_dependency() -> RedisClient:
    """Get Redis client dependency."""
    return await get_redis()


# Database session dependency
async def get_db_session() -> AsyncSession:
    """Get database session dependency."""
    return await get_db()


# Common response headers
def get_common_headers() -> dict:
    """
    Get common response headers.
    
    Returns:
        dict: Common response headers
    """
    return {
        "X-API-Version": "1.0",
        "X-Server": "AI Email Campaign Writer",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }


# Pagination dependency
def get_pagination_params(
    page: int = 1,
    size: int = 20,
    max_size: int = 100
) -> dict:
    """
    Get pagination parameters.
    
    Args:
        page: Page number (1-based)
        size: Page size
        max_size: Maximum page size
        
    Returns:
        dict: Pagination parameters
    """
    if page < 1:
        page = 1
    if size < 1:
        size = 20
    if size > max_size:
        size = max_size
    
    return {
        "page": page,
        "size": size,
        "offset": (page - 1) * size
    }


# Search dependency
def get_search_params(
    query: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None
) -> dict:
    """
    Get search parameters.
    
    Args:
        query: Search query
        sort_by: Sort field
        sort_order: Sort order (asc/desc)
        
    Returns:
        dict: Search parameters
    """
    return {
        "query": query,
        "sort_by": sort_by,
        "sort_order": sort_order if sort_order in ["asc", "desc"] else "desc"
    }
