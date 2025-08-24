"""
Copy Corpus model for brand voice examples and embeddings.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, VECTOR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
import uuid

from app.core.database import Base

class CopyType(str, enum.Enum):
    """Copy type enumeration"""
    SUBJECT_LINE = "subject_line"
    EMAIL_BODY = "email_body"
    CTA = "cta"
    BRAND_VOICE = "brand_voice"
    WINNING_COPY = "winning_copy"

class CopyCorpus(Base):
    """Copy Corpus model for brand voice examples and embeddings"""
    
    __tablename__ = "copy_corpus"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Copy information
    label = Column(String(255), nullable=False)  # e.g., "High-performing subject line"
    content = Column(Text, nullable=False)  # The actual copy text
    copy_type = Column(Enum(CopyType), nullable=False)
    
    # Performance metrics (if applicable)
    performance_score = Column(String(50), nullable=True)  # e.g., "open_rate: 25%"
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=True)
    
    # Vector embedding for similarity search
    embedding = Column(VECTOR(1536), nullable=True)  # OpenAI embedding dimension
    
    # Metadata
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="copy_corpus")
    campaign = relationship("Campaign", back_populates="copy_examples")
    
    def __repr__(self):
        return f"<CopyCorpus(id={self.id}, label='{self.label}', type='{self.copy_type}')>"
