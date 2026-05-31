# Revenue Marketing OS — Hermes Growth

> Marketing in Dealix is not impressions. It is **revenue infrastructure**.
> Every signal connects to an offer, every offer to a campaign, every campaign
> to a deal, every deal to verified revenue, and every revenue event to a
> learning that improves the next campaign.

This document is the source of truth for the **Revenue Marketing OS**
module: `dealix/revenue_marketing_os/` + `api/routers/revenue_marketing_os.py`.

---

## 1. The Money Loop

Marketing inside Dealix obeys exactly one loop:

```
Market Signal
  → ICP
  → Pain
  → Offer
  → Message
  → Channel
  → Lead
  → Call
  → Proposal
  → Revenue
  → Outcome
  → Learning
  → Better Campaign
```

If a campaign cannot be placed inside this loop, it does not run.

---

## 2. Hard Gates (`HARD_GATES` in `governance.py`)

| Gate | Meaning |
| --- | --- |
| `no_live_send` | No external sends without explicit founder approval. |
| `no_scraping` | No scraping any third-party site. |
| `no_cold_outreach_automation` | No cold WhatsApp / LinkedIn DM automation. |
| `no_paid_spend_without_attribution` | No paid ad budget before attribution is wired. |
| `no_claim_without_trust_check` | Every public claim must pass `check_claim()`. |
| `no_unapproved_case_study` | Case studies are draft until the founder approves. |
| `no_named_customer_without_consent` | Named customers require written consent. |
| `no_revenue_numbers_in_public_without_approval` | Money numbers go through Approval Center. |
| `no_guaranteed_results_claim` | Forbidden by the No-Overclaim register. |
| `no_full_compliance_promise` | Forbidden — we describe controls, not guarantees. |
| `no_unverified_revenue_counted` | `paid` / `invoiced` / `committed` require proof flags. |

---

## 3. Module layout

```
dealix/revenue_marketing_os/
├── __init__.py            # public surface
├── schemas.py             # Pydantic records (ICP, Offer, Message, Campaign, Lead, Touch, Revenue, Attribution, Experiment, ScaleKillDecision)
├── store.py               # JSON-backed thread-safe single-blob store
├── scoring.py             # Lead score + Revenue Quality + funnel ratios
├── attribution.py         # first/last/multi-touch attribution + summary
├── governance.py          # Trust check + revenue assurance + action gate
├── dashboard.py           # Dashboard aggregator + scale/kill engine
├── seed.py                # Idempotent offer-ladder + ICP seed
└── seed_offers.yaml       # Offer ladder + ICP card seed
api/routers/revenue_marketing_os.py   # HTTP surface (Hermes Growth)
```

---

## 4. HTTP surface

All admin routes are mounted under `/api/v1/hermes/growth/` and require
`X-Admin-API-Key` (the same admin gate as every other Dealix admin
surface). Public read-only routes are mounted at
`/api/v1/hermes/growth/public/`.

| Method + path | Purpose |
| --- | --- |
| `GET /status` | Module status + counts + hard gates |
| `POST /seed` | Idempotent offer-ladder + ICP seed |
| `GET /offers` | List offer ladder |
| `GET /icps` | List ICP cards |
| `POST /campaigns` | Create a campaign in `draft` |
| `GET /campaigns` | List campaigns |
| `POST /campaigns/{id}/approve` | Founder approval → `active` |
| `POST /leads` | Capture lead + compute fit score |
| `GET /leads?campaign_id=` | List leads |
| `POST /touches` | Record a touch + optionally advance lead status |
| `POST /experiments` | Register a message/channel experiment |
| `GET /experiments` | List experiments |
| `POST /revenue` | Record revenue (rejects unverified `paid`) |
| `GET /revenue` | List revenue |
| `GET /revenue-quality` | Per-record + average quality score |
| `POST /attribution` | Compute + persist attribution rows for a revenue event |
| `GET /attribution` | List attribution + by-channel/campaign/offer summary |
| `GET /dashboard` | Money-loop dashboard snapshot |
| `POST /scale-kill/{campaign_id}` | Suggest a scale/pause/kill decision (founder still approves) |
| `POST /governance/claim-check` | Run text through the No-Overclaim guard |
| `POST /governance/action-check?action=...` | Check approval-required actions |
| `GET /funnel` | B2B funnel ratios |
| `GET /public/offer-ladder` | Public read-only view of the offer ladder |

---

## 5. Scoring laws

```
Lead Score =
  0.25 ICP fit + 0.20 pain likelihood + 0.20 ability to pay +
  0.15 urgency + 0.10 partner potential + 0.10 trust fit

Revenue Quality =
  0.25 margin + 0.20 repeatability + 0.20 retainer potential +
  0.15 data moat + 0.10 partner potential - 0.10 delivery burden
```

Both are pure functions in `scoring.py`. The lead score is clipped to
0-100. The revenue quality score is clipped to `[0, 100]` so a heavy
one-off ranks below a small recurring contract.

---

## 6. Revenue Assurance — what counts as revenue

Likes, views, replies, booked meetings, and verbal interest **do NOT
count**. Revenue Assurance accepts a record only when:

| Status | Required proof |
| --- | --- |
| `paid` / `retainer_active` / `renewed` / `expanded` | `payment_verified` OR `invoice_verified` |
| `invoiced` | `invoice_verified` |
| `committed` | `agreement_signed` |
| `pipeline` / `proposal_sent` / `influenced` | No proof required (not counted as real revenue) |

The dashboard's `verified_revenue_sar` aggregates only records that
pass `scoring.revenue_is_real()`.

---

## 7. Attribution

`attribution.compute_attribution()` supports three models:

* **`first_touch`** — full credit to the earliest touch.
* **`last_touch`** — full credit to the most recent touch.
* **`multi_touch`** — equal-weight credit across every touch.

Unverified revenue gets zero attribution rows. Verified revenue with
no touches falls back to a `channel_influenced` self-credit row so
the dashboard's "Revenue by Channel" is never blank.

`attribution.summarize_attribution()` aggregates by channel,
campaign, offer, and attribution type for the dashboard.

---

## 8. Scale / Kill engine

`dashboard.evaluate_campaign()` reads the campaign's `target_accounts`
+ funnel metrics and suggests one of: `scale`, `pause`, `kill`,
`hold`. The suggestion ALWAYS carries
`requires_founder_approval=true` — there is no auto-act path.

Default thresholds match the spec:

| Condition | Suggestion |
| --- | --- |
| `targeted ≥ target_accounts` and `paid_diagnostics ≥ 3` | `scale` |
| `targeted ≥ target_accounts` and `qualified_replies == 0` | `kill` |
| `targeted ≥ target_accounts / 2` and `paid_diagnostics == 0` | `pause` |
| otherwise | `hold` |

---

## 9. Seed offers

`seed.seed_if_empty()` (or `POST /seed`) idempotently loads the offer
ladder from `seed_offers.yaml`:

| Tier | Offer |
| --- | --- |
| free | AI Governance Checklist |
| entry | Revenue Hunter Pilot · AI Trust Diagnostic · Workshop |
| core | AI Trust Kit · Monthly Revenue Command · Agency White-label |
| expansion | Executive PMO |
| enterprise | Agent Governance OS · Agentic Control Plane |

And three ICP cards: marketing agencies, B2B SMEs, AI Governance buyers.

---

## 10. Tests

```
tests/test_revenue_marketing_os.py
```

Covers the 11 non-negotiables (see the docstring in that file) plus
the full end-to-end Money-Loop integration test:

```
campaign → lead → touch → revenue → attribution → dashboard
```

---

## 11. What this module does NOT do

* Send any external message (every send is a draft).
* Auto-scale any campaign (every decision is a suggestion).
* Count any revenue that lacks a verification flag.
* Publish any claim that hits the No-Overclaim guard.
* Issue any payment, refund, or discount (those live in `dealix.payments`).

The Money Loop runs through the Approval Center for everything that
touches an external party.
