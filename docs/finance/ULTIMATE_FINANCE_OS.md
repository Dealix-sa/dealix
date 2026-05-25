# Ultimate Finance OS

> Make Dealix financially controlled from day one.
> Cash is the scoreboard. Margin is the protection. Retention is the compounder.

---

## 1. Purpose

Give the founder a **single financial truth** for the company, computed daily, visible on `/finance`, and connected to every decision: pricing, scope, channel, hiring, tooling.

The Finance OS is not an accounting system (the bookkeeper's accounting system is). The Finance OS is the **operating finance** view: cash in the bank, MRR, pipeline, margin, AI/tool unit economics, and runway — updated in hours, not months.

---

## 2. Core metrics

Every metric below has a single named source query in the metrics layer (Phase 4) and is surfaced on `/finance`.

### 2.1 Cash collected
- Definition: SAR received into Dealix accounts in a given period.
- Sources: `finance_events` (kind=`payment`).
- Granularity: day, week, month, MTD, YTD.

### 2.2 MRR (Monthly Recurring Revenue)
- Definition: sum of active monthly contracts (Managed Ops + retainers).
- Sources: active rows in `proposal_queue` with recurring offers + `finance_events` recurring payments.
- Excludes: one-time sprints, data packs, custom AI projects (those count toward cash, not MRR).

### 2.3 Pipeline
- Definition: sum of `amount_sar` for proposals in `state ∈ {draft, sent}`.
- Granularity: by sector, by channel, by offer.

### 2.4 Weighted pipeline
- Definition: pipeline × stage probability.
- Stage probabilities (defaults, override per offer in `dealix/finance/stage_probs.yaml`):
  - draft: 10%
  - sent: 30%
  - in negotiation: 50%
  - verbal yes / awaiting payment: 75%
  - paid: 100%

### 2.5 Proposal value
- Definition: total SAR of proposals sent in a period.
- Helps detect "sending fewer / smaller proposals" trends early.

### 2.6 Payment follow-ups outstanding
- Definition: count of proposals in `payment_capture_queue` not yet terminal.
- Threshold: > 5 days since last follow-up triggers a flag.

### 2.7 Gross margin
- Definition: (revenue − COGS) / revenue.
- COGS for Dealix: AI cost + tool cost + contractor cost + delivery hours × rate.
- Updated per engagement and rolled up per month.

### 2.8 Founder hours
- Definition: founder time spent per engagement and per category (sales, delivery, ops, R&D).
- Source: `clients/<handle>/feedback.md` + the founder time-tracking note (see §5.2).
- Used to compute "real" gross margin.

### 2.9 Delivery hours
- Definition: hours spent on each paid engagement.
- Source: timesheet entry on the workspace.

### 2.10 AI / tool cost
- Definition: sum of `finance_events` with kind in `{ai_cost, tool_cost}`.
- Granularity: by provider, by workflow, by client (when attributable).

### 2.11 Runway
- Definition: `cash_on_hand / monthly_burn`.
- `monthly_burn` = trailing 30-day average of all outflows.
- Surfaced as **months** (e.g., "5.25 months"). Below 3 months → top-action banner on `/ceo`.

---

## 3. Decisions the Finance OS exists to support

These are decisions the founder makes weekly. Each has a metric trigger and a rough decision tree.

### 3.1 Raise price
- Trigger: ≥ 3 consecutive engagements with the same offer accept without negotiation.
- Decision: raise by 20% on the next two engagements; observe acceptance.

### 3.2 Reduce scope
- Trigger: gross margin on an offer drops below 60% for 2 consecutive months.
- Decision: trim the scope to the highest-leverage components; ship the same outcome with less work.

### 3.3 Kill bad revenue
- Trigger: an engagement consumes > 2× the budgeted founder hours **and** is below the target margin.
- Decision: complete the current scope, decline renewal, document the lesson in `client_os.md` of the engagement.

### 3.4 Hire contractor
- Trigger: a single category of delivery hours exceeds 20 hrs/week of founder time for 3 consecutive weeks.
- Decision: hire a contractor for that category; gross margin recomputed.

### 3.5 Buy tool
- Trigger: a manual workflow burns > 5 hrs/week and a tool costing < 5% of that hourly value exists.
- Decision: trial for 30 days; record AI/tool cost; compare margin.

### 3.6 Scale channel
- Trigger: a channel has CAC < 25% of LTV **and** is not bottlenecked by approval latency.
- Decision: double the channel spend; reassess in 14 days.

### 3.7 Pause channel
- Trigger: a channel's send → reply rate is below half the portfolio average for 2 consecutive weeks.
- Decision: pause; root-cause; do not restart without a written hypothesis.

### 3.8 Convert sprint to retainer
- Trigger: post-sprint feedback NPS ≥ 9 **and** the client used the deliverable in week 2.
- Decision: propose the Managed Ops retainer at the next check-in.

---

## 4. AI unit economics (the metric that compounds at scale)

| Metric                              | Formula                                                           |
|-------------------------------------|-------------------------------------------------------------------|
| `ai_cost_sar_per_proposal`          | sum(`finance_events.ai_cost` attributable) / proposals sent       |
| `ai_cost_sar_per_qualified_lead`    | sum(`ai_cost` for research + scoring) / leads scored qualified    |
| `tool_cost_sar_per_proposal`        | sum(`tool_cost`) / proposals sent                                 |
| `contribution_margin_per_proposal`  | (price − AI cost − tool cost − founder hours × rate) / price      |

Threshold to investigate: `contribution_margin_per_proposal < 70%`.

These metrics live on `/finance/unit-economics` and feed the **scale-channel** and **buy-tool** decisions above.

---

## 5. Source of truth

### 5.1 `finance_events` table
- Every cash event (`payment`), every cost (`ai_cost`, `tool_cost`, `contractor_cost`), and every recurring entry has a row.
- A reference link (Stripe id, provider invoice) is required.

### 5.2 Founder time tracking
- A single weekly form filled by the founder at end of week.
- Fields: hours spent in each category (sales, delivery, ops, R&D), by client when applicable.
- Stored in `private_ops/founder_time/YYYY-WW.yaml`.

### 5.3 Accounting reconciliation
- Monthly reconciliation against bank statements + bookkeeper records.
- Discrepancies trigger an investigation (Sev3); no metric is reported with unreconciled events older than 30 days.

---

## 6. Pricing principles

1. **Price the outcome, not the hours.** Hours are an internal accounting unit.
2. **Bracket the price by margin, not by the customer's preference.** Margin target: ≥ 70% on managed offers, ≥ 50% on custom.
3. **Stop discounting when the customer is willing to pay full price.** The Approval Center surfaces a flag if a proposal is below the floor for the offer.
4. **Recurring > one-time.** A retainer at 70% of the equivalent project price is preferred.
5. **Bundle proof, not features.** The price includes the proof artifact (case study) the customer will help us publish.

---

## 7. Cash discipline

- **Invoice terms:** 100% upfront for ≤ 5,000 SAR; 50/50 above; net-30 only for enterprise with a signed PO.
- **Late payments:** payment follow-up worker walks every overdue invoice daily.
- **Refunds:** A3. Always founder-approved. Always with a written reason.
- **Expenses:** any new recurring expense > 250 SAR/mo requires a `buy tool` decision recorded above.

---

## 8. Reporting cadence

| Report                  | Cadence  | Audience           |
|--------------------------|----------|--------------------|
| Daily cash digest        | Daily    | Founder            |
| Weekly scorecard         | Mon AM   | Founder            |
| Monthly close            | Month +5 | Founder + advisors |
| Quarterly review         | Quarter+10 | Founder + advisors |

All reports are generated by workers (`morning-digest`, `weekly-scorecard`, `monthly-close`). No manual report assembly.

---

## 9. Connection to other layers

- **Revenue Factory** writes `finance_events` for every payment.
- **Delivery OS** writes hours, AI cost attribution per engagement.
- **Worker Mesh** writes AI/tool cost per provider, per workflow.
- **Trust Plane** approves A2/A3 finance decisions (refunds, pricing changes, contractor hires).
- **Product Platform** reads margin per workflow to decide productization order.

---

## 10. Rule

> **Cash is the scoreboard. Margin is the protection. Retention is the compounder.**

Without cash, nothing else is true. Without margin, cash is fragile. Without retention, every month resets to zero.
