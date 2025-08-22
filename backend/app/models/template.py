"""
Template model for email template management.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base


class Template(Base):
    """Template model for email template management."""
    
    __tablename__ = "templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Template information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    html_content = Column(Text, nullable=True)
    plain_text_content = Column(Text, nullable=True)
    
    # Template settings
    is_active = Column(Boolean, default=True, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    category = Column(String(100), nullable=True)  # newsletter, promotional, transactional, etc.
    
    # Template variables
    variables = Column(JSON, default=list, nullable=False)  # List of variable names
    
    # Template metadata
    tags = Column(JSON, default=list, nullable=False)
    metadata = Column(JSON, default=dict, nullable=False)
    
    # Usage statistics
    usage_count = Column(Integer, default=0, nullable=False)
    last_used_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="templates")
    campaigns = relationship("Campaign", backref="template")
    
    def __repr__(self) -> str:
        return f"<Template(id={self.id}, name={self.name})>"
    
    def get_variables(self) -> list:
        """Get list of template variables."""
        return self.variables or []
    
    def has_variable(self, variable_name: str) -> bool:
        """Check if template has a specific variable."""
        return variable_name in self.get_variables()


class TemplateVariable(Base):
    """Template variable model for managing template variables."""
    
    __tablename__ = "template_variables"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey("templates.id"), nullable=False)
    
    # Variable information
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    default_value = Column(Text, nullable=True)
    is_required = Column(Boolean, default=False, nullable=False)
    
    # Variable type and validation
    variable_type = Column(String(50), default="string", nullable=False)  # string, number, date, boolean, etc.
    validation_rules = Column(JSON, default=dict, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    template = relationship("Template")
    
    def __repr__(self) -> str:
        return f"<TemplateVariable(id={self.id}, name={self.name})>"
