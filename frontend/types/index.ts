// User Types
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  avatar?: string;
  role: 'user' | 'admin';
  isEmailVerified: boolean;
  createdAt: string;
  updatedAt: string;
  subscription?: Subscription;
}

export interface Subscription {
  id: string;
  plan: 'free' | 'pro' | 'enterprise';
  status: 'active' | 'canceled' | 'past_due';
  currentPeriodEnd: string;
  cancelAtPeriodEnd: boolean;
}

// Campaign Types
export interface Campaign {
  id: string;
  name: string;
  description?: string;
  status: 'draft' | 'scheduled' | 'sending' | 'sent' | 'paused';
  type: 'newsletter' | 'promotional' | 'transactional' | 'automated';
  subject: string;
  content: string;
  htmlContent: string;
  plainTextContent: string;
  sender: {
    name: string;
    email: string;
  };
  recipients: Recipient[];
  tags: string[];
  metadata: Record<string, any>;
  scheduledAt?: string;
  sentAt?: string;
  createdAt: string;
  updatedAt: string;
  userId: string;
  analytics?: CampaignAnalytics;
}

export interface Recipient {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  status: 'subscribed' | 'unsubscribed' | 'bounced' | 'spam';
  metadata?: Record<string, any>;
}

export interface CampaignAnalytics {
  id: string;
  campaignId: string;
  sent: number;
  delivered: number;
  opened: number;
  clicked: number;
  bounced: number;
  unsubscribed: number;
  spamReports: number;
  openRate: number;
  clickRate: number;
  bounceRate: number;
  createdAt: string;
  updatedAt: string;
}

// Template Types
export interface Template {
  id: string;
  name: string;
  description?: string;
  category: 'newsletter' | 'promotional' | 'transactional' | 'automated';
  content: string;
  htmlContent: string;
  plainTextContent: string;
  variables: TemplateVariable[];
  isPublic: boolean;
  isDefault: boolean;
  createdAt: string;
  updatedAt: string;
  userId?: string;
}

export interface TemplateVariable {
  name: string;
  type: 'string' | 'number' | 'boolean' | 'date';
  description: string;
  defaultValue?: any;
  required: boolean;
}

// AI Generation Types
export interface AIGenerationRequest {
  prompt: string;
  context: {
    industry?: string;
    targetAudience?: string;
    tone?: 'professional' | 'casual' | 'friendly' | 'formal';
    length?: 'short' | 'medium' | 'long';
    language?: string;
  };
  template?: string;
  variables?: Record<string, any>;
}

export interface AIGenerationResponse {
  id: string;
  content: string;
  htmlContent: string;
  plainTextContent: string;
  subject: string;
  suggestions: string[];
  metadata: {
    model: string;
    tokens: number;
    processingTime: number;
  };
  createdAt: string;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

// Form Types
export interface LoginForm {
  email: string;
  password: string;
  rememberMe?: boolean;
}

export interface RegisterForm {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
  acceptTerms: boolean;
}

export interface CampaignForm {
  name: string;
  description?: string;
  subject: string;
  content: string;
  type: Campaign['type'];
  scheduledAt?: string;
  recipients: string[];
  tags: string[];
}

// WebSocket Types
export interface WebSocketMessage {
  type: 'campaign_update' | 'analytics_update' | 'notification';
  data: any;
  timestamp: string;
}

// File Upload Types
export interface FileUpload {
  id: string;
  filename: string;
  originalName: string;
  mimeType: string;
  size: number;
  url: string;
  uploadedAt: string;
  userId: string;
}

// Notification Types
export interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  isRead: boolean;
  createdAt: string;
  userId: string;
}

// Theme Types
export interface Theme {
  mode: 'light' | 'dark' | 'system';
  primaryColor: string;
  secondaryColor: string;
}

// Settings Types
export interface UserSettings {
  id: string;
  userId: string;
  theme: Theme;
  emailPreferences: {
    marketing: boolean;
    updates: boolean;
    security: boolean;
  };
  notifications: {
    email: boolean;
    push: boolean;
    sms: boolean;
  };
  timezone: string;
  language: string;
  createdAt: string;
  updatedAt: string;
}
