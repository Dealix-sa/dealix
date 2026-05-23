# Ultimate Observability & DORA

> Measure engineering, runtime, revenue, trust, and AI performance.
> The company improves only what it measures.

---

## 1. Purpose

Give Dealix a **single observability surface** that combines:
- **Runtime metrics** (is the system up and healthy?)
- **Revenue metrics** (is the factory producing?)
- **Trust metrics** (are we safe?)
- **Engineering metrics** (are we shipping well? — DORA)
- **AI metrics** (are our models on-spec and economical?)

These metrics feed `/ceo`, `/sales-cockpit`, `/trust`, `/workers`, `/finance`, `/evals`, and the weekly scorecard. Every metric has an owner, a definition, and a target.

---

## 2. Runtime metrics

These metrics tell us whether the **machine** is healthy.

| Metric                  | Definition                                                         | Target            | Owner   |
|--------------------------|--------------------------------------------------------------------|--------------------|---------|
| API uptime               | Percentage of 1-minute intervals where `/healthz` returned 200.    | ≥ 99.9% rolling 30d| Runtime |
| Worker success rate      | Successful runs / total runs (24h).                                | ≥ 99% per worker   | Runtime |
| Queue latency p95        | Time from enqueue to start of run.                                 | ≤ 60s              | Runtime |
| Failed jobs (24h)        | Count of `worker_runs.status='failed'` in 24h.                     | ≤ 5 across mesh    | Runtime |
| Stale reports            | Reports older than their freshness budget.                         | 0                  | Data    |
| Approval latency p95     | Time from approval queued to approved/rejected.                    | ≤ 4h working hours | Founder |
| External action blocks   | Count of attempted external actions denied by trust plane (24h).   | < 10 (alert ≥ 20)  | Trust   |

These metrics appear on `/workers` and feed the company score.

---

## 3. Revenue metrics

These metrics tell us whether the **factory** is producing.

| Metric                    | Definition                                                    | Target (weekly)         | Owner    |
|----------------------------|---------------------------------------------------------------|--------------------------|----------|
| Leads discovered           | New rows in `lead_intelligence` this week.                    | ≥ 100                    | Revenue  |
| Leads approved             | Approved outreach in the Approval Center.                     | ≥ 25                     | Revenue  |
| Sent outreach              | Outreach with `state='sent'`.                                 | ≥ 25                     | Revenue  |
| Replies                    | Any inbound message classified.                               | ≥ 5                      | Revenue  |
| Positive replies           | `classification='positive'`.                                  | ≥ 2                      | Revenue  |
| Samples produced           | `sample_queue.state='delivered'`.                             | 3                        | Revenue  |
| Proposals sent             | `proposal_queue.state='sent'`.                                | 1–3                      | Revenue  |
| Payment follow-ups due     | Open `payment_capture_queue` past due date.                   | 0                        | Finance  |
| Cash collected             | `finance_events.kind='payment'` sum.                          | Trends ↑ month-over-month| Founder  |

These metrics appear on `/sales-cockpit`, `/finance`, and the weekly scorecard.

---

## 4. Trust metrics

These metrics tell us whether we are **safe**.

| Metric                    | Definition                                                    | Target           | Owner |
|----------------------------|---------------------------------------------------------------|-------------------|-------|
| Suppression violations     | Send attempts blocked by suppression list (24h).              | 0 (alert ≥ 1)     | Trust |
| Overclaim violations       | `no_overclaim` check failures (24h).                          | 0 (alert ≥ 1)     | Trust |
| A3 attempts                | Actions classified as A3 (any) (24h).                         | Logged; reviewed  | Trust |
| Prompt injection failures  | `prompt_injection` suite failures on latest run.              | 0                 | Trust |
| Eval pass rate per suite   | Pass rate per AI eval suite.                                  | ≥ 98% regression, 100% safety | Trust |
| Incidents (open)           | `incidents.closed_at IS NULL`.                                | 0 sev1; ≤ 2 sev2  | Trust |

These metrics appear on `/trust`, `/evals`, and the weekly scorecard. Any sev1 incident triggers a top-action banner on `/ceo` until closed.

---

## 5. Engineering metrics (DORA)

DORA defines four "throughput + stability" metrics; we add a fifth ("rework") to capture quality drift. Each is computed daily by the `dora-collector` worker.

### 5.1 Change Lead Time
- Definition: time from first commit on a branch to that change running in production.
- Source: GitHub PRs + deploy events.
- Target band:
  - Elite: < 1 hour
  - High: 1 day – 1 week
  - Dealix L2 → L5 target: **≤ 1 day median.**

### 5.2 Deployment Frequency
- Definition: deploys to production per day.
- Source: deploy events.
- Target band:
  - Elite: multiple per day
  - High: between once per day and once per week
  - Dealix L2 → L5 target: **≥ 1/day on active weeks.**

### 5.3 Change Fail Rate (CFR)
- Definition: percentage of deploys that lead to a rollback or hotfix.
- Source: deploy events + incident links.
- Target: **≤ 15%.**

### 5.4 Failed Deployment Recovery Time (MTTR for deploys)
- Definition: time from failed deploy detected to restoration.
- Source: deploy events + restore events.
- Target: **≤ 1 hour median.**

### 5.5 Deployment Rework Rate (added)
- Definition: percentage of deploys followed by a corrective change within 7 days.
- Source: deploy events + commit subjects (`fix:`, `revert:`).
- Target: **≤ 10%.**

These metrics appear in `/security` and the weekly scorecard. They are **trends**, not pass/fail gates per deploy.

---

## 6. AI metrics

These metrics tell us whether our **models** are doing useful, safe, economical work.

| Metric                          | Definition                                                         | Target                |
|----------------------------------|--------------------------------------------------------------------|------------------------|
| Eval pass rate per suite         | (See §4.)                                                          | ≥ 98% regression       |
| AI cost SAR / proposal           | `ai_cost` events attributable / proposals sent.                    | ≤ 20 SAR (revisit each quarter) |
| AI cost SAR / qualified lead     | `ai_cost` for research + scoring / qualified leads.                | ≤ 5 SAR                |
| Tool call rejection rate         | Tool calls denied by trust / total tool calls.                     | < 5%                   |
| Prompt template coverage         | % of prompt templates with at least one regression test.           | 100%                   |
| Red-team finding burndown        | Open findings from the last quarterly red-team.                    | 0 sev1; ≤ 3 sev2       |

These metrics appear on `/evals`.

---

## 7. Where the metrics live

- **Source data:** Postgres tables (Phase 2+) or CSV (Phase 1).
- **Computation:** the metrics layer in `dealix/metrics/` (Phase 4 introduces materialized views).
- **Dashboards:** the Founder Console pages listed in `docs/frontend/ULTIMATE_FOUNDER_CONSOLE.md`.
- **Daily digest:** `morning-digest` worker emails the founder a one-page bilingual summary.
- **Weekly scorecard:** `weekly-scorecard` worker assembles the bilingual Monday digest.

---

## 8. SLOs (Service Level Objectives)

Targets above become **SLOs** when:
- They are measured continuously.
- A miss triggers an investigation.
- A trend toward a miss triggers a top-action banner.

Each SLO has:
- A **window** (24h, 7d, 30d).
- A **threshold** (the target).
- An **owner** (who responds when the SLO burns).

SLOs live in `dealix/observability/slos.yaml`.

---

## 9. Alerting

| Alert                                     | Severity | Surface                                                |
|-------------------------------------------|----------|--------------------------------------------------------|
| API uptime < 99% over 1h                  | Sev1     | Founder + on-call.                                     |
| Any worker auto-disabled (§5 failures)    | Sev2     | `/ceo` banner + Worker Health page.                    |
| Suppression violation                     | Sev1     | Founder + Trust Center incident.                       |
| Prompt-injection regression fail          | Sev2     | `/evals` page + block A2/A3 using affected template.   |
| Cash collected = 0 for 7 consecutive days | Sev2     | `/finance` flag + weekly scorecard.                    |
| Backups not restored in a quarter         | Sev3     | `/security` page + monthly review.                     |

---

## 10. Why DORA matters for Dealix

DORA's research shows that **speed and stability move together**: high-performing teams ship more often **and** break things less often. For Dealix, this matters because:
- The factory's throughput depends on engineering ship rate.
- The trust plane's correctness depends on safe deploys.
- The customer's experience depends on low MTTR.

We use DORA not as a vanity metric, but as a **leading indicator**: when our four (+ one) metrics degrade, the company's ability to deliver degrades — even if the dashboards still look green.

---

## 11. Rule

> **The company improves only what it measures.**

If a behaviour matters, it has a metric. If it has a metric, the metric has an owner. If the metric has an owner, the owner sees it weekly. Without all three, the behaviour drifts.
