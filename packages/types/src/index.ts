// User types
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

// Campaign types
export interface Campaign {
  id: string;
  userId: string;
  name: string;
  subject: string;
  content: string;
  status: CampaignStatus;
  recipientCount: number;
  sentCount: number;
  openedCount: number;
  clickedCount: number;
  createdAt: Date;
  updatedAt: Date;
  scheduledAt?: Date;
  sentAt?: Date;
}

export enum CampaignStatus {
  DRAFT = 'draft',
  SCHEDULED = 'scheduled',
  SENDING = 'sending',
  SENT = 'sent',
  PAUSED = 'paused',
  CANCELLED = 'cancelled'
}

// Recipient types
export interface Recipient {
  id: string;
  campaignId: string;
  email: string;
  firstName?: string;
  lastName?: string;
  status: RecipientStatus;
  sentAt?: Date;
  openedAt?: Date;
  clickedAt?: Date;
  unsubscribedAt?: Date;
}

export enum RecipientStatus {
  PENDING = 'pending',
  SENT = 'sent',
  DELIVERED = 'delivered',
  OPENED = 'opened',
  CLICKED = 'clicked',
  BOUNCED = 'bounced',
  UNSUBSCRIBED = 'unsubscribed'
}

// Template types
export interface Template {
  id: string;
  userId: string;
  name: string;
  subject: string;
  content: string;
  variables: string[];
  isPublic: boolean;
  createdAt: Date;
  updatedAt: Date;
}

// Analytics types
export interface CampaignAnalytics {
  campaignId: string;
  totalRecipients: number;
  sentCount: number;
  deliveredCount: number;
  openedCount: number;
  clickedCount: number;
  bouncedCount: number;
  unsubscribedCount: number;
  openRate: number;
  clickRate: number;
  bounceRate: number;
  unsubscribeRate: number;
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// AI Service types
export interface AIGenerationRequest {
  prompt: string;
  context?: string;
  tone?: string;
  length?: 'short' | 'medium' | 'long';
  variables?: Record<string, string>;
}

export interface AIGenerationResponse {
  content: string;
  subject?: string;
  suggestions?: string[];
  confidence: number;
}

// Email Service types
export interface EmailSendRequest {
  to: string[];
  subject: string;
  content: string;
  from?: string;
  replyTo?: string;
  campaignId?: string;
}

export interface EmailSendResponse {
  messageId: string;
  status: 'sent' | 'failed';
  error?: string;
}
