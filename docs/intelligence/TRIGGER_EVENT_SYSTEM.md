# Trigger Event System

**Owner:** Strategy Office + Operators
**Source of truth:** This doc + `docs/intelligence/ACCOUNT_SCORING_MODEL.md`

## Purpose

Trigger events are observable signals that a candidate account has entered a window where Dealix's offer is timely. Without trigger discipline, outreach defaults to spray-and-pray. With it, outreach lands on buyers in their open moment.

## Trigger taxonomy

Triggers cluster into five families.

### 1. Capital triggers

| Trigger | Why it opens a window |
|---|---|
| Funding round announced | Spend bias is high; revenue infrastructure decisions get prioritized |
| New investor on board | Board pressure to formalize revenue ops |
| M&A announcement | Integration creates pipeline rebuild need |
| Major customer concentration risk publicly disclosed | Diversification pressure |

### 2. Talent triggers

| Trigger | Why it opens a window |
|---|---|
| New Head of Sales hired | Wants to ship change in first 90 days |
| New Head of GTM or VP Sales hired | Same pattern at larger company size |
| Sales team expanded (3+ hires in a quarter) | Onboarding velocity requires playbooks |
| Senior commercial departure | Pipeline gap opens fast |

### 3. Market/product triggers

| Trigger | Why it opens a window |
|---|---|
| New product or service launched | Needs go-to-market motion |
| Expansion into a new sector or geography | Needs sector-specific deal flow |
| Pricing change publicly announced | Repositioning creates outbound rewrite need |
| Public RFP issued | Competitive moment with clear scope |

### 4. Operational triggers

| Trigger | Why it opens a window |
|---|---|
| Public job posting for "Revenue Operations" or "SDR" or "Growth" | Acknowledged ops gap |
| Public statement about a flat or down quarter | Revenue urgency surfaces |
| CRM migration announcement | Integration window for the layer above CRM |
| Public partnership announcement | Network expansion mode |

### 5. Saudi-specific triggers

| Trigger | Why it opens a window |
|---|---|
| KSA office opening | Need for KSA-specific revenue infrastructure |
| Vision-2030-related contract win | Capacity expansion requires deal flow infra |
| PDPL compliance announcement | Governance posture matters; trust-gated tools land |
| New Saudi sector regulator decision | Sector dynamics shift |

## Trigger sourcing — sanctioned only

- Public company announcements (press, official social).
- Public job boards.
- Public industry news.
- Founder or operator's own conversation logs.
- Partner-supplied (where the partner has authorization).

Triggers are NEVER sourced from:

- Scraped data.
- Private leaks.
- Third-party "intent data" that lacks documented provenance.
- Personal social posts from individual employees without context.

## Trigger qualification

Not every trigger fires Dealix outreach. Qualification rules:

1. The account must already be ICP-fit. A trigger on an out-of-ICP account is noted, not actioned.
2. The trigger must be no older than 90 days.
3. At least one specific person at the account must be identifiable as the right persona (see `BUYER_PERSONA_SYSTEM.md`).
4. The outreach hypothesis must connect the trigger to a specific Dealix offer in a single sentence.

If any of the four fail, the trigger is logged but not actioned.

## Trigger and account scoring

A qualified trigger adds to the account's score (see `ACCOUNT_SCORING_MODEL.md`). A stale trigger (>90 days) decays to zero. Multiple compounding triggers (e.g., funding + new HoS in the same quarter) score higher than two unrelated triggers.

## Trigger and outreach

When a qualified trigger fires:

1. The Outbound Draft Machine generates a tailored draft referencing the trigger (see `docs/growth/OUTBOUND_DRAFT_MACHINE.md`).
2. The draft enters the queue at approval class A2 for founder review.
3. On approval, the draft is sent through the sanctioned channel for that persona.
4. The send is logged with trigger reference.

## Trigger maintenance

- Weekly: scan for new triggers across active sectors.
- Weekly: decay triggers older than 90 days.
- Monthly: review trigger-to-reply rate; retire trigger types that produce no replies across three months.

## Trust gate

| Action | Approval class |
|---|---|
| New trigger pattern added to taxonomy | A1 — Strategy Office |
| Trigger-driven outreach draft | A2 — Founder + Operator |
| Bulk send across multiple triggered accounts in one batch | A2 — Founder + Operator (per batch) |

## What this system does NOT do

- It does not scrape.
- It does not buy intent data.
- It does not auto-send on trigger detection.
- It does not surface or sell trigger lists to third parties.

## Failure mode

- Outreach fires on stale triggers; receivers ignore.
- Trigger noise (e.g., "logo color change") gets actioned.
- Trigger source provenance is undocumented; later audit cannot reconstruct.

## Recovery path

1. Re-run the qualification rules on the current trigger queue.
2. Decay stale entries.
3. Re-document provenance for any actioned trigger missing the source field.

## Disclaimer

Trigger events are signals, not predictions. A triggered account may not respond. Dealix does not guarantee response, meeting, or conversion. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
