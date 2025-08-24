
# Product Brief

⚠️ IMPORTANT  
This document defines the **product’s purpose, users, and goals**.  
The infrastructure plan (`INFRASTRUCTURE_PLAN.md`) must always be aligned with this brief.

---

## 1. Product Name
PulseQuill
---

## 2. Product Purpose

AI Email Campaign Writer



Legendary, enterprise‑grade AI for writing, personalizing, and optimizing email at scale.
Write. Personalize. Ship. Learn — in real time.


1) Executive Snapshot
•
What it is: Multi‑model, production‑ready email campaign writer with real‑time analytics and predictive optimization.
•
Who it’s for: Fortune 500 growth, lifecycle, and CRM teams; agencies; high‑volume senders.
•
Why it wins: Orchestrates GPT‑4 + Claude for best‑of‑breed copy and brand consistency. Ships with strict compliance, rock‑solid delivery, and live performance feedback loops.

2) System Architecture (Production‑Ready)
Frontend: Next.js 14 • React 18 • TypeScript • Tailwind CSS • Framer Motion
Backend: FastAPI (Python 3.9+) • SQLAlchemy 2.0 (async) • JWT Auth
Data: PostgreSQL 15 • pgvector • Redis (sessions/cache/rate limiting)
AI: OpenAI GPT‑4 • Anthropic Claude • LangChain orchestration
Realtime: Socket.io over ASGI

Delivery: SendGrid (primary) with retry + suppression handling
Deploy: Vercel (FE) • Render (BE) • Managed PostgreSQL • Cloud object storage
[Browser] └─ Next.js App Router (SSR/ISR) — Tailwind, Framer Motion, WCAG AA └─ WebSocket client (Socket.io) [API] └─ FastAPI (ASGI): Auth, Campaigns, Templating, AI Orchestrator, Webhooks ├─ LangChain Router → (GPT‑4 | Claude) ├─ Mustache.js templating service ├─ Analytics stream (events → Redis queue → Postgres) └─ SendGrid delivery + webhooks [Data] ├─ PostgreSQL (OLTP + pgvector) └─ Redis (sessions, caches, rate limits, queues)


3) AI Content Engine

**Framework Architecture**:
- **LangChain**: Core orchestration, model selection, prompt templates
- **LangGraph**: Quality gate workflows, A/B testing orchestration
- **CrewAI**: Multi-agent collaboration (strategist, writer, brand specialist)
- **LlamaIndex**: RAG for brand guidelines and historical data
- **AutoGen**: Human-in-the-loop approvals and reviews
- **pgvector**: Vector similarity for brand voice matching

**Model Selection Logic**:
| Task | Preferred Model | Notes |
|------|----------------|-------|
| Subject lines, CTAs, variants | GPT‑4 | Punchy creativity, concise copy |
| Brand voice, tone alignment, complex personalization | Claude | Long‑context, nuanced style control |
| Long‑form nurture emails / value content | Claude → GPT‑4 polish | Claude drafts, GPT‑4 tightens |
Token & Temperature Policy
•

Token cap: ≤ 2000 tokens per generation (hard stop + auto‑trim).
•
Dynamic temperature: 0.3 (compliance notices) → 0.9 (creative brainstorm).
•

Heuristic: Higher prior engagement → lower temperature; new segment tests → higher.
Structured Prompt Skeleton
objective: "Drive demo signups for {segment}" brand_guidelines: voice: "confident, human, no hype"
words_to_use: ["platform", "automate", "secure"] words_to_avoid: ["revolutionary", "disrupt"] audience_context: persona: {persona} pains: [ ... ] triggers: [ ... ] assets: offer: {offer} social_proof: {proof} output: format: "email_html" variants: 3 constraints: {links_mustache_vars: true, max_tokens: 2000}
Quality Gate (Brand Compliance & QA)

**LangGraph Workflow**:
1. **LLM draft** (LangChain) → 
2. **Style lint** (forbidden words, tone checks) → 
3. **Fact/URL validator** → 
4. **CAN‑SPAM/GDPR footer injection** → 
5. **Human preview** (AutoGen if required)
4) Campaign Studio (Email Specs)
•
Templating: Mustache.js with dynamic variables (e.g., {{first_name}}, {{last_seen_at}}).
•
Responsive: Mobile‑first breakpoints 320/768/1024/1440; table‑based HTML for Outlook.
•
Compatibility: Gmail, Outlook, Apple Mail, Yahoo (VML fallbacks for Outlook).
•
Images: Auto compress + WebP with PNG/JPEG fallbacks; CDN cache‑control.
•
Link Tracking: Per‑recipient signed query (campaign, variant, recipient_id, utm_*).
•
Unsubscribe: One‑click, always‑visible; tenant‑wide suppression; CAN‑SPAM/GDPR compliant.
5) Real‑time Analytics & Experimentation
•
WebSockets (Socket.io): Live status: queued → delivered → opened → clicked → bounced → spam → unsubscribed.
•
Event schema: send, deliver, open, click, bounce, spam_report, unsubscribe.
•
Key Metrics (live):
o
Delivery Rate = Delivered / Sent × 100
o
Open Rate = Opened / Delivered × 100
o
Click Rate = Clicked / Opened × 100
o
Bounce Rate = Bounced / Sent × 100
•

A/B Testing: Two‑proportion z‑test with Wilson 95% CI, sequential monitoring guard (peeking‑safe). **LangGraph orchestrates the A/B testing workflow**.
•

Predictive Analytics: Gradient boosting for engagement probability; features: send‑time, prior opens/clicks, subject length, emoji use, segment fit; model refreshed nightly. **Uses pgvector for similarity-based predictions**.
6) UX System (AA Accessible)
•

Design Tokens:
o
Colors: Primary #3B82F6, Secondary #8B5CF6, Success #10B981, Warning #F59E0B, Error #EF4444
o
Type: Inter, base 14px; 1.25 modular scale
o
Spacing grid: 4px increments (4, 8, 16, 24, 32, 48, 64)
•
Motion: Framer Motion micro‑interactions, 300ms duration, ease‑out.
•
Loading: Skeletons for lists/editors; progress bars for AI generation.
•
Errors: Friendly, actionable remediation; preserve user input.
•

Accessibility: Keyboard reachable, ARIA roles, color‑contrast AA, focus rings, reduced‑motion prefs.



7) Data Model (PostgreSQL + pgvector)
-- Users create type plan_t as enum ('free','pro','enterprise');
create table users ( id uuid primary key default gen_random_uuid(), email citext unique not null, plan plan_t not null default 'free', password_hash text not null, created_at timestamptz default now() ); -- Audiences & Subscribers create table audiences ( id uuid primary key default gen_random_uuid(), owner_id uuid references users(id), name text not null, segmentation jsonb default '{}', subscriber_count int default 0, created_at timestamptz default now() ); -- Campaigns create type campaign_status as enum ('draft','scheduled','sending','paused','completed','failed'); create table campaigns ( id uuid primary key default gen_random_uuid(), owner_id uuid references users(id), name text not null, status campaign_status not null default 'draft', subject text, html_template text not null, mustache_vars jsonb default '{}', schedule_at timestamptz, analytics jsonb default '{}', created_at timestamptz default now() ); create index on campaigns(owner_id); create index on campaigns(status); -- Email Events create table email_events ( id bigserial primary key,
campaign_id uuid references campaigns(id), recipient_id uuid, event_type text check (event_type in ('send','deliver','open','click','bounce','spam_report','unsubscribe')), url text, meta jsonb, occurred_at timestamptz not null default now() ); create index on email_events(campaign_id, event_type, occurred_at); -- Vector store for brand voice examples / prior winners (pgvector + LlamaIndex)
create table copy_corpus ( 
    id uuid primary key default gen_random_uuid(), 
    owner_id uuid references users(id), 
    label text, 
    content text, 
    embedding vector(1536) 
);
Indexes & Perf: B‑tree on status, owner_id; composite on (campaign_id, event_type, occurred_at); GIN on JSONB fields.
Redis (TTL): sessions 7d; analytics aggregates 1h; AI generation cache 24h; rate limit (sliding window) keys per IP/user.
Retention: GDPR‑aligned policies per tenant; auto cleanup for stale events and soft‑deleted recipients.
8) Performance SLOs
•
Frontend: Lighthouse ≥ 90 across the board; initial bundle < 500KB; TTI < 3s.
•
Backend: p95 < 200ms; complex queries < 50ms; background jobs via Celery + Redis.
•
Delivery: Automated retries, bounce handling, suppression list integrity, deliverability alerts.

9) Security & Compliance
•
Auth: JWT (15‑min access, 7‑day refresh); bcrypt cost 12.
•
API: Rate limits 100/min, 1000/hr, 10000/day; HSTS, CORS allowlist.
•
Encryption: AES‑256 at rest; TLS in transit.
•
Email Trust: SPF, DKIM, DMARC.
•
Regulatory: GDPR DPA, CAN‑SPAM, SOC 2 controls, granular data export/delete.

10) API & Integrations
REST Patterns: /v1/campaigns, /v1/audiences, /v1/content/variants, /v1/events, /v1/webhooks/sendgrid

Webhooks Out: campaign.completed, abtest.winner, threshold.alert
3rd‑Party: Salesforce/HubSpot/Pipedrive (contacts & deals), GA/Mixpanel/Amplitude (attribution), Stripe (plans, metering).
Docs: OpenAPI 3.0 with Swagger UI.
11) DevOps & Observability
•
CI/CD: GitHub Actions → Vercel/Render; pre‑commit (ruff, black, mypy, eslint, stylelint).
•
Logs & Metrics: Structured JSON logs, Prometheus metrics, Grafana dashboards, on‑call alerts.
•
Rollout: Blue/green on API; canary for model‑prompt changes; feature flags per tenant.

12) Testing Strategy (≥90% coverage)
•
Unit: Prompt builders, validators, template renderer.
•
Integration: SendGrid sandbox, webhook ingestion, DB migrations.
•
E2E: Playwright flows (compose → preview → send → analyze).
•
Load: k6 scenarios (burst sends, sustained sends, webhook fan‑in).



14) Example API Sketches
POST /v1/content/generate Authorization: Bearer <token> { "campaign_id": "…", "brief": {"objective":"win-back","persona":"ops_manager", "offer":"20% off"}, "variants": 3, "temperature": "auto" } POST /v1/campaigns/{id}/send POST /v1/audiences/import GET /v1/events?campaign_id=…&type=open

15) Model Router Pseudocode
def choose_model(task, persona_complexity, needs_brand_guardrails): if task in {"subject", "cta", "short_variant"}: return "gpt-4" if needs_brand_guardrails or persona_complexity == "high": return "claude" return "gpt-4" def auto_temperature(context_risk, experiment_phase): base = 0.5 if context_risk == "regulated": base = 0.3 if experiment_phase in {"explore","ab_test_new"}: base += 0.3 return min(max(base, 0.1), 0.9)
16) Success KPIs
•
Copy production speed +300%; deliverability >98%; open rate +15–30%; time‑to‑ship < 15 min from brief to send.
•
Lighthouse ≥95 (FE); API p95 <200ms; test coverage >90%.
Ready to build PulseQuill?
Ship the five prompts above, and you’ll generate a deployable, enterprise‑grade AI email platform in hours—not months.