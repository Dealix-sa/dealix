# First 100 Target Accounts Template

> **Status:** Empty template. The founder fills it manually.
> **Schema:** `schemas/launch/target_account.schema.json`.
> **Companion:** `TARGET_ACCOUNT_RESEARCH_PLAYBOOK_AR.md`.

## How to use this template

Print this page. For each of the 100 accounts, fill one row manually. The math:

- 100 accounts researched.
- 30 with ICP score ≥ 65.
- 10 pursued.
- 3 reply.
- 1 discovery booked.
- 1 audit delivered.

The numbers are harsh. They are also realistic.

## The template (one row per account)

| # | Company | Sector | City | Decision Maker | Likely Pain | First Offer | ICP Score | Source | Permission | Channel | Approval | Next Action | Notes |
| -- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | | | | | | REVENUE_LEAK_AUDIT | /100 | | implicit/inbound/warm | email/LinkedIn/phone/WhatsApp-after-consent | pending | | |
| 2 | | | | | | | | | | | | | |
| 3 | | | | | | | | | | | | | |
| ... | | | | | | | | | | | | | |
| 100 | | | | | | | | | | | | | |

## Field glossary

| Field | Allowed values |
| --- | --- |
| Company | name from website |
| Sector | from the 15 in `SAUDI_VERTICAL_SELECTION_MATRIX_AR.md` |
| City | Riyadh, Jeddah, Dammam, other |
| Decision Maker | name + role |
| Likely Pain | from `BUYER_PAIN_MAP_AR.md` |
| First Offer | REVENUE_LEAK_AUDIT (default for top 50%) |
| ICP Score | 0–100 per `ICP_SCORING_SYSTEM_AR.md` |
| Source | founder network, LinkedIn manual, Google Maps, public site, event, referral, inbound |
| Permission | explicit (they asked), implicit (engaged with content), none (cold) |
| Channel | email, LinkedIn manual, phone, WhatsApp-after-consent |
| Approval | pending, approved, sent, replied, paused |
| Next Action | specific: "send email #1" or "book discovery" |
| Notes | one line, max 200 chars |

## The 30-row MVP

You do not need 100 in week 1. You need 30. The math:

- 30 researched (15 min each = 7.5 hours).
- 15 with ICP score ≥ 65.
- 5 pursued.
- 1 reply (a 20% reply rate is good).
- 1 discovery booked.

7.5 hours of research for 1 discovery call. That is the cost of doing this right.

## The 100-row plan

If you have 2 weeks of runway and want to go hard:

- Week 1: 30 researched, 10 pursued, 1 reply.
- Week 2: 30 more researched (total 60), 10 more pursued (total 20), 3 more replies.
- Week 3: 40 more researched (total 100), 20 more pursued (total 40), 5 more replies.
- Week 4: re-score the active 40; drop the bottom 20; pursue the top 20.

The 100 is a target, not a deadline. The active list should always be 30–50.

## How to track

- Use the JSON schema in `schemas/launch/target_account.schema.json`.
- One file per account in `data/launch/targets/<account_id>.json`.
- Aggregate weekly in `reports/launch/DAILY_TARGET_ACCOUNT_REVIEW_TEMPLATE.md`.

## When to abandon the list

If after 2 weeks you have 0 replies from 20 pursuits, the message is broken. Stop sending. Rewrite the email sequence. Re-test on 5 new accounts. If still 0, the wedge may be wrong — go back to `BEST_FIRST_WEDGE_DECISION_AR.md`.
