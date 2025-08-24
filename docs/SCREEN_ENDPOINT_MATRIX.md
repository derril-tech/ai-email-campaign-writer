# Screen ↔ Endpoint ↔ DTO Matrix

This document maps frontend screens to backend endpoints and data transfer objects (DTOs) to ensure alignment between UI and API.

## Authentication Flow

| Screen | Endpoint | DTO | Status |
|--------|----------|-----|--------|
| `/auth/login` | `POST /auth/login` | `UserLogin` | ✅ Implemented |
| `/auth/register` | `POST /auth/register` | `UserRegistration` | ✅ Implemented |
| Token refresh | `POST /auth/refresh` | `TokenRefresh` | ✅ Implemented |

## Dashboard & Analytics

| Screen | Endpoint | DTO | Status |
|--------|----------|-----|--------|
| `/dashboard` | `GET /campaigns` | `CampaignList` | ✅ Implemented |
| Dashboard stats | `GET /analytics/campaigns` | `AnalyticsOverview` | ✅ Implemented |
| Campaign performance | `GET /analytics/campaigns/{id}` | `CampaignAnalytics` | ✅ Implemented |
| Real-time analytics | WebSocket `/ws` | `AnalyticsEvent` | ✅ Implemented |

## Campaign Management

| Screen | Endpoint | DTO | Status |
|--------|----------|-----|--------|
| Campaign list | `GET /campaigns` | `CampaignList` | ✅ Implemented |
| Create campaign | `POST /campaigns` | `CampaignCreate` | ✅ Implemented |
| Edit campaign | `PUT /campaigns/{id}` | `CampaignUpdate` | ✅ Implemented |
| View campaign | `GET /campaigns/{id}` | `Campaign` | ✅ Implemented |
| Delete campaign | `DELETE /campaigns/{id}` | - | ✅ Implemented |
| Send campaign | `POST /campaigns/{id}/send` | - | ✅ Implemented |

## AI Content Generation

| Screen | Endpoint | DTO | Status |
|--------|----------|-----|--------|
| AI content generator | `POST /ai/generate` | `AIGenerationRequest` | ✅ Implemented |
| Advanced AI generation | `POST /ai/generate-advanced` | `AIAdvancedRequest` | ✅ Implemented |
| AI generation progress | WebSocket `/ws` | `AIGenerationProgress` | ✅ Implemented |

## Copy Corpus Management (pgvector)

| Screen | Endpoint | DTO | Status |
|--------|----------|-----|--------|
| Copy corpus list | `GET /copy-corpus` | `CopyCorpusList` | ✅ Implemented |
| Add copy entry | `POST /copy-corpus` | `CopyCorpusCreate` | ✅ Implemented |
| View copy entry | `GET /copy-corpus/{id}` | `CopyCorpusDetail` | ✅ Implemented |
| Delete copy entry | `DELETE /copy-corpus/{id}` | - | ✅ Implemented |
| Similarity search | `GET /copy-corpus?similar_to=text` | `CopyCorpusSimilar` | ✅ Implemented |

## Template Management (Mustache.js)

| Screen | Endpoint | DTO | Status |
|--------|----------|-----|--------|
| Template list | `GET /templates` | `TemplateList` | ✅ Implemented |
| Create template | `POST /templates` | `TemplateCreate` | ✅ Implemented |
| Render template | `POST /templates/{id}/render` | `TemplateRender` | ✅ Implemented |
| Template preview | `GET /templates/{id}/preview` | `TemplatePreview` | ✅ Implemented |

## A/B Testing

| Screen | Endpoint | DTO | Status |
|--------|----------|-----|--------|
| Create A/B test | `POST /campaigns/{id}/ab-test` | `ABTestCreate` | ✅ Implemented |
| View A/B test | `GET /campaigns/{id}/ab-test/{test_id}` | `ABTestResults` | ✅ Implemented |
| A/B test updates | WebSocket `/ws` | `ABTestUpdate` | ✅ Implemented |

## Load Testing & Performance

| Screen | Endpoint | DTO | Status |
|--------|----------|-----|--------|
| Load test dashboard | `GET /load-test` | `LoadTestList` | ✅ Implemented |
| Run burst test | `POST /load-test/burst` | `LoadTestBurst` | ✅ Implemented |
| View test results | `GET /load-test/{test_id}` | `LoadTestResults` | ✅ Implemented |
| Performance metrics | `GET /health` | `SystemHealth` | ✅ Implemented |

## System Configuration

| Screen | Endpoint | DTO | Status |
|--------|----------|-----|--------|
| System config | `GET /config` | `SystemConfig` | ✅ Implemented |
| Health check | `GET /health` | `HealthStatus` | ✅ Implemented |

## Missing Endpoints & Screens

### Required by Product Brief

| Screen | Endpoint | DTO | Priority |
|--------|----------|-----|----------|
| `/campaigns/new` | `POST /campaigns` | `CampaignCreate` | High |
| `/campaigns/{id}/edit` | `PUT /campaigns/{id}` | `CampaignUpdate` | High |
| `/campaigns/{id}/preview` | `GET /campaigns/{id}/preview` | `CampaignPreview` | Medium |
| `/audiences` | `GET /audiences` | `AudienceList` | High |
| `/audiences/new` | `POST /audiences` | `AudienceCreate` | High |
| `/audiences/import` | `POST /audiences/import` | `AudienceImport` | Medium |
| `/templates` | `GET /templates` | `TemplateList` | Medium |
| `/templates/new` | `POST /templates` | `TemplateCreate` | Medium |
| `/analytics` | `GET /analytics/campaigns` | `AnalyticsOverview` | High |
| `/analytics/campaigns` | `GET /analytics/campaigns` | `CampaignAnalyticsList` | High |
| `/settings` | `GET /settings` | `UserSettings` | Low |
| `/settings/profile` | `PUT /settings/profile` | `ProfileUpdate` | Low |

### Missing DTOs

```typescript
// AI Generation DTOs
interface AIGenerationRequest {
  task: 'subject_line' | 'email_body' | 'cta' | 'campaign_strategy';
  context: {
    brand_voice: string;
    target_audience: string;
    campaign_goal: string;
    key_message: string;
  };
  constraints: {
    max_tokens: number;
    temperature: number;
    include_cta: boolean;
  };
  framework: 'langchain' | 'langgraph' | 'crewai' | 'llamaindex' | 'autogen';
}

interface AIAdvancedRequest {
  task: 'campaign_strategy' | 'brand_alignment' | 'content_optimization';
  context: {
    brand_guidelines: string;
    target_audience: string;
    campaign_goal: string;
    historical_performance: string;
  };
  frameworks: {
    primary: 'crewai' | 'langgraph' | 'llamaindex';
    supporting: string[];
    quality_gates: boolean;
    human_review: boolean;
  };
}

interface AIGenerationProgress {
  task_id: string;
  status: 'processing' | 'completed' | 'failed';
  progress: number;
  estimated_completion: string;
}

// Copy Corpus DTOs (pgvector)
interface CopyCorpusList {
  entries: CopyCorpusEntry[];
  total: number;
}

interface CopyCorpusEntry {
  id: string;
  label: string;
  content: string;
  copy_type: 'subject_line' | 'email_body' | 'cta' | 'brand_voice' | 'winning_copy';
  performance_score?: string;
  similarity_score?: number;
  tags: string;
  created_at: string;
}

interface CopyCorpusCreate {
  label: string;
  content: string;
  copy_type: 'subject_line' | 'email_body' | 'cta' | 'brand_voice' | 'winning_copy';
  performance_score?: string;
  campaign_id?: string;
  tags?: string;
}

interface CopyCorpusDetail extends CopyCorpusEntry {
  similar_entries: Array<{
    id: string;
    content: string;
    similarity_score: number;
  }>;
}

// Template DTOs (Mustache.js)
interface TemplateList {
  templates: Template[];
}

interface Template {
  id: string;
  name: string;
  category: string;
  html_content: string;
  variables: string[];
  preview_image?: string;
  created_at: string;
}

interface TemplateCreate {
  name: string;
  category: string;
  html_content: string;
  variables: string[];
}

interface TemplateRender {
  variables: Record<string, any>;
}

interface TemplateRenderResponse {
  rendered_html: string;
  variables_used: string[];
  missing_variables: string[];
}

// A/B Testing DTOs
interface ABTestCreate {
  test_type: 'subject_line' | 'email_body' | 'cta';
  variants: Array<{
    name: string;
    content: string;
  }>;
  test_size: number;
  duration_hours: number;
  winning_criteria: 'open_rate' | 'click_rate' | 'conversion_rate';
}

interface ABTestResults {
  test_id: string;
  status: 'running' | 'completed' | 'failed';
  winning_variant?: string;
  confidence_level: number;
  statistical_significance: boolean;
  variants: Array<{
    id: string;
    name: string;
    sent: number;
    opened: number;
    open_rate: number;
    confidence_interval: [number, number];
  }>;
}

interface ABTestUpdate {
  test_id: string;
  variant_id: string;
  sent: number;
  opened: number;
  open_rate: number;
}

// Load Testing DTOs
interface LoadTestList {
  tests: LoadTestSummary[];
}

interface LoadTestSummary {
  test_id: string;
  scenario: string;
  status: 'running' | 'completed' | 'failed';
  created_at: string;
}

interface LoadTestBurst {
  scenario: 'campaign_creation' | 'email_sending' | 'webhook_processing';
  duration_minutes: number;
  target_users: number;
  ramp_up_minutes: number;
}

interface LoadTestResults {
  test_id: string;
  status: 'completed' | 'failed';
  scenario: string;
  summary: {
    total_requests: number;
    successful_requests: number;
    failed_requests: number;
    average_response_time: number;
    p95_response_time: number;
    p99_response_time: number;
  };
  thresholds: {
    p95_response_time: number;
    error_rate: number;
    passed: boolean;
  };
}

// Analytics DTOs
interface AnalyticsOverview {
  summary: {
    total_campaigns: number;
    total_sent: number;
    total_opened: number;
    total_clicked: number;
    avg_open_rate: number;
    avg_click_rate: number;
  };
  trends: Array<{
    date: string;
    campaigns: number;
    sent: number;
    opened: number;
    clicked: number;
  }>;
}

interface CampaignAnalytics {
  campaign_id: string;
  name: string;
  summary: {
    sent: number;
    delivered: number;
    opened: number;
    clicked: number;
    bounced: number;
    unsubscribed: number;
  };
  timeline: Array<{
    timestamp: string;
    event: string;
    count: number;
  }>;
  segments: Array<{
    segment: string;
    open_rate: number;
    click_rate: number;
  }>;
}

interface AnalyticsEvent {
  type: 'campaign_progress' | 'ai_generation_progress' | 'ab_test_update';
  data: any;
}

// System DTOs
interface SystemConfig {
  features: {
    ai_generation: boolean;
    a_b_testing: boolean;
    advanced_analytics: boolean;
    pgvector: boolean;
    load_testing: boolean;
  };
  limits: {
    max_campaigns: number;
    max_subscribers: number;
    max_ai_generations: number;
  };
  supported_providers: {
    email: string[];
    ai: string[];
    vector_db: string[];
  };
  ai_frameworks: {
    langchain: boolean;
    langgraph: boolean;
    crewai: boolean;
    llamaindex: boolean;
    autogen: boolean;
  };
}

interface HealthStatus {
  status: 'healthy' | 'unhealthy';
  timestamp: string;
  version: string;
  services: {
    database: string;
    redis: string;
    email_service: string;
    ai_service: string;
  };
}

// Audience DTOs
interface AudienceList {
  items: Audience[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

interface Audience {
  id: string;
  name: string;
  description?: string;
  subscriberCount: number;
  segmentation: Record<string, any>;
  createdAt: string;
  updatedAt: string;
}

interface AudienceCreate {
  name: string;
  description?: string;
  segmentation?: Record<string, any>;
}

interface AudienceImport {
  file: File;
  mapping: Record<string, string>;
  options: {
    skipDuplicates: boolean;
    updateExisting: boolean;
  };
}

// User Settings DTOs
interface UserSettings {
  profile: UserProfile;
  preferences: UserPreferences;
  integrations: Integration[];
}

interface UserProfile {
  firstName: string;
  lastName: string;
  email: string;
  companyName?: string;
  industry?: string;
}

interface UserPreferences {
  timezone: string;
  dateFormat: string;
  emailNotifications: boolean;
  defaultSenderEmail?: string;
  defaultSenderName?: string;
}

interface ProfileUpdate {
  firstName?: string;
  lastName?: string;
  companyName?: string;
  industry?: string;
}
```

## Navigation Structure

Based on the current infrastructure, the navigation should include:

```
/ (Landing page)
├── /auth
│   ├── /login
│   └── /register
├── /dashboard (Main dashboard with real-time analytics)
├── /campaigns
│   ├── / (Campaign list)
│   ├── /new (Create campaign with AI assistance)
│   ├── /[id] (View campaign with analytics)
│   ├── /[id]/edit (Edit campaign)
│   ├── /[id]/preview (Preview campaign)
│   └── /[id]/ab-test (A/B testing management)
├── /ai
│   ├── /generate (AI content generation)
│   ├── /generate-advanced (Advanced AI workflows)
│   └── /history (AI generation history)
├── /copy-corpus
│   ├── / (Copy corpus management)
│   ├── /new (Add new copy entry)
│   ├── /[id] (View copy entry with similarity)
│   └── /search (Similarity search)
├── /templates
│   ├── / (Template library)
│   ├── /new (Create template)
│   ├── /[id] (View template)
│   └── /[id]/render (Template rendering)
├── /audiences
│   ├── / (Audience list)
│   ├── /new (Create audience)
│   └── /import (Import audience)
├── /analytics
│   ├── / (Analytics overview)
│   ├── /campaigns (Campaign analytics)
│   └── /real-time (Real-time dashboard)
├── /load-testing
│   ├── / (Load test dashboard)
│   ├── /burst (Burst testing)
│   └── /results (Test results)
└── /settings
    ├── /profile (Profile settings)
    ├── /preferences (User preferences)
    └── /integrations (Third-party integrations)
```

## Action Items

### High Priority
1. ✅ AI content generation screens (`/ai/generate`, `/ai/generate-advanced`)
2. ✅ Copy corpus management (`/copy-corpus/*`)
3. ✅ Template management with Mustache.js (`/templates/*`)
4. ✅ A/B testing management (`/campaigns/{id}/ab-test`)
5. ✅ Load testing dashboard (`/load-testing/*`)
6. ✅ Real-time analytics integration

### Medium Priority
1. Create missing campaign management screens (`/campaigns/new`, `/campaigns/[id]/edit`)
2. Implement audience management endpoints and screens
3. Add campaign preview functionality
4. Implement audience import feature

### Low Priority
1. Add user settings and profile management
2. Implement third-party integrations
3. Add advanced analytics features

## Tech Stack Alignment

✅ **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
✅ **Backend**: FastAPI, Python 3.11+, SQLAlchemy
✅ **Database**: PostgreSQL with pgvector extension
✅ **AI**: OpenAI GPT-4, Anthropic Claude, LangChain, LangGraph, CrewAI, LlamaIndex, AutoGen
✅ **Email**: SendGrid with retry + suppression handling
✅ **Authentication**: JWT with refresh tokens
✅ **Design System**: Design tokens, component library
✅ **Templating**: Mustache.js with dynamic variables
✅ **Vector Database**: pgvector for similarity search
✅ **Testing**: Jest, Playwright (E2E), k6 (Load testing)
✅ **Real-time**: WebSocket for live analytics and AI progress

## Performance Requirements

- **Frontend**: Lighthouse ≥ 90, initial bundle < 500KB, TTI < 3s
- **Backend**: p95 < 200ms, complex queries < 50ms
- **AI Generation**: < 30 seconds for complex workflows
- **Vector Search**: < 100ms for similarity queries
- **Delivery**: Automated retries, bounce handling, deliverability alerts

## Security & Compliance

- **Auth**: JWT (15-min access, 7-day refresh), bcrypt cost 12
- **API**: Rate limits 100/min, 1000/hr, 10000/day
- **Email**: SPF, DKIM, DMARC
- **Regulatory**: GDPR, CAN-SPAM compliance
- **AI**: Token limits, temperature policies, content filtering

---

**Last Updated**: December 2024
**Version**: 2.0.0 - Updated to reflect current infrastructure with AI frameworks, pgvector, and load testing
