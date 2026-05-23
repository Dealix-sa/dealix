# Partner Acquisition

> How we recruit, onboard, and manage partners.
> Partners serve our ICP but don't compete with our offer.

## Why Partners

Partners reach buyers we can't reach alone:
- Accountants see ledgers (= revenue reality of their clients)
- Consultants advise on growth (= can recommend operating layer)
- Cloud / CRM partners see tooling adoption gaps
- Sector trade associations have closed audiences

## Ideal Partner Profile

- Serves Saudi mid-market (same ICP)
- Has a relationship with founders/CEOs (not just procurement)
- Does **not** sell productized revenue ops themselves
- Has ≥ 5 active client relationships in our Tier 1 sectors
- Is willing to refer in exchange for transparent referral fees
- Saudi-based or has Saudi delivery team

## Partner Types

| Type | Example | Fit | First-90-day target |
|---|---|---|---|
| Accountant / CFO services firm | Boutique accounting practice | High | 1 partner signed |
| Boutique business consultant | Strategy / ops consultancy | High | 1 partner signed |
| Cloud / CRM reseller | Salesforce, HubSpot Saudi partner | Medium | 1 conversation |
| Sector trade association | Logistics chamber | Medium | Speaker / member |
| Founder communities | Saudi YC alumni, sector founder groups | Medium | 1 active participation |
| Government innovation hub | SDAIA, Misk | Low (this quarter) | Defer |

## Recruitment Process

1. Identify 3 candidate partners per month (founder + advisor input)
2. Founder-personal outreach (no agent for first touch)
3. Coffee / Zoom meeting — explain Dealix's model + the partnership structure
4. If interest: send Partner Agreement template (link: `legal/partnership_template.md` in private)
5. Pilot: agree on 1 referral within 60 days as proof of concept
6. If pilot lands: formalize quarterly review cadence

## Referral Terms (default)

- 10% of first 6 months of recurring revenue (Managed Ops)
- 5% one-time fee for Sprint or Data Pack closed-won
- Paid 30 days after Dealix receives payment from the customer
- Capped at SAR 25K per referral per year (CFO sanity)
- Documented in `partners/partner_pipeline.csv` (private)

## What Partners Get From Us

- A productized offer they can recommend confidently
- Quarterly performance report (referrals sent / closed / fees)
- Co-branded sector reports (with their attribution)
- Founder accessibility for any client question

## What Partners Don't Get

- White-labeling (we are not a reseller channel)
- Exclusive territory (unless documented + reciprocal)
- Pricing flexibility (productized prices apply)
- Access to our customer list or pipeline
- Permission to send on our behalf

## Anti-Pattern Partners (do not engage)

- Spammy "lead-gen agencies"
- Anyone proposing to sell us a list
- Anyone wanting equity in exchange for an intro
- Anyone with a recent public trust incident
- Anyone in our competitive set

## Partner Pipeline Tracking

`partners/partner_pipeline.csv` (private) schema:
```
partner_id, name, type, status, first_contact_at, last_action_at, signed_at, referrals_sent, referrals_closed, fees_paid_sar, notes
```

Status enum: `prospect | conversation | pilot | active | paused | offboarded`

## Quarterly Partner Review

- Active partners: referral volume vs target
- Stuck partners: convert to active or move to paused
- Offboard if no referrals in 6 months + no plausible reason

## What This Refuses

- Pay-for-intro relationships disguised as partnerships
- Partnerships that require client data sharing
- Anything that compromises the productized model
- Partnerships announced publicly before pilot proves out
