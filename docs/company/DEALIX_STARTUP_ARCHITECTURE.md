# Dealix — Startup Architecture

> **Source of truth for the Dealix company + product architecture.**
> Branch: `phase/startup-architecture-brand-os`
> Status: Living document. All outbound is draft-only by default (`OUTBOUND_MODE=draft_only`).
> Language note: Arabic is the primary positioning language of the company; this English file mirrors the Arabic-first brand and is kept in sync with `DEALIX_COMPANY_OS_AR.md`.

---

## 1. Positioning

**Dealix is a Saudi B2B AI Operating Systems company.**

Dealix does not sell a chatbot, a CRM, a dashboard, an agency service, or a generic automation tool. Dealix designs, ships, and operates compact AI operating systems — one per commercial function — that plug into Saudi SMEs and mid-market companies and run that function end-to-end: discovery, decision, delivery, and proof.

The company is incorporated as a Saudi limited liability company (LLC) and operates under Saudi law, Saudi PDPL, ZATCA e-invoicing rules, and Asia/Riyadh as its default timezone. Pricing is in SAR. Brand voice is Arabic-first, with English mirrors for investors and international partners.

Operating doctrine:

> AI explores, analyzes, and recommends. Deterministic workflows execute. Humans approve critical external commitments.
> No autonomous external sending. No fake clients, testimonials, or guaranteed ROI. All forecasts are scenario-based with explicit confidence levels and assumptions.

---

## 2. The 14 Core Products

Dealix ships 14 productized AI operating systems. Each one is a self-contained function with defined inputs, outputs, approval gates, and proof artifacts. They are sold individually and bundled.

| # | Product (EN) | المنتج (AR) | Function |
|---|---|---|---|
| 1 | Revenue Command Room OS | غرفة قيادة الإيرادات | Daily revenue command: pipeline, outreach drafts, CEO brief, KPIs. |
| 2 | Company Brain OS | دماغ الشركة | Central knowledge + memory layer: decisions, playbooks, client context. |
| 3 | WhatsApp / Inbox Follow-up OS | نظام متابعة الواتساب والبريد | Drafted, approval-gated follow-ups across WhatsApp and inbox. No live send by default. |
| 4 | Email Outreach Review OS | نظام مراجعة بريد التواصل | Drafted outbound email, review queue, approval before any send. |
| 5 | SMS Notification / Follow-up OS | نظام إشعارات ومتابعة SMS | Drafted SMS notifications and follow-ups; `SMS_SEND_ENABLED=false` by default. |
| 6 | AI Trust & Compliance OS | نظام الثقة والامتثال بالذكاء الاصطناعي | PDPL controls, approval classes, audit trails, no-overclaim register, evidence packs. |
| 7 | Client Delivery OS | نظام تسليم العملاء | Discovery → build → test → success report per client. |
| 8 | Controlled Live Outbound OS | نظام التواصل الحي المُحكم | Strictly gated live outbound; requires `EXTERNAL_SEND_ENABLED=true` + per-channel flags. Default off. |
| 9 | Founder Decision Desk | مكتب قرارات المؤسس | Daily decision queue, escalation matrix, delegation matrix. |
| 10 | Company Diagnosis Sprint | سprints تشخيص الشركة | Paid 1-week diagnostic: pain mapping, data audit, baseline, recommendation. |
| 11 | Offer Intelligence OS | نظام ذكاء العروض | Offer ladder, pricing engine, sector-specific offer generation. |
| 12 | Market & Competitor Watch OS | نظام مراقبة السوق والمنافسين | Sector radar, competitor signals, market shifts, Saudi regulatory updates. |
| 13 | Proposal + Contract OS | نظام العروض والعقود | Proposal and contract generation, ZATCA-aware invoicing, Moyasar payment links. |
| 14 | Executive Proof Pack OS | نظام حزم الإثبات التنفيذية | Baseline → after → documented delta proof packs for executives. |

All 14 products share the same trust engine, approval gates, and draft-only-by-default outbound posture.

---

## 3. Architecture Layers

The Dealix platform is layered. Each layer is independently deployable and independently testable.

### Layer 0 — Trust & Policy Kernel
- PDPL-aware controls (`integrations/pdpl.py`)
- Approval classes and audit trails
- No-overclaim register (forbidden claims: guaranteed ROI, specific percentages, fake testimonials)
- Outbound send flags (all default off):
  - `EXTERNAL_SEND_ENABLED=false`
  - `EMAIL_SEND_ENABLED=false`
  - `WHATSAPP_SEND_ENABLED=false`
  - `WHATSAPP_ALLOW_LIVE_SEND=false`
  - `SMS_SEND_ENABLED=false`
  - `OUTBOUND_MODE=draft_only`
- Secrets from `.env` only; `SecretStr` for every secret; gitleaks + detect-secrets + bandit pre-commit.

### Layer 1 — Data & Persistence
- Postgres (prod), SQLite+aiosqlite (local)
- SQLAlchemy async ORM
- Alembic migrations
- Supabase project memory (optional)
- Ledgers as CSV source of truth for commercial ops:
  - `ledgers/prospects.csv`
  - `ledgers/deals_pipeline.csv`
  - `ledgers/outreach_log.csv`
  - `ledgers/reply_log.csv`

### Layer 2 — LLM Gateway & Routing
- Multi-provider routing: Anthropic Claude (reasoning), Gemini (research), Groq (fast classify), DeepSeek (code), GLM (Arabic-first)
- Automatic fallback chains
- Optional Langfuse tracing
- Per-provider usage tracking and cost governance

### Layer 3 — Agent Runtime
- 15+ production agents, each with defined inputs/outputs, structured logs, graceful degradation, tests
- Agent definitions under `agents/` and `agent_definitions/`
- Secure agent runtime with IAM boundaries

### Layer 4 — Product OS Layer
- The 14 product OSes, each backed by routers, workflows, and prompts
- Productized service catalog with readiness gates
- Each OS owns its own prompts, playbooks, and proof artifacts

### Layer 5 — Delivery & Orchestration
- FastAPI backend (routers across sales, compliance, analytics, agents, webhooks)
- Worker processes (Dockerfile.worker)
- Company Brain worker (Dockerfile.company-brain)
- Watchdog (Dockerfile.watchdog)
- Web (Dockerfile.web, Next.js under `apps/web`)

### Layer 6 — Command & Reporting
- Revenue Command Room dashboard (`reports/command_room/index.html`)
- Daily CEO report (`reports/revenue/YYYY-MM-DD/daily_ceo_report.md`)
- Founder dashboard
- KPI system and operating scorecard

### Layer 7 — Brand & Distribution
- Landing assets under `landing/`
- Arabic-first brand voice (`docs/company/BRAND_VOICE.md`)
- Bilingual AR/EN content
- Design system

---

## 4. Data Flow (Daily Commercial Loop)

```
prospects.csv
   │
   ▼
[Lead Engine] ICP score + dedupe + PDPL-aware enrichment
   │
   ▼
[Outreach Drafting] → outbox/YYYY-MM-DD/*.md  (DRAFT ONLY)
   │
   ▼
[Founder Approval Queue] → approve / reject / rewrite / shorten / make formal / change offer / move to nurture / do not contact
   │  (only if EXTERNAL_SEND_ENABLED + channel flags true)
   ▼
[Manual Send] → outreach_log.csv
   │
   ▼
[Reply Capture] → reply_log.csv
   │
   ▼
[Deals Pipeline] → deals_pipeline.csv
   │
   ▼
[Diagnostic Sprint → Pilot → Subscription]
   │
   ▼
[Client Delivery OS] → baseline → build → test → success report
   │
   ▼
[Executive Proof Pack OS] → documented delta
   │
   ▼
[Company Brain OS] → learnings → next cycle
```

No step in this loop sends anything externally without an explicit human approval and the relevant send flags enabled. The default state of the entire loop is draft generation + human review.

---

## 5. Deployment

### Local
```bash
make setup
cp .env.example .env   # edit secrets
make run               # http://localhost:8000/docs
```

### Full stack
```bash
make docker-up         # app + Postgres + Redis + MongoDB
curl http://localhost:8000/health
```

### Production (Railway)
- `railway.json`, `railway.toml`, `railway.web.toml`, `railway.company-brain.toml`
- `docker-compose.prod.yml`
- `ENVIRONMENT=production`, `DEBUG_MODE=false`
- `MOYASAR_LIVE_MODE=false` until payment cutover approved
- `WHATSAPP_ALLOW_LIVE_SEND=false` until opt-in + legal review complete
- `OUTBOUND_MODE=draft_only` unless Controlled Live Outbound OS is explicitly enabled

### Production gates (review before paid traffic / public demos / enterprise pilots)
1. Launch operator runbook
2. Production readiness checklist
3. Commercial go-live gate
4. Domain operations runbook
5. Frontend production runbook
6. Server hardening checklist
7. Monitoring matrix
8. Incident drill
9. Founder daily operating rhythm
10. Production finalization status

---

## 6. Tech Stack

| Area | Choice |
|---|---|
| Backend | FastAPI, SQLAlchemy async, Pydantic |
| DB | Postgres (prod), SQLite+aiosqlite (local) |
| Migrations | Alembic |
| Cache/Queue | Redis |
| Frontend | Next.js (`apps/web`) + static landing assets |
| LLMs | Anthropic Claude, Gemini, Groq, DeepSeek, GLM (Arabic-first) |
| LLM observability | Langfuse (optional) |
| Payments | Moyasar (SAR, sandbox by default) |
| Invoicing | ZATCA-aware e-invoicing |
| WhatsApp | WhatsApp Business Cloud API (send gated by flags) |
| Email | SMTP (send gated by flags) |
| SMS | provider TBD (send gated by flags) |
| Maps/Leads | Google Places API |
| CI/CD | GitHub Actions |
| Containers | Docker multi-stage, non-root user |
| Security | gitleaks, detect-secrets, bandit, Trivy, pa11y, Lighthouse |
| Secrets | `.env` only, `SecretStr`, pre-commit hooks |
| Timezone | Asia/Riyadh |
| Currency | SAR |

---

## 7. Team Structure (Current + Planned)

### Current (founder-stage)
- Founder / CEO / Operator — runs the daily commercial loop, approvals, delivery, founder decisions.
- AI / Platform (founder-led engineering) — LLM gateway, agents, product OSes, delivery builds.

### Planned hiring triggers (hire only when the trigger fires, not before)
| Role | Trigger | Confidence |
|---|---|---|
| Delivery lead | 2 concurrent paid pilots | High — once 2 pilots are signed, delivery bandwidth becomes the bottleneck. |
| Sales / founder associate | 1 closed subscription after pilot | Medium — a first recurring subscription validates the motion and justifies outreach support. |
| Engineer #2 | 3 concurrent client builds | Medium — 3 concurrent builds exceed single-engineer capacity. |
| Compliance / ops lead | First enterprise pilot or regulator engagement | Medium — enterprise and regulator conversations require a dedicated owner. |
| Customer success | 5 active subscriptions | Medium — retention work starts mattering at 5 accounts. |

Hiring is conservative and trigger-based. No hires are made on forecast alone; the trigger must actually fire.

---

## 8. Revenue Model

### Entry: Company Diagnosis Sprint — SAR 4,999
- 1-week paid diagnostic
- Pain mapping, data audit, baseline, recommendation
- Output: diagnostic report + recommended OS bundle

### Pilot: 1-month Pilot — SAR 14,999
- Build + deploy one product OS for one client function
- Baseline → after → documented delta
- Output: Executive Proof Pack

### Recurring: Monthly Subscription
- Retainer for operating the OS(es) post-pilot
- Scenario forecast (not a guarantee):

| Scenario | Monthly subscription (SAR) | Confidence | Assumptions |
|---|---|---|---|
| Conservative | 7,500 – 12,000 | Medium-high | Single OS, one function, light ongoing ops. |
| Base | 12,000 – 25,000 | Medium | 2–3 OSes bundled, moderate delivery load. |
| Stretch | 25,000 – 60,000 | Low-medium | Multi-OS bundle + controlled live outbound + executive proof packs. |

These are planning scenarios, not price commitments. Actual pricing is set per client via Offer Intelligence OS and confirmed in Proposal + Contract OS.

---

## 9. Operating Model (summary — full detail in STARTUP_OPERATING_MODEL.md)

- Legal entity: Saudi LLC
- Pricing currency: SAR
- Outbound posture: draft-only by default; all send flags off
- Delivery: 4-week pilot cycle (Discovery → Build → Test → Success report)
- Client lifecycle: Prospecting → Diagnosis → Pilot → Subscription → Expansion → Renewal
- Proof: baseline before, after, documented delta — no guaranteed ROI
- Compliance: PDPL-native, ZATCA-aware, approval-first

---

## 10. Growth Strategy (summary — full detail in SAUDI_B2B_MARKET_STRATEGY.md)

### Phase 1 — Diagnosis-led land (current)
- Sell Company Diagnosis Sprint to Saudi SMEs in 8 target sectors.
- Convert diagnostics to pilots. Convert pilots to subscriptions.
- All outreach is draft-only and human-approved.

### Phase 2 — Bundle expansion
- Once a client is subscribed to one OS, expand to 2–3 OSes using the same trust engine.
- Executive Proof Pack becomes the renewal artifact.

### Phase 3 — Controlled live outbound
- Only after opt-in, legal review, and explicit per-environment flag enablement.
- Controlled Live Outbound OS governed by `EXTERNAL_SEND_ENABLED=true` + channel flags.

### Phase 4 — Sector depth + partnership
- Deepen 2–3 verticals (e.g., clinics, real estate).
- Agency partner program for delivery capacity.

### Phase 5 — Platform
- Company Brain OS as the shared memory layer across all client OSes.
- Ecosystem plays (partners, integrations, certification).

All phases are gated by real signals (signed pilots, active subscriptions, compliance readiness), not by calendar dates alone.

---

## 11. Metrics

### North Star
- Monthly recurring revenue (SAR) from active subscriptions.

### Daily KPIs
- Prospects researched
- Outreach drafts generated (not sent)
- Drafts approved
- Drafts manually sent (only if flags on)
- Replies received
- Pipeline updates

### Weekly KPIs
- Diagnostics booked
- Pilots started
- Pilots completed
- Subscriptions signed
- Proof packs delivered

### Monthly KPIs
- MRR (SAR)
- Active subscriptions count
- Net new diagnostics
- Pilot → subscription conversion rate
- Churn
- Gross margin
- Runway (months)

### Trust KPIs (always tracked)
- Approval gates passed without bypass
- Send flags in correct state per environment
- PDPL controls active
- No-overclaim register violations (target: 0)
- Audit trail completeness (target: 100%)

---

## 12. Safety & Compliance Posture

- **No fake clients, testimonials, or ROI.** Every external claim must be backed by a real proof pack with baseline + after + documented delta.
- **All outbound is draft-only by default.** `OUTBOUND_MODE=draft_only`, all send flags false.
- **PDPL-native.** Data subject requests, breach response, retention policy, cross-border transfer addendum.
- **ZATCA-aware.** E-invoicing readiness, Moyasar sandbox by default.
- **Approval-first.** No autonomous external commitments. Humans approve critical external actions.
- **Scenario forecasts, not guarantees.** Every forecast includes confidence level + assumptions.
- **Arabic-first.** Primary positioning, content, and outreach in Arabic; English mirrors for investors and partners.

---

## 13. Related Documents

- `docs/company/DEALIX_COMPANY_OS_AR.md` — الشركة كنظام تشغيل (Arabic)
- `docs/company/DEALIX_COMPANY_OS_EN.md` — Company as an operating system (English)
- `docs/company/FOUNDER_OPERATING_SYSTEM_AR.md` — نظام المؤسس (Arabic)
- `docs/company/STARTUP_OPERATING_MODEL.md` — Operating model detail
- `docs/company/SAUDI_B2B_MARKET_STRATEGY.md` — Saudi B2B market strategy
- `docs/company/DAILY_OPERATING_RHYTHM.md` — Daily / weekly / monthly rhythm
- `docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md` — Platform source of truth
- `docs/ops/CONTROLLED_LIVE_OUTBOUND.md` — Controlled live outbound gates
- `integrations/pdpl.py` — PDPL controls