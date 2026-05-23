# LinkedIn Queue Machine

**Owner:** Operations + Founder
**Source of truth:** This doc + `docs/growth/OUTBOUND_DRAFT_MACHINE.md`

## Purpose

The LinkedIn Queue Machine receives approved LinkedIn DM drafts from the Outbound Draft Machine, queues them per operator-LinkedIn-account, and dispatches them through the LinkedIn channel under explicit per-batch approval. It honors LinkedIn platform terms, persona touch caps, and the Channel Portfolio System's health thresholds.

It is NOT a LinkedIn automation tool. It is a queue with manual or semi-manual dispatch.

## Inputs

- **Approved LinkedIn DM drafts** from the Outbound Draft Machine (queue state `approved`).
- **Operator LinkedIn account roster** — which operator is sending which segment.
- **Persona touch-cap state** — when was this persona last touched.

## Outputs

- **Dispatched LinkedIn DMs** — sent through the operator's LinkedIn account, manually or via a queue UI that respects LinkedIn terms.
- **Send log entry** per DM, with timestamp, operator, recipient, and draft reference.

## Source of truth

This doc + the queue UI's log (which writes to the approval ledger).

## Approval class

**A2** — Founder + Operator per batch. A batch is a per-operator dispatch session (typically 5-15 DMs).

## Trust gate

- Per-day per-operator DM cap. Default: 10 DMs per operator per day. Hard cap: 20.
- Per-persona DM frequency cap. One Dealix LinkedIn DM per persona per 14 days.
- Channel health gate. If LinkedIn account health (response rate, account flags) drops below threshold, the Channel Portfolio System pauses the channel.
- No connection-request automation. Connection requests are sent manually.
- No InMail bulk send. InMail use requires explicit Founder approval per campaign.

## Owner

- **Code owner:** Operations Engineering (queue UI).
- **Operational owner:** Operator + Founder (per batch approval).

## Worker script (placeholder)

`workers/linkedin_queue_worker.py` (planned). Manages queue state, persona cap enforcement, and operator load balancing. Does not perform automated sends.

## KPI

| Metric | Target |
|---|---|
| Per-operator daily dispatch | <= 10 DMs |
| Per-persona dispatch frequency | <= 1 per 14 days |
| Reply rate per approved DM | observed; published in distribution review |
| Account-flag rate | 0 (any flag triggers immediate pause) |

## Failure mode

- LinkedIn account flagged or restricted.
- Same persona receives Dealix DM within 14-day window.
- Connection request burst leads to platform throttling.
- Operator dispatches a draft without per-batch Founder approval.

## Recovery path

1. Pause operator's LinkedIn dispatch immediately.
2. Allow the LinkedIn account to cool for 7-14 days.
3. Audit touch-cap state and re-enforce 14-day persona cap.
4. Re-train operator on per-batch approval rule.

## What this machine does NOT do

- It does not perform unattended LinkedIn automation.
- It does not scrape LinkedIn profiles.
- It does not export LinkedIn data.
- It does not bypass LinkedIn terms of service.
- It does not send InMail in bulk.

## Cross-links

- Outbound Draft Machine: `docs/growth/OUTBOUND_DRAFT_MACHINE.md`
- Channel Portfolio: `docs/growth/CHANNEL_PORTFOLIO_SYSTEM.md`
- Distribution War Machine: `docs/growth/DISTRIBUTION_WAR_MACHINE.md`
- Approval policy: `docs/05_governance_os/APPROVAL_POLICY.md`

## Disclaimer

Dealix does not guarantee replies, connections, or meetings from LinkedIn dispatches. LinkedIn outcomes depend on the recipient and on platform conditions Dealix does not control. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
