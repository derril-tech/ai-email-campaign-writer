export interface AIGenerationRequest {
  campaign_type: 'welcome' | 'newsletter' | 'promotional' | 'abandoned_cart' | 're-engagement' | 'custom'
  audience: AudienceInfo
  brand_voice: 'professional' | 'casual' | 'friendly' | 'formal' | 'enthusiastic' | 'authoritative'
  tone: 'friendly' | 'professional' | 'excited' | 'urgent' | 'informative' | 'persuasive'
  call_to_action: string
  content_length: 'short' | 'medium' | 'long'
  include_subject_line: boolean
  custom_prompt?: string
  industry_context?: string
  product_details?: string
  target_goals?: string[]
}

export interface AudienceInfo {
  industry?: string
  demographics?: string
  interests?: string[]
  pain_points?: string[]
  goals?: string[]
  experience_level?: 'beginner' | 'intermediate' | 'advanced'
}

export interface AIGenerationResponse {
  subject_line: string
  email_content: {
    html: string
    text: string
  }
  suggestions: string[]
  generation_id: string
  confidence_score: number
  estimated_engagement: number
}

export interface SubjectLineGenerationRequest {
  campaign_topic: string
  target_audience: string
  tone: 'excited' | 'urgent' | 'curious' | 'professional' | 'friendly'
  count: number
  include_emojis?: boolean
  max_length?: number
}

export interface SubjectLineGenerationResponse {
  subject_lines: string[]
  scores: number[]
  recommendations: string[]
}

export interface ContentOptimizationRequest {
  content: string
  optimization_type: 'engagement' | 'conversion' | 'deliverability' | 'accessibility'
  target_audience: string
  industry?: string
  goals?: string[]
  constraints?: string[]
}

export interface ContentOptimizationResponse {
  optimized_content: {
    html: string
    text: string
  }
  improvements: string[]
  score: number
  before_after_comparison: {
    readability_score: number
    engagement_potential: number
    conversion_likelihood: number
  }
}

export interface AIGenerationHistory {
  id: string
  type: 'email_content' | 'subject_line' | 'content_optimization'
  prompt: string
  response: string
  metadata: {
    campaign_type?: string
    audience_info?: AudienceInfo
    generation_time: number
    tokens_used: number
    model_used: string
  }
  created_at: string
}

export interface AIGenerationHistoryResponse {
  generations: AIGenerationHistory[]
  pagination: {
    page: number
    limit: number
    total: number
    pages: number
  }
}

export interface AIConfig {
  available_models: string[]
  max_tokens_per_request: number
  rate_limits: {
    requests_per_minute: number
    requests_per_hour: number
    requests_per_day: number
  }
  supported_languages: string[]
  content_types: string[]
}
