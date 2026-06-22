# Dealix — Daily Operating Rhythm

> **The daily, weekly, and monthly rhythm that runs the company.**
> Branch: `phase/startup-architecture-brand-os`
> All outbound is draft-only by default (`OUTBOUND_MODE=draft_only`). No autonomous external sends. No fake clients or guaranteed ROI.

---

## 1. Purpose

This document defines the operating cadence of Dealix. It is the executable counterpart to `FOUNDER_OPERATING_SYSTEM_AR.md` and `DEALIX_COMPANY_OS_AR.md`. Every day, week, and month has a defined shape so that the company runs on rhythm, not on reaction.

The rhythm is built around the 14 product OSes and the ledgers that are the source of truth for commercial operations.

---

## 2. Daily Rhythm

### 2.1 Morning Review — Command Room (08:30 – 09:00)

| Time | Action | Tool | Output |
|---|---|---|---|
| 08:30 | Run `make company-day` | Revenue Command Room OS | Daily batch triggered |
| 08:35 | Review `reports/command_room/index.html` | Revenue Command Room OS | Pipeline snapshot, KPIs |
| 08:36 | Review `ledgers/prospects.csv` (new entries) | Revenue Command Room OS | New prospects acknowledged |
| 08:40 | Review drafts in `outbox/YYYY-MM-DD/` | Email Outreach Review OS / WhatsApp Follow-up OS / SMS OS | Draft queue ready for review |
| 08:45 | Review founder approval queue | Founder Decision Desk | Today's decisions listed |
| 08:50 | Review market & competitor signals | Market & Competitor Watch OS | Critical signals flagged |

**Morning KPIs (checked):**
- Prospects researched (yesterday's batch)
- Drafts generated (yesterday's batch)
- Open replies awaiting triage
- Pipeline changes overnight

### 2.2 Target Research (09:00 – 10:00)

| Time | Action | Tool | Output |
|---|---|---|---|
| 09:00 | Research new targets in priority sector of the day | Revenue Command Room OS + Google Places API | New prospects in `ledgers/prospects.csv` |
| 09:30 | ICP scoring + dedupe + PDPL-aware enrichment | Revenue Command Room OS | Scored prospects |
| 09:45 | Segment prospects into outreach batches | Revenue Command Room OS | Batched draft requests |

**KPIs for this block:**
- New prospects researched (target: 20–40/day, scenario-dependent)
- ICP match rate (tracked, not guaranteed)
- Duplicate suppression rate

### 2.3 Outreach Drafting (10:00 – 11:00)

| Time | Action | Tool | Output |
|---|---|---|---|
| 10:00 | Generate outreach drafts (email/WhatsApp/SMS) | Email Outreach Review OS / WhatsApp Follow-up OS / SMS OS | Drafts in `outbox/YYYY-MM-DD/` |
| 10:30 | Review and edit drafts (approve / reject / rewrite / shorten / make formal / change offer / move to nurture / do not contact) | Founder Decision Desk | Decisioned drafts |
| 10:45 | Queue approved drafts for manual send (only if flags enabled) | Founder Decision Desk | Send-ready queue |

**KPIs for this block:**
- Drafts generated
- Drafts approved
- Drafts rejected/rewritten (quality signal)
- Send-ready count (only if `EXTERNAL_SEND_ENABLED=true` + channel flags)

**Default state:** `OUTBOUND_MODE=draft_only`. No draft is sent without explicit founder approval and the relevant send flags enabled.

### 2.4 Follow-up Tracking (11:00 – 12:00)

| Time | Action | Tool | Output |
|---|---|---|---|
| 11:00 | Triage replies in `ledgers/reply_log.csv` | WhatsApp/Inbox Follow-up OS | Classified replies |
| 11:15 | Draft follow-up responses (approval-gated) | WhatsApp/Inbox Follow-up OS | Follow-up drafts |
| 11:30 | Update `ledgers/deals_pipeline.csv` with new stages | Revenue Command Room OS | Updated pipeline |
| 11:45 | Flag hot opportunities for diagnosis outreach | Founder Decision Desk | Hot list |

**KPIs for this block:**
- Replies received
- Reply-to-meeting conversion (tracked)
- Pipeline stage movements
- Hot opportunities flagged

### 2.5 Afternoon Delivery (13:00 – 16:00)

| Time | Action | Tool | Output |
|---|---|---|---|
| 13:00 | Client delivery work (Discovery / Build / Test) | Client Delivery OS | Delivery progress |
| 14:00 | Build/deploy OS for active pilot clients | Client Delivery OS + agents | Deployed OS updates |
| 14:30 | Review proof packs in progress | Executive Proof Pack OS | Proof pack status |
| 15:00 | Record learnings into Company Brain OS | Company Brain OS | Updated memory |
| 15:30 | Trust & compliance check (approval gates, send flags, audit trail) | AI Trust & Compliance OS | Compliance status |

**KPIs for this block:**
- Active pilots progress (on-track / at-risk)
- Proof packs in progress
- Approval gates bypassed (target: 0)
- Send flags correct per environment (target: all correct)
- Audit trail completeness (target: 100%)

### 2.6 Evening Report (16:30 – 17:00)

| Time | Action | Tool | Output |
|---|---|---|---|
| 16:30 | Review `reports/revenue/YYYY-MM-DD/daily_ceo_report.md` | Revenue Command Room OS | CEO report reviewed |
| 16:40 | Update tomorrow's decision queue | Founder Decision Desk | Tomorrow's queue |
| 16:50 | Record final decisions into Company Brain OS | Company Brain OS | Decision log updated |

**Evening KPIs (recorded):**
- Prospects researched today
- Drafts generated / approved / send-ready
- Drafts manually sent (only if flags on)
- Replies received and triaged
- Pipeline movements
- Delivery progress
- Compliance status
- Decisions logged

---

## 3. Weekly Rhythm

### Sunday — Weekly Review & Planning
- Review all weekly KPIs (diagnostics booked, pilots started, pilots completed, subscriptions signed, proof packs delivered).
- Full pipeline review in `ledgers/deals_pipeline.csv`.
- Set top 3 priorities for the week.
- Update Company Brain OS with weekly learnings.

### Monday — Sector Research Day
- Deep research on one priority sector.
- Update `data/outreach/saudi_icp_segments.json`.
- Review competitor signals for that sector via Market & Competitor Watch OS.
- Draft sector-specific offer updates via Offer Intelligence OS.

### Tuesday — Delivery & Client Day
- Review every active client's status (Discovery / Build / Test / Report).
- Confirm every pilot client has a clear baseline.
- Identify clients approaching success report.

### Wednesday — Offers & Pricing Day
- Review offer ladder.
- Update pricing engine based on market signals.
- Review proposals in progress via Proposal + Contract OS.

### Thursday — Trust & Compliance Day
- Review no-overclaim register (target: 0 violations).
- Verify send flags per environment.
- Review audit trail completeness.
- Write a short weekly summary into Company Brain OS.

### Friday — Rest (no commercial operations)
### Saturday — Next-week Planning (1 hour only)
- Read the weekly summary.
- Set 3 priorities for next week.
- No sends.

### Weekly KPIs
- Diagnostics booked
- Pilots started
- Pilots completed
- Subscriptions signed
- Proof packs delivered
- No-overclaim violations (target: 0)
- Send flag correctness (target: 100%)
- Audit trail completeness (target: 100%)

---

## 4. Monthly Rhythm

### Last working day of the month — Monthly Review
- Review MRR (SAR).
- Review active subscriptions count.
- Compute pilot → subscription conversion rate.
- Compute churn.
- Compute gross margin.
- Compute runway (months).
- Review hiring triggers: did any fire?
- Write monthly executive narrative.

### First working day of the month — Monthly Planning
- Set monthly revenue target (scenario + confidence + assumptions).
- Set target diagnostics count.
- Set target pilots count.
- Update offer pack for priority sectors.
- Review `SAUDI_B2B_MARKET_STRATEGY.md` and adjust sector priorities if needed.

### Mid-month — Correction Check
- Compare actual progress vs plan.
- If deviation > 20%, review causes and adjust plan.
- Review stalled pipeline opportunities.

### Monthly KPIs
- MRR (SAR)
- Active subscriptions
- Net new diagnostics
- Pilot → subscription conversion rate
- Churn
- Gross margin
- Runway (months)
- Hiring triggers fired (and actions taken)

---

## 5. KPI Summary by Period

| Period | KPIs |
|---|---|
| Daily | Prospects researched, drafts generated, drafts approved, drafts sent (if flags on), replies received, pipeline movements, delivery progress, compliance status, decisions logged. |
| Weekly | Diagnostics booked, pilots started, pilots completed, subscriptions signed, proof packs delivered, no-overclaim violations, send flag correctness, audit trail completeness. |
| Monthly | MRR, active subscriptions, net new diagnostics, pilot→sub conversion, churn, gross margin, runway, hiring triggers fired. |

### Trust KPIs (tracked every period)
- Approval gates bypassed (target: 0)
- Send flags correct per environment (target: 100%)
- PDPL controls active (target: yes)
- No-overclaim register violations (target: 0)
- Audit trail completeness (target: 100%)

---

## 6. Outbound Safety Rules (always on)

- `OUTBOUND_MODE=draft_only` is the default for every environment.
- `EXTERNAL_SEND_ENABLED=false`, `EMAIL_SEND_ENABLED=false`, `WHATSAPP_SEND_ENABLED=false`, `WHATSAPP_ALLOW_LIVE_SEND=false`, `SMS_SEND_ENABLED=false` by default.
- No draft is sent without explicit founder approval.
- No live WhatsApp send without opt-in + legal review + per-environment flag.
- No guaranteed ROI, no fake clients, no fake testimonials.
- Every external claim is backed by a real proof pack (baseline → after → documented delta).

---

## 7. Source Files & Outputs

### Ledgers (source of truth)
- `ledgers/prospects.csv` — prospects
- `ledgers/deals_pipeline.csv` — pipeline
- `ledgers/outreach_log.csv` — sends
- `ledgers/reply_log.csv` — replies

### Daily outputs
- `outbox/YYYY-MM-DD/*.md` — outreach drafts
- `reports/revenue/YYYY-MM-DD/daily_ceo_report.md` — CEO report
- `reports/command_room/index.html` — command dashboard

### Scripts
- `scripts/revenue/run_daily_revenue_machine.py` — daily commercial machine
- `scripts/dealix_daily_operator.py` — daily operator (demo/production)

---

## 8. Related Documents

- `DEALIX_STARTUP_ARCHITECTURE.md` — full system architecture
- `DEALIX_COMPANY_OS_AR.md` / `DEALIX_COMPANY_OS_EN.md` — company as an OS
- `FOUNDER_OPERATING_SYSTEM_AR.md` — founder operating system (Arabic)
- `STARTUP_OPERATING_MODEL.md` — operating model, pricing, runway
- `SAUDI_B2B_MARKET_STRATEGY.md` — Saudi B2B market strategy
- `docs/ops/CONTROLLED_LIVE_OUTBOUND.md` — controlled live outbound gates