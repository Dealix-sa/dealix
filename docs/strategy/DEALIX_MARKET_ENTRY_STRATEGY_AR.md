# Dealix Market Entry Strategy (Saudi Arabia)

> **Status:** Operating strategy. Default, not destiny.
> **Decision:** start with `Marketing & Advertising Agencies` (see `BEST_FIRST_WEDGE_DECISION_AR.md`).
> **Companion docs:** `SAUDI_VERTICAL_SELECTION_MATRIX_AR.md` · `DEALIX_POSITIONING_BIBLE_AR.md` · `COMPETITOR_POSITIONING_AR.md`.

## The 30-second mental model

Dealix is a **Revenue Operations System** for Saudi B2B SMEs. It is not a CRM, not a chatbot, not a marketing agency, not a dashboard. It is a layer above the company's daily ops that turns missed follow-ups, lost WhatsApp threads, and forgotten leads into next actions.

The wedge is a **3-to-5-day Revenue Leak Audit** that shows 10 specific losses and 10 specific fixes. The audit is the door. The offers behind it are productized.

## Who we serve in week 1

Marketing & advertising agencies with 5–50 people in Riyadh, Jeddah, Dammam, and the Eastern Province. Decision-maker is the owner or head of sales. Pain: lost client follow-ups, missed replies, no pipeline visibility.

## Who we serve in week 4

B2B services (consulting, IT services, training) and training/coaching centers. Same offer. Same shape. Different network.

## What we sell

A 6-tier offer ladder. Each offer is productized. None has a final price; all are `pricing_status: draft_only` until founder approval.

| # | Offer | Length | Buyer | Goes after |
| -- | --- | --- | --- | --- |
| 1 | Revenue Leak Audit | 3–5 days | Agency owner | first contact |
| 2 | WhatsApp & Follow-up OS | 2–4 weeks | Sales lead | audit deliverable |
| 3 | Sales Command Center | 4–6 weeks | Founder / GM | proven WhatsApp chaos |
| 4 | Proposal & Proof Pack OS | 4–8 weeks | Sales lead | selling motion exists |
| 5 | AI Operating System for SMB | 8–12 weeks | Founder | 2+ offers shipped |
| 6 | Custom Enterprise OS | 12+ weeks | COO / VP | SMB plan completed |

Full cards: `docs/offers/*_OFFER_AR.md`.

## How we sell

| Channel | Rule | Trust preflight |
| --- | --- | --- |
| Email | manual, one-by-one | required |
| LinkedIn | manual, no automation | required |
| Phone | manual, no robo-dialer | required |
| WhatsApp | only after explicit consent | required + `consent_record` |
| Referral | personal intro | required + source logged |

Every draft goes through `scripts/trust_preflight_dry_run.py` before the founder reviews it. Every send is logged in `templates/launch/approval_queue.example.json`.

## How we price

We don't, in week 1. Every offer card carries `pricing_status: draft_only`. The first time we set a real number, the founder approves it. See `docs/offers/PRICING_LOGIC_AND_APPROVAL_POLICY_AR.md`.

## How we deliver

The first 14 days of delivery are scripted in `docs/delivery/CLIENT_ONBOARDING_PLAYBOOK_AR.md` and `docs/delivery/FIRST_14_DAYS_CLIENT_DELIVERY_AR.md`. Every Monday, the client sees a value report (template: `docs/delivery/CLIENT_VALUE_REPORTING_AR.md`).

## How we renew

The renewal motion is the 30/60/90-day plan, plus `docs/delivery/RENEWAL_AND_UPSELL_PLAYBOOK_AR.md`. Renewal is a renewal, not a re-pitch. The client sees a year-end report and decides to continue, expand, or pause.

## How we scale

We don't, in week 1. Scaling is a month-3 problem. The 30/60/90 plan (`03_30_60_90_DAY_PLAN.md`) is the only scaling roadmap. Do not invent a separate one.

## What success looks like at day 30

- 30 target accounts researched and scored
- 20 outreach messages sent (after preflight)
- 5 discovery calls booked
- 1 audit delivered (free or paid)
- 0 claims made that the trust preflight would have rejected
- 1 case study draft (no client logo without permission)
- 1 founder weekly review completed

## What success looks like at day 60

- 3 paid pilots in motion
- 2 case studies approved
- 1 referral partner identified
- 1 industry event attended
- 1 content pillar chosen, 8 posts published

## What success looks like at day 90

- 1 repeatable revenue motion (audit → pilot → renewal)
- 1 founder command room live
- 1 sales assistant / setter contracted
- 1 enterprise conversation in progress
- 1 partner co-selling motion defined

## What failure looks like (so we can spot it early)

- More than 3 weeks with no discovery call booked
- More than 2 audits delivered with no upsell interest
- More than 1 trust preflight violation that the founder approves anyway
- More than 1 cold WhatsApp message sent
- More than 1 fake proof claim (testimonial without permission, fabricated numbers)

If any of these happen, the weekly review triggers a `pivot_or_pause` decision. The 30/60/90 plan has explicit stop conditions.

## The founder's first 7 days

See `02_FIRST_7_DAYS_EXECUTION.md`. Print it. Run it.
