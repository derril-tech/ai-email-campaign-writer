"""
Services module for business logic and external integrations.
"""

from .ai_service import AIService, ai_service, get_ai_service
from .email_service import EmailService, email_service, get_email_service

__all__ = [
    # AI Service
    "AIService",
    "ai_service",
    "get_ai_service",
    
    # Email Service
    "EmailService",
    "email_service",
    "get_email_service",
]
