# Go-To-Market Strategy

> How we reach the Tier 1 ICP this quarter.
> Channel-by-channel. Each channel has a kill switch.

## GTM Thesis

The first 10 paying customers come from **founder-led warm outreach + public learning content**, not from paid acquisition.

Paid acquisition is DEFERRED until:
- 3 paid sprints delivered with proof
- 1 retainer signed
- Unit economics validated (CAC < 1/3 of LTV at lowest rung)

## Channels (in priority order)

### 1. Warm Founder Outreach (PRIMARY)
- **What:** Personal LinkedIn / WhatsApp messages from founder to Tier 1 prospects
- **Volume:** 25/week, founder-drafted or agent-drafted + founder-approved
- **Approval:** Every send goes through Trust Approval Matrix
- **Metric:** Reply rate ≥ 15%, call-booking rate ≥ 20% of replies
- **Kill switch:** If reply rate < 5% for 2 weeks → review messaging, change segment

### 2. Sector Reports + Public Learning Content (SECONDARY)
- **What:** One sector report per quarter + one weekly LinkedIn post
- **Distribution:** LinkedIn (Arabic + English), founder personal account
- **Approval:** Every post passes claim_guard.py
- **Metric:** ≥ 1 inbound lead per sector report; ≥ 3 inbound leads per quarter
- **Kill switch:** If no inbound after 6 weeks → swap format (video, carousel, podcast guest)

### 3. Referrals + Advisor Network (SECONDARY)
- **What:** Explicit referral asks at end of every sprint, plus quarterly advisor sync
- **Volume:** 1 explicit ask per closed sprint
- **Approval:** Standard delivery handoff
- **Metric:** ≥ 1 referred lead per 3 closed sprints
- **Kill switch:** If no referrals after 5 closed sprints → revisit handoff script

### 4. Partner Channel (TERTIARY)
- **What:** Accountants / consultants / cloud partners who serve the same ICP
- **Volume:** 1 partner conversation per month
- **Approval:** Partner agreement template required before referral fees
- **Metric:** ≥ 1 partner-sourced lead by end of quarter
- **Kill switch:** Defer if no traction by month 3

### 5. Paid Acquisition (DEFERRED)
Not active this quarter. See `READINESS_TO_INVEST.md` triggers above.

## Channel Mix Targets (this quarter)

| Channel | Lead share target |
|---|---|
| Warm outreach | 60% |
| Content inbound | 20% |
| Referrals | 15% |
| Partner | 5% |
| Paid | 0% |

If any channel exceeds target by 20pts, double down on it next quarter.
If any channel underperforms by 20pts for 2 months, kill it or rebuild it.

## Weekly GTM Cadence

- Sunday: refresh outreach queue (next week's 25 prospects, scored, drafted)
- Monday–Wednesday: send outreach in batches, log in pipeline
- Thursday: content post + reply on replies
- Friday: follow-ups + referral asks for closed deals
- Saturday: rest (forced rest — see RISK_REGISTER R-006)

## Messaging Pillars (used across all channels)

1. **Productized, not project-priced** — "499 SAR, 7 days, here's exactly what you get"
2. **Evidence over promise** — "Here's a sample report from a similar company (sanitized)"
3. **Trust over speed** — "We don't auto-send; you approve every external action"
4. **Founder operator, not vendor** — "I built this on me first; here's the public proof"

## Anti-Patterns (forbidden)

- Cold scraped lists (suppression-list policy)
- Mass automation without per-message approval
- Generic "AI transformation" messaging
- Pretending to be a team when it's the founder
- Sending in any language the buyer doesn't operate in
- Reaching out to anyone on the suppression list (enforced in code)

## GTM Review Cadence

- Weekly: channel mix vs target, reply rates, content engagement
- Monthly: kill switch evaluation per channel
- Quarterly: rewrite this doc, lock messaging pillars for next quarter

## What GTM Refuses

- Spray-and-pray
- Buying lists
- White-labeling outreach for an agency
- Conference booth sponsorships (this quarter)
- Webinars without a clear ICP attached
