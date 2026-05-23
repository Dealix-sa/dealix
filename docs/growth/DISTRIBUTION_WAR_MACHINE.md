# Distribution War Machine

**Owner:** Founder
**Source of truth:** This doc + `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md`

## Purpose

"Distribution War Machine" is Dealix's umbrella term for the coordinated set of growth machines that produce, gate, and route demand. It is not a single piece of software. It is a discipline that says: every distribution surface must produce a queued draft, every queued draft must pass a named approval gate, and every approved send must produce a logged outcome.

The word "war" is operational — it means daily, sustained, and never improvised. It does not mean aggressive outbound at scale. Dealix does not do aggressive outbound at scale.

## The four loops

Distribution at Dealix runs four loops, each addressed by a subset of the machines below.

### Loop 1 — Identify

Find candidate accounts and trigger events through sanctioned sources. Owned by the Intelligence layer (`docs/intelligence/`).

### Loop 2 — Draft

Produce persona-specific, channel-specific drafts for every qualified account. Owned by the Draft Machines (`OUTBOUND_DRAFT_MACHINE.md`, `EMAIL_DRAFT_MACHINE.md`, `LINKEDIN_QUEUE_MACHINE.md`, `CONTACT_FORM_QUEUE_MACHINE.md`).

### Loop 3 — Gate and send

Pass each draft through the named approval class and execute through the sanctioned channel. Owned by the Approval architecture (`docs/05_governance_os/`) and the Reply Router.

### Loop 4 — Convert and capture

Move replies through to meetings, sprints, and Proof Packs. Capture every closed loop as a Capital asset. Owned by the Follow-Up, Nurture, Reply Router, Proof-to-Demand, and Capital machines.

## The 12 machines

| Machine | Loop | Doc |
|---|---|---|
| Outbound Draft | Draft | `OUTBOUND_DRAFT_MACHINE.md` |
| LinkedIn Queue | Draft | `LINKEDIN_QUEUE_MACHINE.md` |
| Email Draft | Draft | `EMAIL_DRAFT_MACHINE.md` |
| Contact Form Queue | Draft | `CONTACT_FORM_QUEUE_MACHINE.md` |
| Follow-Up | Convert | `FOLLOW_UP_MACHINE.md` |
| Reply Router | Gate/Send | `REPLY_ROUTER_MACHINE.md` |
| Nurture | Convert | `NURTURE_MACHINE.md` |
| Partner Referral | Identify/Convert | `PARTNER_REFERRAL_MACHINE.md` |
| ABM Strategic Account | Identify/Convert | `ABM_STRATEGIC_ACCOUNT_MACHINE.md` |
| Proof to Demand | Convert | `PROOF_TO_DEMAND_MACHINE.md` |
| Content to Demand | Identify/Draft | `CONTENT_TO_DEMAND_ENGINE.md` |
| Channel Portfolio | All | `CHANNEL_PORTFOLIO_SYSTEM.md` |

## Operating principles

1. **Prepare, queue, recommend. Do not auto-execute externally.** Every machine produces a draft, a queue entry, or a recommendation. External sends require explicit founder or customer approval.
2. **Sanctioned channels only.** See `OFFER_CHANNEL_FIT_SYSTEM.md` for the channel whitelist.
3. **One persona, one offer, one channel per touch.** Multi-channel saturation per touch is forbidden.
4. **Trigger discipline.** Outreach fires on qualified triggers (see `TRIGGER_EVENT_SYSTEM.md`), not on the calendar.
5. **Every send produces an entry in the approval log.**

## Daily operating rhythm

| Time | Action | Owner |
|---|---|---|
| Morning | Trigger scan; new qualified accounts enter the Draft Machine | Operator |
| Mid-morning | Draft Machine queues new drafts at approval class A2 | Operator |
| Late morning | Founder reviews queue; approves or revises | Founder |
| Afternoon | Approved drafts dispatched through sanctioned channels | Operator |
| End of day | Reply Router routes incoming replies; Follow-Up scheduler updates | Operator |
| Weekly | Account scoring rerun; tier movement; nurture cadence update | Operator + Strategy Office |

## Capacity model

The Distribution War Machine is bounded by:

- One Founder approval throughput (estimated 30-60 approved sends per day).
- Per-operator Tier-A capacity (25 accounts).
- Per-persona touch frequency (one Dealix touch per 14 days).

These bounds are features. They prevent the machine from drifting into spam.

## Trust gate

| Action | Approval class |
|---|---|
| New machine added to the Distribution War Machine | A2 — Founder + Strategy Office |
| Channel added to the portfolio | A2 — Founder + Strategy Office |
| Approval class change for any machine | A3 — Founder only |

## Failure mode

- A machine bypasses the approval queue and ships externally.
- One persona receives multiple Dealix touches in a week.
- Reply Router fails to route a hot reply; the conversation dies.
- Drafts pile up in the queue beyond founder approval throughput.

## Recovery path

1. Pause the bypassing machine.
2. Audit the approval log for the affected window.
3. Apology + reset to the affected personas if multiple touches landed.
4. Adjust draft throughput to founder approval throughput.

## Cross-links

- All machines: `docs/growth/AUTONOMOUS_DISTRIBUTION_MACHINES.md`
- Channel portfolio: `docs/growth/CHANNEL_PORTFOLIO_SYSTEM.md`
- Approval policy: `docs/05_governance_os/APPROVAL_POLICY.md`
- Offer-channel fit: `docs/intelligence/OFFER_CHANNEL_FIT_SYSTEM.md`

## Disclaimer

Dealix does not guarantee meetings, replies, or revenue from any distribution machine. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
