# THE PROJECT BRIEF #

# Project Name #

AI Email Campaign Writer

# Product Description / Presentation #


# PulseQuill — AI Email Campaign Writer

**Legendary, enterprise‑grade AI for writing, personalizing, and optimizing email at scale.**
*Write. Personalize. Ship. Learn — in real time.*

---

## 1) Executive Snapshot

* **What it is:** Multi‑model, production‑ready email campaign writer with real‑time analytics and predictive optimization.
* **Who it’s for:** Fortune 500 growth, lifecycle, and CRM teams; agencies; high‑volume senders.
* **Why it wins:** Orchestrates GPT‑4 + Claude for best‑of‑breed copy **and** brand consistency. Ships with strict compliance, rock‑solid delivery, and live performance feedback loops.

---

## 2) System Architecture (Production‑Ready)

**Frontend:** Next.js 14 • React 18 • TypeScript • Tailwind CSS • Framer Motion
**Backend:** FastAPI (Python 3.9+) • SQLAlchemy 2.0 (async) • JWT Auth
**Data:** PostgreSQL 15 • pgvector • Redis (sessions/cache/rate limiting)
**AI:** OpenAI GPT‑4 • Anthropic Claude • LangChain orchestration
**Realtime:** Socket.io over ASGI
**Delivery:** SendGrid (primary) with retry + suppression handling
**Deploy:** Vercel (FE) • Render (BE) • Managed PostgreSQL • Cloud object storage

```
[Browser]
  └─ Next.js App Router (SSR/ISR) — Tailwind, Framer Motion, WCAG AA
       └─ WebSocket client (Socket.io)
[API]
  └─ FastAPI (ASGI): Auth, Campaigns, Templating, AI Orchestrator, Webhooks
       ├─ LangChain Router → (GPT‑4 | Claude)
       ├─ Mustache.js templating service
       ├─ Analytics stream (events → Redis queue → Postgres)
       └─ SendGrid delivery + webhooks
[Data]
  ├─ PostgreSQL (OLTP + pgvector)
  └─ Redis (sessions, caches, rate limits, queues)
```

---

## 3) AI Content Engine

**Model Selection Logic**

| Task                                                 | Preferred Model       | Notes                               |
| ---------------------------------------------------- | --------------------- | ----------------------------------- |
| Subject lines, CTAs, variants                        | **GPT‑4**             | Punchy creativity, concise copy     |
| Brand voice, tone alignment, complex personalization | **Claude**            | Long‑context, nuanced style control |
| Long‑form nurture emails / value content             | Claude → GPT‑4 polish | Claude drafts, GPT‑4 tightens       |

**Token & Temperature Policy**

* **Token cap:** ≤ **2000** tokens per generation (hard stop + auto‑trim).
* **Dynamic temperature:** 0.3 (compliance notices) → 0.9 (creative brainstorm).
* **Heuristic:** Higher prior engagement → lower temperature; new segment tests → higher.

**Structured Prompt Skeleton**

```yaml
objective: "Drive demo signups for {segment}"
brand_guidelines:
  voice: "confident, human, no hype"
  words_to_use: ["platform", "automate", "secure"]
  words_to_avoid: ["revolutionary", "disrupt"]
audience_context:
  persona: {persona}
  pains: [ ... ]
  triggers: [ ... ]
assets:
  offer: {offer}
  social_proof: {proof}
output:
  format: "email_html"
  variants: 3
  constraints: {links_mustache_vars: true, max_tokens: 2000}
```

**Quality Gate (Brand Compliance & QA)**

1. LLM draft → 2) Style lint (forbidden words, tone checks) → 3) Fact/URL validator → 4) CAN‑SPAM/GDPR footer injection → 5) Human preview.

---

## 4) Campaign Studio (Email Specs)

* **Templating:** **Mustache.js** with dynamic variables (e.g., `{{first_name}}`, `{{last_seen_at}}`).
* **Responsive:** Mobile‑first breakpoints **320/768/1024/1440**; table‑based HTML for Outlook.
* **Compatibility:** Gmail, Outlook, Apple Mail, Yahoo (VML fallbacks for Outlook).
* **Images:** Auto compress + WebP with PNG/JPEG fallbacks; CDN cache‑control.
* **Link Tracking:** Per‑recipient signed query (campaign, variant, recipient\_id, utm\_\*).
* **Unsubscribe:** One‑click, always‑visible; tenant‑wide suppression; **CAN‑SPAM/GDPR** compliant.

---

## 5) Real‑time Analytics & Experimentation

* **WebSockets (Socket.io):** Live status: queued → delivered → opened → clicked → bounced → spam → unsubscribed.
* **Event schema:** `send`, `deliver`, `open`, `click`, `bounce`, `spam_report`, `unsubscribe`.
* **Key Metrics (live):**

  * **Delivery Rate** = Delivered / Sent × 100
  * **Open Rate** = Opened / Delivered × 100
  * **Click Rate** = Clicked / Opened × 100
  * **Bounce Rate** = Bounced / Sent × 100
* **A/B Testing:** Two‑proportion z‑test with **Wilson 95% CI**, sequential monitoring guard (peeking‑safe).
* **Predictive Analytics:** Gradient boosting for engagement probability; features: send‑time, prior opens/clicks, subject length, emoji use, segment fit; model refreshed nightly.

---

## 6) UX System (AA Accessible)

* **Design Tokens:**

  * Colors: Primary **#3B82F6**, Secondary **#8B5CF6**, Success **#10B981**, Warning **#F59E0B**, Error **#EF4444**
  * Type: Inter, base 14px; `1.25` modular scale
  * Spacing grid: **4px** increments (4, 8, 16, 24, 32, 48, 64)
* **Motion:** Framer Motion micro‑interactions, **300ms** duration, ease‑out.
* **Loading:** Skeletons for lists/editors; progress bars for AI generation.
* **Errors:** Friendly, actionable remediation; preserve user input.
* **Accessibility:** Keyboard reachable, ARIA roles, color‑contrast AA, focus rings, reduced‑motion prefs.

---

## 7) Data Model (PostgreSQL + pgvector)

```sql
-- Users
create type plan_t as enum ('free','pro','enterprise');
create table users (
  id uuid primary key default gen_random_uuid(),
  email citext unique not null,
  plan plan_t not null default 'free',
  password_hash text not null,
  created_at timestamptz default now()
);

-- Audiences & Subscribers
create table audiences (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid references users(id),
  name text not null,
  segmentation jsonb default '{}',
  subscriber_count int default 0,
  created_at timestamptz default now()
);

-- Campaigns
create type campaign_status as enum ('draft','scheduled','sending','paused','completed','failed');
create table campaigns (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid references users(id),
  name text not null,
  status campaign_status not null default 'draft',
  subject text,
  html_template text not null,
  mustache_vars jsonb default '{}',
  schedule_at timestamptz,
  analytics jsonb default '{}',
  created_at timestamptz default now()
);
create index on campaigns(owner_id);
create index on campaigns(status);

-- Email Events
create table email_events (
  id bigserial primary key,
  campaign_id uuid references campaigns(id),
  recipient_id uuid,
  event_type text check (event_type in
    ('send','deliver','open','click','bounce','spam_report','unsubscribe')),
  url text,
  meta jsonb,
  occurred_at timestamptz not null default now()
);
create index on email_events(campaign_id, event_type, occurred_at);

-- Vector store for brand voice examples / prior winners
create table copy_corpus (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid references users(id),
  label text,
  content text,
  embedding vector(1536)
);
```

**Indexes & Perf:** B‑tree on `status`, `owner_id`; composite on `(campaign_id, event_type, occurred_at)`; GIN on JSONB fields.

**Redis (TTL):** sessions **7d**; analytics aggregates **1h**; AI generation cache **24h**; rate limit (sliding window) keys per IP/user.

**Retention:** GDPR‑aligned policies per tenant; auto cleanup for stale events and soft‑deleted recipients.

---

## 8) Performance SLOs

* **Frontend:** Lighthouse ≥ **90** across the board; initial bundle < **500KB**; TTI < **3s**.
* **Backend:** p95 **< 200ms**; complex queries **< 50ms**; background jobs via **Celery + Redis**.
* **Delivery:** Automated retries, bounce handling, suppression list integrity, deliverability alerts.

---

## 9) Security & Compliance

* **Auth:** JWT (15‑min access, 7‑day refresh); bcrypt cost 12.
* **API:** Rate limits **100/min, 1000/hr, 10000/day**; HSTS, CORS allowlist.
* **Encryption:** AES‑256 at rest; TLS in transit.
* **Email Trust:** SPF, DKIM, DMARC.
* **Regulatory:** GDPR DPA, CAN‑SPAM, SOC 2 controls, granular data export/delete.

---

## 10) API & Integrations

**REST Patterns:** `/v1/campaigns`, `/v1/audiences`, `/v1/content/variants`, `/v1/events`, `/v1/webhooks/sendgrid`
**Webhooks Out:** `campaign.completed`, `abtest.winner`, `threshold.alert`
**3rd‑Party:** Salesforce/HubSpot/Pipedrive (contacts & deals), GA/Mixpanel/Amplitude (attribution), Stripe (plans, metering).
**Docs:** OpenAPI 3.0 with Swagger UI.

---

## 11) DevOps & Observability

* **CI/CD:** GitHub Actions → Vercel/Render; pre‑commit (ruff, black, mypy, eslint, stylelint).
* **Logs & Metrics:** Structured JSON logs, Prometheus metrics, Grafana dashboards, on‑call alerts.
* **Rollout:** Blue/green on API; canary for model‑prompt changes; feature flags per tenant.

---

## 12) Testing Strategy (≥90% coverage)

* **Unit:** Prompt builders, validators, template renderer.
* **Integration:** SendGrid sandbox, webhook ingestion, DB migrations.
* **E2E:** Playwright flows (compose → preview → send → analyze).
* **Load:** k6 scenarios (burst sends, sustained sends, webhook fan‑in).

---

## 13) Claude‑Ready Prompt Pack (Run in Sequence)

**P1 — Project Setup & Architecture**
"Create the complete project structure and architecture for PulseQuill… (Next.js 14 + TS + Tailwind; FastAPI + SQLAlchemy + JWT; Postgres + pgvector + Redis; Vercel/Render). Include env files, Docker, Makefile, OpenAPI stub."

**P2 — Core Backend Implementation**
"Implement FastAPI services: auth, campaigns, audiences, template rendering (Mustache), AI orchestration (model router + token/temperature policies), SendGrid webhook ingestion, Socket.io, logging/error middleware."

**P3 — Frontend Components & UI**
"Build React components: Campaign Builder, Prompt Studio, Variant Comparator, Audience Segments, Live Analytics, A/B Lab, Settings. Add WCAG AA, dark/light, skeletons, motion."

**P4 — AI Integration & Features**
"Wire GPT‑4 + Claude via LangChain with model selection rules, quality gate, vector retrieval for brand voice, and generation cache. Produce 3 variants + subject lines + CTAs per brief."

**P5 — Deployment & Optimization**
"Ship to Vercel/Render with perf budgets, caching headers, DB indexes, Celery workers, OpenAPI docs, alerting, and backup/retention jobs."

---

## 14) Example API Sketches

```http
POST /v1/content/generate
Authorization: Bearer <token>
{
  "campaign_id": "…",
  "brief": {"objective":"win-back","persona":"ops_manager", "offer":"20% off"},
  "variants": 3,
  "temperature": "auto"
}

POST /v1/campaigns/{id}/send
POST /v1/audiences/import
GET  /v1/events?campaign_id=…&type=open
```

---

## 15) Model Router Pseudocode

```python
def choose_model(task, persona_complexity, needs_brand_guardrails):
    if task in {"subject", "cta", "short_variant"}:
        return "gpt-4"
    if needs_brand_guardrails or persona_complexity == "high":
        return "claude"
    return "gpt-4"

def auto_temperature(context_risk, experiment_phase):
    base = 0.5
    if context_risk == "regulated":
        base = 0.3
    if experiment_phase in {"explore","ab_test_new"}:
        base += 0.3
    return min(max(base, 0.1), 0.9)
```

---

## 16) Success KPIs

* Copy production speed **+300%**; deliverability **>98%**; open rate **+15–30%**; time‑to‑ship **< 15 min** from brief to send.
* Lighthouse **≥95** (FE); API p95 **<200ms**; test coverage **>90%**.

---

### Ready to build PulseQuill?

Ship the five prompts above, and you’ll generate a deployable, enterprise‑grade AI email platform in hours—not months.




FOLLOW THIS 8 STEP PLAN TO PREPARE THE INFRASTRUCTURE
-----------------------------------------------------

# 🚀 Claude Fullstack Repo Prep – Optimized 8 Step Plan

  
The goal: build an extensive frontend + backend scaffold so Claude Code only has to finish ~20% of the work.  
Each step must be **completed ** before advancing  (this is important).
IMPORTANT: YOU ARE BUILDING ONLY THE INFRASTRUCTURE OF THE APPLICATION NOT THE APPLICATION ITSELF !!!. FOLLOW THE STEPS IN NUMERICAL ORDER !!! starting from step 1.
You are doing the groundwork for the application, including setting up the folder structure, configuration files, and any necessary boilerplate code.
IMPORTANT: the checklist in each step has to be checked off 100% before moving to the next step. And always provide comments to your code blocks so that even a non-tech person can understand what you have done.

---

## STEP 1 — Build the Rich Infrastructure
Create a **deep scaffold** for both frontend and backend so Claude code can recognize the architecture immediately.

- Build a **frontend app shell** with routing, placeholder pages, components, and styling setup.  
- Build a **backend app shell** with API structure, health endpoint, and config in place.  
- Include `REPO_MAP.md`, `API_SPEC.md`, and a draft `CLAUDE.md` in the `docs/` folder.  (create the docs folder if it does not  already exist)
- Add **TODO markers and folder-level `_INSTRUCTIONS.md`** files so Claude knows exactly where to add logic.

**Deliverables**
- Frontend app shell with routing, placeholder pages, components, and styling setup  
- Backend app shell with API structure, health endpoint, and config  
- `docs/REPO_MAP.md`, `docs/API_SPEC.md` (stub), and draft `docs/CLAUDE.md`  
- TODO markers + folder-level `_INSTRUCTIONS.md` files  

**Checklist**
- [ ] Frontend scaffold built  
- [ ] Backend scaffold built 
- [ ] Docs folder created with drafts (`REPO_MAP.md`, `API_SPEC.md`, `CLAUDE.md`)  
- [ ] TODO markers and `_INSTRUCTIONS.md` stubs in place  

---

## STEP 2 — Enrich the Scaffold
If the repo looks shallow, enrich it so Claude needs fewer leaps of imagination.  

Add:
- Sample frontend routes and components (`/`, `/about`, `/dashboard`)  
- Domain model stubs and types/interfaces  
- Mock data + fixtures for UI flows  
- README files with quick run instructions for both frontend and backend  
- Instructions embedded in folders (e.g. `CLAUDE_TASK: …`)

**Deliverables**
- Sample routes and pages (`/`, `/about`, `/dashboard`)  
- Domain model stubs and type definitions  
- Mock data and fixtures for UI flows  
- README files for frontend and backend with run instructions  
- Folder-level instructions (`_INSTRUCTIONS.md`)  

**Checklist**
- [ ] At least 2–3 sample routes/pages exist  
- [ ] Domain types/interfaces stubbed out  
- [ ] Mock data + fixtures included  
- [ ] README_FRONTEND.md and README_BACKEND.md added  
- [ ] Each folder has `_INSTRUCTIONS.md` where relevant 

---

## STEP 3 — Audit for Alignment
Check that the scaffold actually matches the product brief, tech specs, and UX /UI goals.
Add additional UI/UX elements (if needed) to make the application visually appealing (and update the design requirements after that)

- Do navigation and pages reflect the product’s main flows?  
- Do API endpoints match the UI needs?  
- Is the chosen tech stack consistent (no unused or conflicting libraries)?  
- Is the UX direction reflected (design tokens, layout, component stubs)?

**Deliverables**
- Alignment review across Product ↔ UI/UX ↔ Tech  
- Identify any missing flows, mismatched libraries, or conflicting instructions  

**Checklist**
- [ ] Navigation structure matches product journeys  
- [ ] Components/pages map to required features  
- [ ] API endpoints cover MVP needs  
- [ ] No contradictory or unused technologies  

---

## STEP 4 — Document the Architecture
Now make the docs **Claude-ready**:

- **REPO_MAP.md**: Full repo breakdown with roles of each folder  
- **API_SPEC.md**: Endpoints, payloads, error handling  
- **CLAUDE.md**: Editing rules, coding conventions, AI collaboration guidelines  

These three files are the **context backbone** Claude will use to understand the repo.

**Deliverables**
- `REPO_MAP.md`: full repo breakdown with folder purposes  
- `API_SPEC.md`: endpoints, models, error conventions  
- `CLAUDE.md`: collaboration rules, editing boundaries  

**Checklist**
- [ ] REPO_MAP.md fully describes structure  
- [ ] API_SPEC.md covers all MVP endpoints and schemas  
- [ ] CLAUDE.md includes project overview, editing rules, examples  

---

## STEP 5 — Improve the Prompt
Enhance the prompt (in `docs/PROMPT_DECLARATION.md`) with details Claude needs:

- FE/BE boundaries and data contracts  
- UX guidelines (states, accessibility, interaction patterns)  
- Performance budgets (bundle size, API latency)  
- Security constraints (auth, rate limits, PII handling)  
- Testing expectations (unit, integration, end-to-end)

**Deliverables**
- FE/BE boundaries and contracts  
- UX guidelines (states, accessibility, patterns)  
- Performance budgets (bundle size, latency targets)  
- Security constraints (auth, PII, rate limits)  
- Testing expectations  

**Checklist**
- [ ] Prompt includes FE/BE division of responsibility  
- [ ] UX principles and design tokens specified  
- [ ] Performance/security/testing requirements added  
- [ ] Prompt is concrete and actionable for Claude  

---

## STEP 6 — Expert Audit of the Prompt
Now do a **meticulous audit** of the one-page prompt declaration.

- Add Frontend Architecture, Backend Architecture, Design requirements, Core Integrations, Success Criteria, Implementation Guidelines and Security & Compliance categories from this Project Brief to the prompt declaration.
- Remove inconsistencies, duplicates, or unused technologies  
- Ensure Tech Stack → Product → Scaffold alignment (no mismatches)  
- Add UI/UX details that make the product visually appealing and usable  
- Double-check frontend and backend folders are ready  
- Confirm editing boundaries are clear (what Claude can/can’t touch)  
- Make the declaration **battle-tested and handoff-ready**

**Deliverables**
- Remove inconsistencies/duplicates  
- Ensure stack ↔ product ↔ scaffold alignment  
- Add UI/UX and accessibility details  
- Clarify file boundaries (editable vs do-not-touch)  
- Confirm prompt uses Claude-friendly syntax  

**Checklist**
- [ ] No unused or contradictory tech remains  
- [ ] UI/UX directives are product-specific and sufficient  
- [ ] Editing boundaries explicitly defined  
- [ ] Prompt syntax uses clear, imperative instructions  

---

## STEP 7 — Bird’s-Eye Repo Review
Do a quick top-level scan for missing pieces:

- All folders contain either code or `_INSTRUCTIONS.md`  
- `.env.example` files exist for both frontend and backend  
- CI/CD config is present and not trivially broken  
- Run scripts (`npm run dev`, `uvicorn …`) work end-to-end  
- No orphan TODOs without clear ownership

**Deliverables**
- Verify all core files exist  
- Confirm environment, CI, and scripts work end-to-end  

**Checklist**
- [ ] Every folder has code or `_INSTRUCTIONS.md`  
- [ ] `.env.example` present for both frontend and backend  
- [ ] CI pipeline triggers and passes basic checks  
- [ ] Dev script (`scripts/dev.sh`) runs both FE and BE  

---

## STEP 8 — Finalize CLAUDE.md
This is where Claude gets its **onboarding pack**. Make sure `CLAUDE.md` includes:

- **Project Overview**: one-paragraph purpose, stack, goals, target users  
- **Folder & File Structure**: what’s editable vs do-not-touch  
- **Coding Conventions**: style guides, naming rules, commenting expectations  
- **AI Collaboration Rules**: response format, edit rules, ambiguity handling  
- **Editing Rules**: full-file vs patches, locked files  
- **Dependencies & Setup**: frameworks, services, env vars  
- **Workflow & Tools**: how to run locally, FE/BE boundary, deployment notes  
- **Contextual Knowledge**: product quirks, domain rules, business logic caveats  
- **Examples**: good vs bad AI answer

**Deliverables**
- Project overview (purpose, stack, goals, users)  
- Folder & file structure with editable vs do-not-touch  
- Coding conventions (style, naming, commenting)  
- AI collaboration rules (response style, edit rules, ambiguity handling)  
- Dependencies and setup instructions  
- Workflow, deployment notes, contextual knowledge  
- Good vs bad answer examples  
- Fill out all the missing information in the CLAUDE.md file

**Checklist**
- [ ] Project overview section filled in  
- [ ] File boundaries clearly defined  
- [ ] Coding/style conventions included  
- [ ] AI collaboration & editing rules written  
- [ ] Dependencies & env notes covered  
- [ ] Workflow & deployment info added  
- [ ] Contextual knowledge documented  
- [ ] Good vs bad examples included  
- [ ] CLAUDE.md file does not miss any important information

---

# ✅ Outcome
When this 8-step plan is followed:
- The repo is a **rich, opinionated scaffold** (80% done).  
- Docs give Claude **clear boundaries + context**.  
- The one-page prompt is **battle-tested** and aligned.  
- Claude Code can safely and efficiently generate the missing 20%.  












