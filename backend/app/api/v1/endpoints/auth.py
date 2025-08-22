"""
Authentication endpoints for login, registration, and token management.
"""

from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password
)
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import (
    Token,
    UserCreate,
    UserLogin,
    PasswordReset,
    PasswordResetRequest
)
from app.services.email import EmailService
from app.services.user import UserService

router = APIRouter()

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Register a new user account.
    """
    # Check if user already exists
    existing_user = await UserService.get_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = await UserService.create_user(db, user_data)
    
    # Generate tokens
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "subscription": user.subscription_plan
        },
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Authenticate user and get tokens.
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Update last login
    await UserService.update_last_login(db, user.id)
    
    # Generate tokens
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "subscription": user.subscription_plan
        },
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Refresh access token using refresh token.
    """
    try:
        # Verify refresh token
        user_id = verify_refresh_token(refresh_token)
        user = await UserService.get_by_id(db, user_id)
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Generate new tokens
        new_access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        new_refresh_token = create_refresh_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.post("/logout")
async def logout(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Logout user and invalidate tokens.
    """
    try:
        # Invalidate refresh token (add to blacklist)
        await UserService.invalidate_refresh_token(db, refresh_token)
        return {"message": "Successfully logged out"}
    except Exception:
        # Even if token is invalid, return success to prevent enumeration
        return {"message": "Successfully logged out"}

@router.post("/forgot-password")
async def forgot_password(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Request password reset email.
    """
    user = await UserService.get_by_email(db, email=request.email)
    if user:
        # Generate password reset token
        reset_token = await UserService.create_password_reset_token(db, user.id)
        
        # Send password reset email
        email_service = EmailService()
        await email_service.send_password_reset_email(
            email=user.email,
            name=user.first_name,
            reset_token=reset_token
        )
    
    # Always return success to prevent email enumeration
    return {"message": "Password reset email sent"}

@router.post("/reset-password")
async def reset_password(
    request: PasswordReset,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Reset password using token.
    """
    # Verify reset token and get user
    user = await UserService.verify_password_reset_token(db, request.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Update password
    hashed_password = get_password_hash(request.new_password)
    await UserService.update_password(db, user.id, hashed_password)
    
    # Invalidate reset token
    await UserService.invalidate_password_reset_token(db, request.token)
    
    return {"message": "Password successfully reset"}

@router.post("/verify-email")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Verify email address using verification token.
    """
    user = await UserService.verify_email_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token"
        )
    
    # Mark email as verified
    await UserService.verify_email(db, user.id)
    
    return {"message": "Email successfully verified"}
