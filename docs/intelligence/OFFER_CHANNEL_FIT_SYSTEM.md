# Offer-Channel Fit System

**Owner:** Strategy Office + Operators
**Source of truth:** This doc + `docs/intelligence/BUYER_PERSONA_SYSTEM.md` + `docs/growth/CHANNEL_PORTFOLIO_SYSTEM.md`

## Purpose

Offer-Channel Fit decides which Dealix sprint goes to which buyer through which channel. The same sprint pitched through the wrong channel is a non-event. The same channel carrying the wrong offer is noise.

## Three inputs

1. **Offer** — the named Dealix sprint (Lead Intelligence, AI Quick Win, Sector Map, Trigger Activation, KSA Entry, etc.).
2. **Buyer persona** — Founder, Head of Sales, Head of GTM.
3. **Channel** — Direct LinkedIn message, founder-to-founder intro, referral, sector event, partner pass-through, Contact-Form submission, Email (warm).

## Fit matrix

| Offer | Founder | Head of Sales | Head of GTM |
|---|---|---|---|
| Lead Intelligence Sprint | LinkedIn DM (warm) / referral | Referral / partner pass-through | Not first offer |
| AI Quick Win Sprint | LinkedIn DM / founder-to-founder | Referral | Not first offer |
| Sector Map Sprint | LinkedIn DM | LinkedIn DM (warm) / event intro | LinkedIn DM (warm) |
| Trigger Activation Sprint | Not primary | LinkedIn DM (warm) / referral | LinkedIn DM (warm) |
| KSA Entry Sprint | Not primary | Not primary | LinkedIn DM (warm) / partner |
| Sector Scorecard Sprint | Founder-to-founder | LinkedIn DM | LinkedIn DM / partner |
| Partner Activation Sprint | Founder-to-founder | Partner pass-through | Partner pass-through |

Cells that say "Not primary" or "Not first offer" indicate that the combination is plausible but not the default routing.

## Channel definitions

| Channel | What it is | Approval class |
|---|---|---|
| LinkedIn DM (warm) | Direct message to a persona who has at least one shared context (connection, comment, event) | A2 |
| LinkedIn DM (cold) | Direct message with no shared context | A2; Dealix limits to <= 3 cold DMs per persona per week per operator |
| Founder-to-founder | Direct intro between two founders, often by the Founder of Dealix | A2 |
| Referral | A current customer, partner, or peer introduces | A2 |
| Sector event intro | In-person or virtual event introduction | A2 |
| Partner pass-through | Partner forwards an inbound to Dealix | A1 (partner-led) + A2 (Dealix follow-up) |
| Contact-Form submission | Inbound from the Dealix website Contact Form | A1 (intake) + A2 (response) |
| Email (warm) | Email to a persona with prior context or referral | A2 |

## Channels Dealix does NOT use

- Cold email blasts.
- WhatsApp cold message.
- SMS broadcast.
- Paid display retargeting at named individuals.
- Scraped contact databases.

## Routing rules

1. The default routing for a Tier-A account is the highest-trust channel available (Founder-to-founder > Referral > LinkedIn DM warm > LinkedIn DM cold).
2. If the highest-trust channel is unavailable, the operator drops to the next level. The operator does not skip levels without justification.
3. No more than one offer-channel attempt per persona per 14 days. Persona fatigue is a trust violation.
4. Across an account, no more than three open channels active simultaneously. Multi-channel saturation reads as spam.

## Offer-channel calibration

Each sprint cycle, the operator records:

- Which offer-channel pairs produced replies.
- Which produced meetings.
- Which produced closed sprints.

After 90 days, low-performing pairs are de-prioritized in the matrix. After 180 days, low-performing pairs are removed from the default routing.

## When the matrix says "Not primary" but the operator wants to try

The matrix is the default. Off-matrix attempts are allowed but require:

- Explicit Founder approval (A2).
- Documented hypothesis ("Why I expect this to work where the matrix says no").
- Logged outcome.

Three failed off-matrix attempts on the same combination remove that path from operator discretion.

## Cross-link to growth machines

The Offer-Channel Fit System is the routing layer that the growth machines obey:

- `docs/growth/OUTBOUND_DRAFT_MACHINE.md` — drafts in the format the channel requires.
- `docs/growth/LINKEDIN_QUEUE_MACHINE.md` — queues LinkedIn channel sends.
- `docs/growth/EMAIL_DRAFT_MACHINE.md` — drafts email channel.
- `docs/growth/CONTACT_FORM_QUEUE_MACHINE.md` — handles inbound Contact-Form routing.
- `docs/growth/REPLY_ROUTER_MACHINE.md` — routes replies back to the right operator.

## Trust gate

| Action | Approval class |
|---|---|
| Matrix update | A1 — Strategy Office |
| Off-matrix attempt | A2 — Founder + Operator |
| Channel addition (e.g., new sanctioned channel) | A2 — Founder + Strategy Office |

## Failure mode

- An operator defaults to LinkedIn DM cold because it scales, ignoring higher-trust paths.
- Same persona receives three Dealix touches in one week.
- Sprint that fits Founder gets pitched to Head of GTM and falls flat.

## Recovery path

1. Re-anchor weekly routing to the matrix.
2. Pause the offending persona for 14 days.
3. Re-evidence channel choice with the Tier-A trust ladder.

## Disclaimer

Offer-channel fit is directional. Dealix does not guarantee response, meeting, or conversion from any combination. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
