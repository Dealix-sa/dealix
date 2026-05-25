# Ultimate Founder Console

> The single internal interface the founder uses to operate the entire Dealix company.
> One URL, one menu, one top action per page, one decision per click.

---

## 1. Purpose

Operate the entire Dealix company from one internal interface.

The console is the **only** interface the founder needs during the working day. If a question can be answered, or a decision can be made, anywhere else (in an email, a spreadsheet, a third-party tool), it is a bug in the console — not a workflow.

Design principle: **Every page must tell Sami what to do next.**

---

## 2. Top-level layout

```
┌──────────────────────────────────────────────────────────────────┐
│ Dealix  ·  CEO  ·  Sales  ·  Approvals  ·  Workers  ·  Trust    │
│         ·  Finance  ·  Distribution  ·  Delivery  ·  Retention  │
│         ·  Proof  ·  Experiments  ·  Partners  ·  Product       │
│         ·  Security  ·  Evals  ·  Audit  ·  Settings            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Top action banner]   →   one sentence, one button              │
│                                                                  │
│  [Page content]        →   data + decisions, nothing else        │
│                                                                  │
│  [Source freshness]    →   "data as of HH:MM, source: X"         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Every page renders three blocks in this order, no exceptions: **top action → content → freshness**.

---

## 3. Pages

### 3.1 `/ceo`
**Goal:** the founder opens this page first thing in the morning and knows what matters today.

Components:
- **Top Action** — one sentence: e.g., "Approve 7 outreach drafts for AlRajhi sector."
- **Company Score** — one number 0–100 with the worst sub-score highlighted.
- **Bottleneck** — the single layer holding the company back this week.
- **Risk** — the single highest-severity flag from the Trust Center.
- **Cash** — collected this month + projected next 30 days.

Data sources:
- `GET /api/v1/internal/ceo/summary`
- `GET /api/v1/internal/ceo/top-action`
- `GET /api/v1/internal/ceo/company-score`

---

### 3.2 `/sales-cockpit`
**Goal:** see the revenue funnel from leads to payment in one screen.

Components:
- Funnel chart: `Lead Intelligence → Outreach → Sent → Replies → Samples → Proposals → Payment`.
- Bottleneck callout: where conversion is worst this week.
- Payment-capture queue: every proposal awaiting payment, with days-since-sent.
- One-click drill into any stage.

Data sources:
- `GET /api/v1/internal/sales/funnel`
- `GET /api/v1/internal/sales/bottleneck`
- `GET /api/v1/internal/sales/payment-capture`

---

### 3.3 `/approvals`
**Goal:** every pending decision in one queue, sorted by urgency × class.

Components:
- Queue table: `id`, `class (A1/A2/A3)`, `summary`, `policy_result`, `evidence`, `age`.
- Quick actions per row: **Approve · Reject · Request edit · Escalate**.
- Bulk action only for A1.
- Each click writes to `approval_decisions` and `audit_events`.

Data sources:
- `GET /api/v1/internal/approvals`
- `POST /api/v1/internal/approvals/{id}/approve`
- `POST /api/v1/internal/approvals/{id}/reject`
- `POST /api/v1/internal/approvals/{id}/request-edit`
- `POST /api/v1/internal/approvals/{id}/escalate`

---

### 3.4 `/workers`
**Goal:** know which background machines are running, failing, or stale — and fix them without a deploy.

Components:
- Worker table: `worker_id`, `owner`, `schedule`, `last_run`, `status`, `failures_24h`, `backlog`.
- Filters: failing, stale, disabled.
- Per-row actions: **Retry · Disable · Open logs**.
- Page-wide health score.

Data sources:
- `GET /api/v1/internal/workers/health`
- `GET /api/v1/internal/workers/failures`
- `POST /api/v1/internal/workers/{id}/retry`

---

### 3.5 `/trust`
**Goal:** see all policy flags, suppression updates, AI risks, and incidents — and decide what to do.

Components:
- Active flags table: `kind`, `subject`, `severity`, `opened`, `owner`.
- Suppression list browser (read-only on this page; edits go through Settings).
- AI risk panel: eval pass rate, last red-team result, prompt-injection failures (24h).
- Incident timeline.

Data sources:
- `GET /api/v1/internal/trust/flags`
- `POST /api/v1/internal/trust/evaluate` (used by other pages, exposed here for manual checks)
- `GET /api/v1/internal/trust/incidents`

---

### 3.6 `/finance`
**Goal:** know the financial position of the company in one screen.

Components:
- Cash collected (this month, last month, projection next 30 days).
- MRR + change (% week-over-week).
- Pipeline + weighted pipeline.
- Gross margin + AI/tool cost.
- Runway in months.

Data sources:
- `GET /api/v1/internal/finance/summary`
- `GET /api/v1/internal/finance/unit-economics`
- `GET /api/v1/internal/finance/runway`

---

### 3.7 `/distribution`
**Goal:** decide which channel to scale, which to pause, and which experiment to run.

Components:
- Channel table: `channel`, `cost`, `volume`, `reply_rate`, `conversion`, `cash`.
- Sector heatmap.
- Active campaigns + status.
- Experiments link → `/experiments`.

Data sources:
- (reuses) `GET /api/v1/internal/sales/funnel` filtered by channel.

---

### 3.8 `/delivery`
**Goal:** every paid engagement in flight, with its delivery state and next QA milestone.

Components:
- Delivery queue: `client`, `start_date`, `delivery_stage`, `qa_status`, `next_milestone`.
- Per-row actions: **Start · QA · Handoff · Mark blocked**.
- Workspace deep link to `clients/<handle>/`.

Data sources:
- `GET /api/v1/internal/delivery/queue`
- `POST /api/v1/internal/delivery/{client}/start`
- `POST /api/v1/internal/delivery/{client}/qa`

---

### 3.9 `/retention`
**Goal:** keep paying customers paying.

Components:
- Health score table per client (green / amber / red).
- Renewal calendar (next 90 days).
- Retainer asks queued.
- Referral asks queued.

---

### 3.10 `/proof`
**Goal:** see, approve, and publish proof assets.

Components:
- Proof library: case studies, testimonials, sample reports.
- Pending proof approvals from clients.
- Publish controls (with trust gate).

---

### 3.11 `/experiments`
**Goal:** track A/B tests with one decision rule per experiment.

Components:
- Experiment table: `hypothesis`, `metric`, `delta`, `confidence`, `decision`.
- New-experiment button (founder-only, gated to one active per channel).

---

### 3.12 `/partners`
**Goal:** see partner-sourced revenue and what to do next with each partner.

Components:
- Partner table: `partner`, `referrals`, `pipeline`, `cash`, `last_touch`.
- Co-sell pipeline.

---

### 3.13 `/product`
**Goal:** decide which repeated workflow to productize next.

Components:
- Feature usage table.
- Repeated workflow detector: workflows used by ≥2 paid customers.
- Productization queue.

Data sources:
- `GET /api/v1/internal/product/usage`
- `GET /api/v1/internal/product/repeated-workflows`

---

### 3.14 `/security`
**Goal:** see the security posture of the company in one place.

Components:
- Secrets scan status (last 24h).
- Dependency review status.
- Access control: who has access to what.
- Supply chain summary.

---

### 3.15 `/evals`
**Goal:** see if our AI is producing safe, on-spec, useful output.

Components:
- Eval pass rate by suite (prompt-injection, refusal, overclaim, regression).
- Last red-team result.
- Per-prompt-template quality score.
- Failing examples for triage.

---

### 3.16 `/audit`
**Goal:** prove what happened. Every approval, every policy result, every external action.

Components:
- Decisions log: `time`, `actor`, `action`, `class`, `decision`, `payload_digest`.
- Filters: by class, by actor, by date.
- Export to CSV (for legal / customer audits).

Data sources:
- `GET /api/v1/internal/audit/approvals`
- `GET /api/v1/internal/audit/actions`

---

### 3.17 `/settings`
**Goal:** change the things the founder is allowed to change without a deploy.

Components:
- Suppression list editor (writes audit).
- Approval-class overrides per worker (with required justification).
- Branding (logo, signature lines for outbound).
- Feature flags.

---

## 4. Cross-page contracts

### 4.1 Top-action contract
Every page exposes a `top_action` object:
```json
{
  "summary": "Approve 7 outreach drafts for AlRajhi sector",
  "url": "/approvals?filter=alrajhi",
  "severity": "amber",
  "computed_at": "2026-05-23T07:12:00+03:00"
}
```
The `/ceo` page surfaces the highest-severity `top_action` from any page.

### 4.2 Freshness contract
Every component that reads data shows:
- The time the data was computed.
- The source (Postgres / private ops / live API).
- A warning if older than the page's freshness budget (default 24h).

### 4.3 Decision contract
Every button that has external impact:
- Renders a confirmation modal with the policy result.
- Writes to `audit_events` on click.
- Disables itself if the trust gate rejects.

### 4.4 Access contract
- Founder role: full access.
- Trusted operator role: read-only on `/audit`, `/finance`, `/evals`, `/security`.
- All other roles: explicit denial (no implicit access).

---

## 5. Empty states

Empty states are a feature, not an error. Each page renders an empty state that **tells the founder what to do** when there is no data:

| Page          | Empty state copy                                                                    |
|---------------|-------------------------------------------------------------------------------------|
| `/ceo`        | "No data yet. Run `make v5-status` and reload."                                     |
| `/sales-cockpit` | "Funnel is empty. Open `/approvals` to seed the first outreach batch."           |
| `/approvals`  | "Nothing to approve. Run lead-discovery worker."                                    |
| `/workers`    | "No workers reporting yet. Check Worker Mesh setup."                                |
| `/trust`      | "No flags. Trust posture clean."                                                    |
| `/finance`    | "No finance events yet. Connect Stripe / private ops."                              |
| `/delivery`   | "No deliveries in flight. First paid engagement seeds this page."                   |
| `/proof`      | "No proof assets yet. Ship the first delivery to seed this."                        |
| `/audit`      | "No decisions logged. The first founder approval seeds this page."                  |

---

## 6. Build status

- v5 in flight on this branch (`founder-console-v5`).
- Live runtime data: pending L3 (see `docs/company/DEALIX_MATURITY_MODEL.md`).
- Trust-gated buttons: pending L4.

---

## 7. Rule

> **The console must tell Sami what to do next.**

If a page renders but does not tell the founder what to do next, the page is incomplete — even if all its components render correctly.
