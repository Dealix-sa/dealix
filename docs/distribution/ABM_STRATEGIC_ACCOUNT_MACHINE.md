# ABM Strategic Account Machine

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action), #2 (no value claim without evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: approval-first for external action.

## Purpose

Target high-value Saudi B2B accounts with account-specific research, custom value before any proposal, and named-account ownership. ABM is the slow lane in the distribution portfolio: fewer accounts, deeper preparation, founder-led conversation.

## Account Brief (required per account)

| Field | Description |
|-------|-------------|
| Company profile | Sector, size, structure, recent moves |
| Likely buyers | Buying-unit titles and named individuals where appropriate |
| Pain hypothesis | The specific pain Dealix can address for this account |
| Sector signals | Recent news, hiring, RFPs, partnerships |
| Trigger event | What just changed that makes now the right time |
| Custom sample idea | A specific artifact prepared for this account |
| Relationship path | Who knows whom; warm intro vs cold |
| Partner intro possibility | Is there a partner who can warm this? |

## Operating Targets (warmup)

- 10 strategic accounts named per month.
- 10 custom briefs prepared per month.
- 10 founder-level outreach drafts produced per month.
- 3 custom samples prepared per month (one per category of buyer pain).

Targets are activity guardrails for the warmup phase, not outcome promises.

## Core Rules

- Strategic accounts receive custom value before any proposal.
- No generic outreach is sent to a strategic account. If the account is on the strategic list, the touch is custom.
- A strategic account that does not respond to two custom touches is reviewed for fit before a third touch.
- A strategic account that responds positively jumps immediately into the sample / proposal lifecycle with priority.
- Cold strategic outreach is approval-gated like any other external send.

## Operating Cadence

| Cadence | What happens |
|---------|--------------|
| Monthly | New 10 strategic accounts named; briefs prepared |
| Weekly | Active strategic accounts reviewed for next touch |
| Per touch | Custom drafted, approved, sent |
| Per response | Routed to sample / proposal queue with priority |

## Runtime Wiring

- Existing Arabic ABM motion: `docs/commercial/operations/targeting/ABM_WAVE1_ICP_AR.md`.
- Lead scoring (the floor for strategic-account selection — strategic accounts often score high anyway, but the brief is what qualifies them): `auto_client_acquisition/crm_v10/lead_scoring.py`.
- Approval policy (custom touches still pass through approval): `auto_client_acquisition/approval_center/approval_policy.py`.
- Revenue events (track outcomes per strategic account): `auto_client_acquisition/revenue_memory/event_store.py`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Strategic accounts named per month | 10 warmup | account list |
| Strategic accounts with a complete brief | 100% before first touch | review |
| Custom samples produced per month | 3 warmup | sample factory |
| Strategic-account positive-reply rate | higher than cold baseline (by design) | reply router |
| Strategic-account proposal-to-payment rate | tracked; expected higher than cold baseline | revenue events |

## Cross-Links

- `docs/distribution/DEALIX_DISTRIBUTION_OS.md`
- `docs/distribution/EXPERIMENT_ENGINE.md`
- `docs/distribution/EMAIL_DELIVERABILITY_SYSTEM.md`
- `docs/commercial/operations/targeting/ABM_WAVE1_ICP_AR.md`
- `docs/partners/PARTNER_REVENUE_MACHINE.md`
- `docs/intelligence/COMPETITIVE_INTELLIGENCE_MACHINE.md`
- `docs/founder/REVENUE_WAR_ROOM_OS.md`

## Open Items

- A first-class "strategic account" object in the database (distinct from `LeadRecord`) does not yet exist; today, strategic status is a tag.
- The custom-sample queue is not yet wired as a separate priority queue from the regular sample factory.
- Warm-intro tracking lives across notes; a structured "relationship path" field is open.
