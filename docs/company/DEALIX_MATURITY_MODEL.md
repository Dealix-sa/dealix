# Dealix Maturity Model

> Where are we, what comes next, and what counts as "done" at each level.
> Read alongside `DEALIX_AUTONOMOUS_ENTERPRISE_OS.md`.

This model exists because the biggest failure mode for Dealix is **jumping levels**: building an autonomous agent at L10 before the company has cash at L5. The model below makes that failure visible and prevents it.

---

## Levels at a glance

| Level | Name                  | One-line definition                                                            |
|-------|-----------------------|--------------------------------------------------------------------------------|
| L0    | Repository System     | Docs, scripts, workflows, frontend, backend exist in the repo.                 |
| L1    | Buildable Product     | Frontend builds, backend starts, tests pass, CI is green.                      |
| L2    | Founder Console       | CEO sees status, approvals, funnel, workers, trust, finance in one place.      |
| L3    | Live Runtime          | The Console reads real data from private ops / database — not mocks.           |
| L4    | Trust-Gated Actions   | Every approval writes audit and passes the policy evaluator.                   |
| L5    | Revenue Factory       | The system moves leads → replies → samples → proposals → payment follow-ups.   |
| L6    | Client Delivery OS    | Payment/PO triggers delivery, QA, handoff, feedback, retention.                |
| L7    | Data Platform         | Postgres is the source of truth; CSV becomes export only.                      |
| L8    | Worker Mesh           | Durable workflows with retries, monitoring, alerts, and a disable switch.      |
| L9    | Productized Platform  | Customer portal, partner portal, integrations, billing, API, RBAC.             |
| L10   | Autonomous Enterprise | Daily company operations run with founder approval only on high-impact moves.  |

---

## Per-level exit criteria

A level is **only "exited"** when **every** item below is true. No partial credit.

### L0 — Repository System
- Repo exists with `docs/`, `scripts/`, `frontend/`, `api/`, `dealix/`.
- README explains how to install and run.
- The Ultimate blueprint exists (`make ultimate-level` passes).
- Owner: Founder.

### L1 — Buildable Product
- `make install-dev` succeeds on a clean checkout.
- `make test` is green.
- `make lint` and `make type-check` are green.
- Frontend builds without errors.
- API starts and `/healthz` returns 200.
- CI on `main` is green.
- Owner: Engineering.

### L2 — Founder Console
- `/ceo`, `/sales-cockpit`, `/approvals`, `/workers`, `/trust`, `/finance` pages render.
- Each page shows at least one real (or seeded) data point.
- The console tells the founder **one** top action.
- The console is reachable from a single deployed URL.
- Owner: Founder Console maintainer.

### L3 — Live Runtime
- Console reads from the live database or private ops snapshot — no mocks.
- Source freshness indicator is visible per page.
- Stale-data warning is wired (>24h triggers a flag).
- One data-source path is wired end-to-end (e.g., `leads → outreach_queue → approvals`).
- Owner: Data Platform.

### L4 — Trust-Gated Actions
- Every approval button writes a record to `approval_decisions`.
- Every external action passes `POST /api/v1/internal/trust/evaluate` first.
- Suppression list is consulted before send.
- No-overclaim policy is enforced.
- `audit_events` table receives ≥1 record per approval.
- Owner: Trust & Governance.

### L5 — Revenue Factory
- ≥100 lead-intelligence records per week.
- ≥25 approved outreach actions per week.
- ≥5 replies per week routed back to the cockpit.
- ≥3 samples produced per week.
- ≥1 proposal sent per week.
- Payment follow-up exists for every proposal.
- Owner: Revenue Ops.

### L6 — Client Delivery OS
- First paid client has a workspace under `clients/<handle>/`.
- `intake.md`, `delivery_plan.md`, `qa_checklist.md`, `delivery_report.md`, `handoff.md`, `feedback.md` exist.
- A QA pass/fail decision is recorded before handoff.
- Health score is computed at handoff and reviewed monthly.
- Retainer or referral ask is queued.
- Owner: Delivery.

### L7 — Data Platform
- Postgres is the primary store; CSV is a periodic export only.
- Core tables exist with migrations (`accounts`, `contacts`, `signals`, `lead_intelligence`, `outreach_queue`, `approval_queue`, `approval_decisions`, `conversation_log`, `sample_queue`, `proposal_queue`, `payment_capture_queue`, `delivery_queue`, `retention_queue`, `proof_library`, `worker_runs`, `audit_events`, `ai_eval_results`, `finance_events`, `product_usage`, `incidents`).
- Event log table receives append-only records for every external-impact action.
- Backups run daily and have been restored at least once successfully.
- Owner: Data Platform.

### L8 — Worker Mesh
- Redis/RQ (or equivalent) queue runs in production.
- Every worker has `worker_id`, `owner`, `schedule`, `retry_policy`, `disable_switch`.
- Worker health page shows last 24h success rate and failure count.
- A failing worker can be retried or disabled from the console without a deploy.
- Alerts fire on stale workers (>1h past schedule) and on backlog > N.
- Owner: Runtime.

### L9 — Productized Platform
- Customer portal exists with role-based access.
- Partner portal exists.
- Billing integration handles invoices + payment capture.
- Public API surface is documented (`docs/api/ULTIMATE_INTERNAL_API.md` has a "public" counterpart).
- Repeated workflows ≥3 have been promoted to product modules.
- Owner: Product.

### L10 — Autonomous Enterprise
- All Revenue Factory workers run autonomously under A0/A1.
- A2/A3 actions are queued for founder approval only.
- The company's daily operating rhythm (digests, scorecards, approvals) runs on autopilot.
- 14+ consecutive days of clean operation with no rollback.
- Owner: Founder + system.

---

## Scale rule (the only rule that matters here)

> **Do not move to the next level until the current level has:**
> 1. **verification** — a script or CI check that proves the level is intact;
> 2. **operating evidence** — at least 14 days of real activity at that level;
> 3. **trust gate** — every external-impact action passes the trust plane;
> 4. **rollback path** — a documented, tested way to disable the level;
> 5. **owner** — a single person accountable for the level's health.

If any of the five is missing, the level is **not exited**, no matter what the dashboard says.

---

## Where we are today (canonical position)

- L0: ✅ achieved.
- L1: ✅ achieved (CI green on `main`).
- L2: 🚧 in progress (Founder Console v5 in flight).
- L3: 🚧 partial (live API trust probes exist; live runtime not yet end-to-end).
- L4: 🚧 partial (audit infrastructure exists; not every approval writes audit).
- L5: ⏳ pre-evidence (no sustained weekly revenue cadence yet).
- L6 – L10: not started — and will not start until L5 has 14 days of evidence.

This position is updated in the project status digest and re-verified by `make ultimate-level` + `make v5-status`.

---

## What this model **prevents**

- "Let's build the customer portal first." — No. That is L9. We are at L2.
- "Let's add an autonomous agent that sends emails." — No. That is L10 autonomy on top of an L5 factory that doesn't exist yet.
- "Let's migrate to Postgres now." — Only if L7 is the actual blocker; otherwise CSV stays.
- "Let's ship a SaaS module." — Only after the workflow has been used by a paid customer (L6) **and** repeated (L9 gate).

Use this document to say **no** to the work you are not yet ready to do.
