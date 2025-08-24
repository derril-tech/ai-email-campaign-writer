// Mock data for UI development and testing

export interface MockUser {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  company: string;
  role: 'user' | 'admin';
  subscription: 'free' | 'pro' | 'enterprise';
  createdAt: string;
}

export interface MockCampaign {
  id: string;
  name: string;
  subject: string;
  status: 'draft' | 'scheduled' | 'sending' | 'sent' | 'paused';
  recipientCount: number;
  sentCount: number;
  openedCount: number;
  clickedCount: number;
  openRate: number;
  clickRate: number;
  createdAt: string;
  scheduledAt?: string;
  sentAt?: string;
}

export interface MockTemplate {
  id: string;
  name: string;
  subject: string;
  category: 'welcome' | 'newsletter' | 'promotional' | 'transactional';
  isPublic: boolean;
  createdAt: string;
}

export interface MockRecipient {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  status: 'active' | 'unsubscribed' | 'bounced';
  lastEmailSent?: string;
  tags: string[];
}

export interface MockAnalytics {
  totalCampaigns: number;
  totalRecipients: number;
  totalEmailsSent: number;
  averageOpenRate: number;
  averageClickRate: number;
  monthlyGrowth: number;
}

// Mock Users
export const mockUsers: MockUser[] = [
  {
    id: '1',
    email: 'john.doe@example.com',
    firstName: 'John',
    lastName: 'Doe',
    company: 'Acme Corp',
    role: 'admin',
    subscription: 'pro',
    createdAt: '2024-01-15T10:00:00Z'
  },
  {
    id: '2',
    email: 'jane.smith@example.com',
    firstName: 'Jane',
    lastName: 'Smith',
    company: 'TechStart Inc',
    role: 'user',
    subscription: 'free',
    createdAt: '2024-02-01T14:30:00Z'
  }
];

// Mock Campaigns
export const mockCampaigns: MockCampaign[] = [
  {
    id: '1',
    name: 'Welcome Campaign',
    subject: 'Welcome to AI Email Campaign Writer!',
    status: 'sent',
    recipientCount: 500,
    sentCount: 500,
    openedCount: 125,
    clickedCount: 25,
    openRate: 25.0,
    clickRate: 5.0,
    createdAt: '2024-01-20T09:00:00Z',
    sentAt: '2024-01-20T10:00:00Z'
  },
  {
    id: '2',
    name: 'Product Launch Announcement',
    subject: '🚀 New Features Available Now!',
    status: 'scheduled',
    recipientCount: 1200,
    sentCount: 0,
    openedCount: 0,
    clickedCount: 0,
    openRate: 0,
    clickRate: 0,
    createdAt: '2024-01-25T15:30:00Z',
    scheduledAt: '2024-02-01T10:00:00Z'
  },
  {
    id: '3',
    name: 'Monthly Newsletter',
    subject: 'Your January Newsletter is Here',
    status: 'draft',
    recipientCount: 0,
    sentCount: 0,
    openedCount: 0,
    clickedCount: 0,
    openRate: 0,
    clickRate: 0,
    createdAt: '2024-01-28T11:00:00Z'
  },
  {
    id: '4',
    name: 'Black Friday Sale',
    subject: '🔥 50% Off Everything - Limited Time!',
    status: 'sent',
    recipientCount: 800,
    sentCount: 800,
    openedCount: 240,
    clickedCount: 80,
    openRate: 30.0,
    clickRate: 10.0,
    createdAt: '2024-11-20T08:00:00Z',
    sentAt: '2024-11-20T09:00:00Z'
  }
];

// Mock Templates
export const mockTemplates: MockTemplate[] = [
  {
    id: '1',
    name: 'Welcome Email',
    subject: 'Welcome to {{company_name}}!',
    category: 'welcome',
    isPublic: true,
    createdAt: '2024-01-10T12:00:00Z'
  },
  {
    id: '2',
    name: 'Newsletter Template',
    subject: '{{newsletter_title}} - {{month}} {{year}}',
    category: 'newsletter',
    isPublic: true,
    createdAt: '2024-01-12T14:00:00Z'
  },
  {
    id: '3',
    name: 'Product Announcement',
    subject: '🎉 Introducing {{product_name}}',
    category: 'promotional',
    isPublic: false,
    createdAt: '2024-01-15T16:00:00Z'
  },
  {
    id: '4',
    name: 'Order Confirmation',
    subject: 'Order #{{order_number}} Confirmed',
    category: 'transactional',
    isPublic: true,
    createdAt: '2024-01-18T10:00:00Z'
  }
];

// Mock Recipients
export const mockRecipients: MockRecipient[] = [
  {
    id: '1',
    email: 'alice@example.com',
    firstName: 'Alice',
    lastName: 'Johnson',
    status: 'active',
    lastEmailSent: '2024-01-20T10:00:00Z',
    tags: ['customer', 'premium']
  },
  {
    id: '2',
    email: 'bob@example.com',
    firstName: 'Bob',
    lastName: 'Wilson',
    status: 'active',
    lastEmailSent: '2024-01-20T10:00:00Z',
    tags: ['customer']
  },
  {
    id: '3',
    email: 'carol@example.com',
    firstName: 'Carol',
    lastName: 'Brown',
    status: 'unsubscribed',
    lastEmailSent: '2024-01-15T09:00:00Z',
    tags: ['former-customer']
  },
  {
    id: '4',
    email: 'dave@example.com',
    firstName: 'Dave',
    lastName: 'Davis',
    status: 'bounced',
    lastEmailSent: '2024-01-10T11:00:00Z',
    tags: ['invalid-email']
  }
];

// Mock Analytics
export const mockAnalytics: MockAnalytics = {
  totalCampaigns: 12,
  totalRecipients: 2400,
  totalEmailsSent: 50000,
  averageOpenRate: 24.5,
  averageClickRate: 3.2,
  monthlyGrowth: 15.3
};

// Mock Campaign Performance Data
export const mockCampaignPerformance = [
  { date: '2024-01-01', sent: 100, opened: 25, clicked: 5 },
  { date: '2024-01-02', sent: 150, opened: 38, clicked: 8 },
  { date: '2024-01-03', sent: 200, opened: 52, clicked: 12 },
  { date: '2024-01-04', sent: 180, opened: 45, clicked: 9 },
  { date: '2024-01-05', sent: 220, opened: 58, clicked: 15 },
  { date: '2024-01-06', sent: 250, opened: 65, clicked: 18 },
  { date: '2024-01-07', sent: 300, opened: 78, clicked: 22 }
];

// Mock AI Suggestions
export const mockAISuggestions = [
  {
    type: 'subject_line',
    suggestions: [
      '🚀 Boost Your Email Marketing with AI',
      'Transform Your Campaigns Today',
      'The Future of Email Marketing is Here'
    ]
  },
  {
    type: 'content_improvement',
    suggestions: [
      'Add a clear call-to-action button',
      'Include social proof or testimonials',
      'Use more personalization tokens'
    ]
  },
  {
    type: 'send_time',
    suggestions: [
      'Tuesday 10:00 AM (highest open rate)',
      'Thursday 2:00 PM (best for B2B)',
      'Wednesday 9:00 AM (overall optimal)'
    ]
  }
];

// Mock Notification Data
export const mockNotifications = [
  {
    id: '1',
    type: 'success',
    title: 'Campaign Sent Successfully',
    message: 'Welcome Campaign has been sent to 500 recipients',
    timestamp: '2024-01-20T10:05:00Z',
    read: false
  },
  {
    id: '2',
    type: 'info',
    title: 'New Feature Available',
    message: 'AI-powered subject line optimization is now live',
    timestamp: '2024-01-19T14:30:00Z',
    read: true
  },
  {
    id: '3',
    type: 'warning',
    title: 'High Bounce Rate',
    message: 'Your recent campaign has a bounce rate of 8%',
    timestamp: '2024-01-18T09:15:00Z',
    read: false
  }
];

// Utility functions for mock data
export const getMockCampaignById = (id: string): MockCampaign | undefined => {
  return mockCampaigns.find(campaign => campaign.id === id);
};

export const getMockUserById = (id: string): MockUser | undefined => {
  return mockUsers.find(user => user.id === id);
};

export const getMockTemplateById = (id: string): MockTemplate | undefined => {
  return mockTemplates.find(template => template.id === id);
};

export const getMockRecipientById = (id: string): MockRecipient | undefined => {
  return mockRecipients.find(recipient => recipient.id === id);
};

// Mock API responses
export const mockApiResponses = {
  campaigns: {
    list: mockCampaigns,
    create: { success: true, campaign: mockCampaigns[0] },
    update: { success: true, campaign: mockCampaigns[0] },
    delete: { success: true }
  },
  templates: {
    list: mockTemplates,
    create: { success: true, template: mockTemplates[0] }
  },
  analytics: {
    overview: mockAnalytics,
    performance: mockCampaignPerformance
  },
  ai: {
    suggestions: mockAISuggestions,
    generate: {
      success: true,
      content: 'Generated email content here...',
      subject: 'Generated subject line'
    }
  }
};
