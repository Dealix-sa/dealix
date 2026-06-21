# Dealix — Best First Wedge Decision (Default)

> **Status:** Default decision, not destiny. Override based on your network.
> **Generated:** 2026-06-12. Based on `SAUDI_VERTICAL_SELECTION_MATRIX_AR.md` (15-sector scoring).
> **Audience:** the founder. Print this. Tape it to your wall.

## TL;DR

**Start with: Marketing & Advertising Agencies** (B2B services, 5–50 people, Riyadh/Jeddah).

Run the **Revenue Leak Audit** as the first offer. Price it as `draft_only` until you sign two.

Why this sector and not the obvious one (clinics, real estate, law):

| Reason | Detail |
| --- | --- |
| **Proof speed** | Agencies already have messy WhatsApp inboxes and lost follow-ups. You can demo the audit on their data in 3 days. |
| **Decision-maker access** | The owner is the sales lead. No procurement gate. |
| **Repeatability** | 1,000+ agencies in KSA, all running on WhatsApp + HubSpot/Notion + manual chasing. |
| **Word of mouth** | Agency owners know each other. One case study pulls 5 referrals. |
| **Delivery complexity** | Low — agencies are tech-friendly, no heavy data residency, no PII. |
| **Compliance risk** | Low — no patient data, no legal data, no financial data. |
| **WhatsApp relevance** | 10/10 — agencies run on WhatsApp for client comms. |
| **WTP** | Mid — agencies are margin-pressed but see ROI when framed as "recover lost leads". |

## The vertical scoring in one table

| Sector | Score | Action |
| --- | --- | --- |
| Marketing & Advertising Agencies | 84 | **Start here** |
| B2B Services (consulting, IT, training) | 78 | Warm sequence week 2 |
| Training & Coaching Centers | 74 | Warm sequence week 3 |
| Private Clinics (medical, dental, cosmetic) | 71 | Pursue week 4, but longer cycle |
| SaaS companies (early-stage) | 70 | Warm sequence week 4 |
| Real Estate Brokerages | 67 | Defer — cycle too long, listing market is cold |
| Law Firms | 62 | Defer — niche, hard differentiation |
| Logistics & Delivery | 60 | Defer — too price-sensitive |
| Restaurants & Local Chains | 58 | Defer — high churn, low WTP |
| Car Rental & Dealerships | 55 | Defer — sales process is offline-first |
| HR & Recruitment | 52 | Defer — regulation-sensitive |
| E-commerce (local) | 50 | Nurture only — not a fit for ops |
| Construction & Maintenance | 45 | Ignore — not a fit for SaaS-style OS |
| Hospitality & Tourism | 42 | Ignore — seasonal, low repeatability |
| Hotels & Experiences | 38 | Ignore — wrong shape |

(Full scoring and 13 sub-criteria in `SAUDI_VERTICAL_SELECTION_MATRIX_AR.md`.)

## The first offer

**Dealix Revenue Leak Audit** — 3 to 5 days.

What the founder actually does:

1. **Day 1:** Sit with the agency's sales lead. Watch their WhatsApp, CRM, and inbox for 60 minutes. Note every place a follow-up got dropped.
2. **Day 2–3:** Pull the data (with permission) into the Dealix read-only analyzer. Tag 10 specific lost opportunities.
3. **Day 4:** Deliver a 1-page report: 10 leaks, 10 fixes, 1 quick win to run this week.
4. **Day 5:** 30-min debrief call. No pitch unless they ask. Offer the WhatsApp & Follow-up OS as a paid pilot only if they ask.

What you **do not** do in week 1:

- No pricing in the audit. The audit is the door, not the upsell.
- No proposal before the debrief.
- No "case study" claim in week 1 — you have no case yet.
- No WhatsApp message to anyone who did not consent.

## The 7-day execution

See `02_FIRST_7_DAYS_EXECUTION.md` for the day-by-day. The shape:

- **Day 1** — Pick the vertical (agencies). Pick the offer (audit). Pick the first 10 target agencies from your network.
- **Day 2** — Research the 10 agencies (LinkedIn, website, Google Maps). Fill `templates/launch/target_account.example.json` × 10. Score each.
- **Day 3** — Write 10 outreach drafts. Run `scripts/trust_preflight_dry_run.py` on every draft. Reject anything that fails.
- **Day 4** — Founder reviews. Send manually through the channel that fits each lead (email / LinkedIn / phone).
- **Day 5** — Follow up on replies. Book 2–3 discovery calls.
- **Day 6** — Run the first audit (offline) using the agency's permissioned data. Build the report skeleton.
- **Day 7** — Founder's weekly review. Decide: double down on agencies, or pivot.

## The kill criteria

Stop the agency wedge if, by day 14:

- You sent 20+ outreach messages and got **fewer than 3 replies**.
- You had 3+ discovery calls and **zero audit signed off**.
- The agency owners you talked to all said "we already have HubSpot / Notion / a VA" and refused to look at the audit.

Pivot to the next-best vertical from the table — usually **B2B Services** or **Training Centers**.

## The compounding assumption

The first audit is **proof**, not revenue. The cash comes from the second offer (WhatsApp & Follow-up OS) and the third (Sales Command Center). Plan for a 60-day payback on the first paid engagement, not a 7-day one. The wedge is about learning, not about closing fast.

## What you actually need to do *today*

1. Open `docs/offers/REVENUE_LEAK_AUDIT_OFFER_AR.md`. Read it.
2. Open `docs/sales/EMAIL_SEQUENCE_LIBRARY_AR.md`. Pick the first email.
3. Open `docs/sales/OBJECTION_HANDLING_BIBLE_AR.md`. Read the top 5 objections.
4. Open `docs/sales/DISCOVERY_CALL_SCRIPT_AR.md`. Memorize the 5 opening questions.
5. Send the first outreach before midnight. Not after a polish round — after one read-through.

The bundle is not a checklist. It is a starting line. Run.
