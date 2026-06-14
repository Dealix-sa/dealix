# Target Account Research Playbook

> **Status:** Manual research, no scraping.
> **Output:** `templates/launch/target_account.example.json` filled for each account.

## The 7-step research flow (15 min per account)

1. **Google search** the company name. Note: website, year founded, size hint.
2. **Open the website**. Read the homepage. Note: services, target market, claims.
3. **LinkedIn search** the company. Note: employee count, key roles, recent posts.
4. **Find the decision maker**. Founder / GM / head of sales. Note name.
5. **Read their LinkedIn posts** (last 30 days). Note: tone, topics, complaints, wins.
6. **Google Maps** if local. Note: reviews, hours, location.
7. **Mutual network** check. Anyone we both know? Note intro path.

Total: 15 minutes. If you cannot finish in 15, the account is not a priority.

## The fields to fill (target account JSON)

| Field | Example | Source |
| --- | --- | --- |
| `account_id` | `agency_x_riyadh` | internal |
| `company_name` | "Agency X" | website |
| `sector` | "marketing_agency" | website |
| `city` | "Riyadh" | Google Maps |
| `size_estimate` | "5–50" | LinkedIn |
| `decision_maker_name` | "Sara" | LinkedIn |
| `decision_maker_role` | "Founder" | LinkedIn |
| `likely_pain` | "lost follow-ups on WhatsApp" | research |
| `first_offer` | "REVENUE_LEAK_AUDIT" | bundle |
| `icp_score_total` | 86 | rubric |
| `contact_source` | "founder network" | manual |
| `permission_status` | "implicit (inbound content)" | manual |
| `outreach_channel` | "email" | decision |
| `approval_status` | "pending_founder_review" | process |
| `next_action` | "send draft email #1" | action |
| `notes` | "She posted about losing a big client last month." | research |

## The data sources (allowed)

- LinkedIn (manual).
- Company website.
- Google Maps.
- Public reviews.
- Public social profiles.
- Inbound inquiries.
- Referral intros.
- Event follow-ups.

## The data sources (NOT allowed)

- Scraped LinkedIn exports.
- Purchased lead lists.
- Cold WhatsApp numbers from a third party.
- Apollo / ZoomInfo / Lusha (these are scraping tools; do not use).
- "I googled their email pattern and guessed" — guessing is not allowed.

If you do not have the data manually, mark the field as `unknown` and re-research later.

## The research output format

Save each account to a separate file in `data/launch/targets/<account_id>.json`. Use the schema in `schemas/launch/target_account.schema.json`.

Do not put 30 accounts in one file. Do not put real PII (phone, email) in the file. The file is for **research and prioritization**, not for outreach. Outreach happens manually, in your own tool, after the founder approves the draft.

## The "do not pursue" signals

Drop the account from the active list if any of these are true:

- They have a public dispute or lawsuit active.
- They are in a sector we have explicitly excluded.
- The decision maker has explicitly asked not to be contacted (e.g. on their LinkedIn).
- The company is in a different geography and we are not licensed to operate there.
- The ICP score is below 50.

## The 30-account minimum for week 1

You will not pursue 30 accounts in week 1. You will **score** 30 and pursue 5–10. The 30 is the funnel:

- 30 scored
- 10 pursued (top ICP)
- 3 replied
- 1 discovery booked
- 1 audit delivered

The math is harsh. The math is real. Plan accordingly.

## The re-score cadence

Every Monday, re-score the active list. Add new accounts. Drop stale ones. The list is alive, not a one-time artifact.
