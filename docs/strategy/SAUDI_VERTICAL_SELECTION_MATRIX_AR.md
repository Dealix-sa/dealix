# Saudi Vertical Selection Matrix

> **Status:** Scored by the bundle's `vertical_score_dry_run.py` against the 13-criterion rubric below.
> **Generated:** 2026-06-12.
> **Decision doc:** `BEST_FIRST_WEDGE_DECISION_AR.md`.

## Scoring rubric (sum to 100)

| Criterion | Max | Why |
| --- | --- | --- |
| pain intensity | 12 | Is the pain real, daily, and felt by the owner? |
| willingness to pay | 12 | Will they pay to fix it this quarter? |
| proof speed | 10 | Can we show a measurable result in ≤14 days? |
| decision maker access | 10 | Can the founder reach the decision maker in 2 steps? |
| sales cycle length | 8 | Days from first contact to paid pilot. |
| WhatsApp / follow-up chaos | 8 | Does the pain map to WhatsApp + lost follow-up? |
| dashboard relevance | 8 | Will a daily digest move the needle? |
| delivery complexity | 7 | Can we deliver with current staff and toolset? |
| compliance risk | -10 | Negative weight. Heavy fines? Data residency? |
| repeatability | 7 | Can we sell the same offer to 100 similar accounts? |
| referral potential | 7 | Will one customer pull 2+ others? |
| first offer fit | 7 | Does `Revenue Leak Audit` apply cleanly? |
| strategic logo value | 6 | Does a name in this sector open doors elsewhere? |

## Score table

| # | Vertical | Score | Top-3 reason | Top-1 disqualifier |
| -- | --- | --- | --- | --- |
| 1 | Marketing & Advertising Agencies | **84** | proof speed, WhatsApp chaos, repeatability | margin pressure caps WTP |
| 2 | B2B Services (consulting, IT, training) | 78 | decision maker access, repeatability | competitive noise |
| 3 | Training & Coaching Centers | 74 | WTP, WhatsApp chaos, decision maker access | seasonal enrollment swings |
| 4 | Private Clinics (medical, dental, cosmetic) | 71 | WTP, proof speed, pain intensity | compliance (patient data) |
| 5 | SaaS companies (early-stage) | 70 | decision maker access, dashboard relevance | low deal volume |
| 6 | Real Estate Brokerages | 67 | WTP, pain intensity | cycle length, market downturn |
| 7 | Law Firms | 62 | WTP, dashboard relevance | niche, hard differentiation |
| 8 | Logistics & Delivery | 60 | pain intensity, WhatsApp chaos | price sensitivity, ops-heavy |
| 9 | Restaurants & Local Chains | 58 | proof speed, WhatsApp chaos | churn, low WTP |
| 10 | Car Rental & Dealerships | 55 | pain intensity | offline-first sales process |
| 11 | HR & Recruitment | 52 | dashboard relevance | regulation, niche data |
| 12 | E-commerce (local) | 50 | WhatsApp chaos | wrong shape (ops, not sales) |
| 13 | Construction & Maintenance | 45 | — | wrong shape, not a SaaS fit |
| 14 | Hospitality & Tourism | 42 | — | seasonal, low repeatability |
| 15 | Hotels & Experiences | 38 | — | wrong shape, ops-heavy |

## Disqualification rules (apply before pursuing any vertical)

- **Compliance risk > 5** on the rubric — defer until founder reviews with legal counsel.
- **Sales cycle > 60 days** on average — defer; bundle targets cycle ≤ 30 days.
- **Proof speed < 7** — defer; we need a measurable result in ≤ 14 days.
- **First-offer fit < 6** — defer; the `Revenue Leak Audit` does not apply cleanly.
- **No decision-maker access in 2 steps** — defer; we cannot bypass procurement in week 1.

## What changed vs intuition

| Common intuition | Bundle's score | Why |
| --- | --- | --- |
| "Clinics are the obvious Saudi vertical" | 71, not #1 | Patient data raises compliance. Cycle is longer because owner delegates to operations manager. |
| "Real estate is hot" | 67, deferred | Listing market is colder. Agents are independent and hard to corral. |
| "Law firms have money" | 62, deferred | Highly niche, hard differentiation, partner-track resistance to "ops" tools. |
| "Logistics is everywhere" | 60, deferred | Price-sensitive, ops-heavy (route planning, not sales ops). |
| "Agencies are too small" | **84, #1** | Owners are operators, no procurement, repeat clients, tech-friendly. |

## What the founder should do with this

1. Read `BEST_FIRST_WEDGE_DECISION_AR.md` first.
2. Override only with a clear reason (your network, your past wins, your local knowledge).
3. Do not pursue more than **2 verticals** in week 1. One is better.
4. Re-score this matrix every 30 days based on real outcomes from your first 10 deals.

## Re-scoring cadence

Every 30 days:

- Pull conversion data from the founder command (`reports/launch/DAILY_FOUNDER_REVENUE_COMMAND_TEMPLATE.md`).
- Recompute the top 5 verticals.
- If a sector drops below 60, archive it from the active list.
- If a sector rises above 75, add it to the active list with a 2-week plan.
