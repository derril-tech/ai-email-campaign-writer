"""
AI schemas for content generation and analysis.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class AIGenerationRequest(BaseModel):
    """AI content generation request schema."""
    content_type: str = Field(..., regex="^(subject|content|both|template)$", description="Type of content to generate")
    campaign_type: str = Field(..., regex="^(newsletter|promotional|transactional|automated)$", description="Campaign type")
    
    # Content parameters
    topic: Optional[str] = Field(None, description="Main topic or theme")
    tone: Optional[str] = Field(None, regex="^(professional|casual|friendly|formal|enthusiastic|urgent)$", description="Content tone")
    length: Optional[str] = Field(None, regex="^(short|medium|long)$", description="Content length")
    target_audience: Optional[str] = Field(None, description="Target audience description")
    
    # Context and examples
    context: Optional[str] = Field(None, description="Additional context or background")
    examples: Optional[List[str]] = Field(None, description="Example content for reference")
    keywords: Optional[List[str]] = Field(None, description="Keywords to include")
    
    # Template variables
    variables: Optional[Dict[str, Any]] = Field(None, description="Template variables")
    
    # AI model preferences
    model: Optional[str] = Field(None, regex="^(gpt-4|gpt-3.5-turbo|claude-3-sonnet|claude-3-opus)$", description="AI model to use")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Creativity level")
    max_tokens: Optional[int] = Field(1000, ge=1, le=4000, description="Maximum tokens to generate")


class AIGenerationResponse(BaseModel):
    """AI content generation response schema."""
    success: bool = Field(..., description="Whether generation was successful")
    content: Optional[str] = Field(None, description="Generated content")
    subject: Optional[str] = Field(None, description="Generated subject line")
    html_content: Optional[str] = Field(None, description="Generated HTML content")
    plain_text_content: Optional[str] = Field(None, description="Generated plain text content")
    
    # Generation metadata
    model_used: str = Field(..., description="AI model used for generation")
    tokens_used: int = Field(..., description="Number of tokens used")
    generation_time: float = Field(..., description="Generation time in seconds")
    
    # Suggestions and alternatives
    suggestions: Optional[List[str]] = Field(None, description="Alternative suggestions")
    improvements: Optional[List[str]] = Field(None, description="Suggested improvements")
    
    # Error information
    error: Optional[str] = Field(None, description="Error message if generation failed")
    error_code: Optional[str] = Field(None, description="Error code if generation failed")


class AIContentAnalysis(BaseModel):
    """AI content analysis request schema."""
    content: str = Field(..., description="Content to analyze")
    analysis_type: str = Field(..., regex="^(readability|sentiment|spam|engagement|seo)$", description="Type of analysis")
    
    # Analysis parameters
    language: Optional[str] = Field("en", description="Content language")
    target_audience: Optional[str] = Field(None, description="Target audience for analysis")


class AIContentAnalysisResponse(BaseModel):
    """AI content analysis response schema."""
    success: bool = Field(..., description="Whether analysis was successful")
    
    # Readability analysis
    readability_score: Optional[float] = Field(None, ge=0.0, le=100.0, description="Readability score")
    reading_level: Optional[str] = Field(None, description="Reading level")
    word_count: Optional[int] = Field(None, description="Word count")
    sentence_count: Optional[int] = Field(None, description="Sentence count")
    
    # Sentiment analysis
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0, description="Sentiment score")
    sentiment_label: Optional[str] = Field(None, description="Sentiment label")
    
    # Spam analysis
    spam_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Spam probability")
    spam_indicators: Optional[List[str]] = Field(None, description="Spam indicators found")
    
    # Engagement analysis
    engagement_score: Optional[float] = Field(None, ge=0.0, le=100.0, description="Engagement score")
    engagement_factors: Optional[List[str]] = Field(None, description="Engagement factors")
    
    # SEO analysis
    seo_score: Optional[float] = Field(None, ge=0.0, le=100.0, description="SEO score")
    seo_suggestions: Optional[List[str]] = Field(None, description="SEO suggestions")
    
    # General analysis
    suggestions: Optional[List[str]] = Field(None, description="General improvement suggestions")
    strengths: Optional[List[str]] = Field(None, description="Content strengths")
    weaknesses: Optional[List[str]] = Field(None, description="Content weaknesses")
    
    # Error information
    error: Optional[str] = Field(None, description="Error message if analysis failed")
    error_code: Optional[str] = Field(None, description="Error code if analysis failed")


class AITemplateGeneration(BaseModel):
    """AI template generation request schema."""
    template_name: str = Field(..., description="Template name")
    template_type: str = Field(..., regex="^(newsletter|promotional|transactional|welcome|follow-up)$", description="Template type")
    
    # Template parameters
    industry: Optional[str] = Field(None, description="Industry or business type")
    tone: Optional[str] = Field(None, description="Template tone")
    variables: Optional[List[str]] = Field(None, description="Required template variables")
    
    # Content preferences
    include_header: bool = Field(True, description="Include email header")
    include_footer: bool = Field(True, description="Include email footer")
    include_cta: bool = Field(True, description="Include call-to-action")
    
    # AI model preferences
    model: Optional[str] = Field(None, description="AI model to use")
    temperature: Optional[float] = Field(0.7, description="Creativity level")


class AITemplateGenerationResponse(BaseModel):
    """AI template generation response schema."""
    success: bool = Field(..., description="Whether generation was successful")
    
    # Generated template
    template_id: Optional[str] = Field(None, description="Generated template ID")
    name: Optional[str] = Field(None, description="Template name")
    subject: Optional[str] = Field(None, description="Template subject")
    content: Optional[str] = Field(None, description="Template content")
    html_content: Optional[str] = Field(None, description="HTML template content")
    plain_text_content: Optional[str] = Field(None, description="Plain text template content")
    
    # Template metadata
    variables: Optional[List[str]] = Field(None, description="Template variables")
    category: Optional[str] = Field(None, description="Template category")
    tags: Optional[List[str]] = Field(None, description="Template tags")
    
    # Generation metadata
    model_used: str = Field(..., description="AI model used")
    tokens_used: int = Field(..., description="Tokens used")
    generation_time: float = Field(..., description="Generation time")
    
    # Error information
    error: Optional[str] = Field(None, description="Error message if generation failed")
    error_code: Optional[str] = Field(None, description="Error code if generation failed")


class AIUsageStats(BaseModel):
    """AI usage statistics schema."""
    user_id: str = Field(..., description="User ID")
    total_requests: int = Field(..., description="Total AI requests")
    requests_today: int = Field(..., description="AI requests today")
    requests_this_month: int = Field(..., description="AI requests this month")
    
    # Usage by type
    generation_requests: int = Field(..., description="Content generation requests")
    analysis_requests: int = Field(..., description="Content analysis requests")
    template_requests: int = Field(..., description="Template generation requests")
    
    # Usage by model
    gpt_requests: int = Field(..., description="GPT model requests")
    claude_requests: int = Field(..., description="Claude model requests")
    
    # Limits and quotas
    daily_limit: int = Field(..., description="Daily request limit")
    monthly_limit: int = Field(..., description="Monthly request limit")
    remaining_daily: int = Field(..., description="Remaining daily requests")
    remaining_monthly: int = Field(..., description="Remaining monthly requests")
    
    # Timestamps
    last_request_at: Optional[datetime] = Field(None, description="Last request timestamp")
    reset_date: datetime = Field(..., description="Quota reset date")
