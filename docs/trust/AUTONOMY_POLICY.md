# Autonomy Policy

The five-level autonomy ladder that decides how much an AI agent can do on its own, vs. how much must be done with the founder in the loop.

## Purpose
Make the boundary between AI autonomy and founder control written, explicit, and enforceable per action. The ladder is the contract that allows the founder to scale operating throughput safely.

## Owner
Sami (Founder).

## Review Cadence
Monthly, against the approval log and friction log.

## Inputs
- The proposed action from an agent.
- The action's classification under the Approval Matrix.
- Historical performance of the agent on similar actions.
- The current operating posture (launching, scaling, recovering).

## Outputs
- An autonomy-level assignment per action class.
- The default autonomy level for every agent in the agent registry.
- A list of autonomy promotions or demotions per quarter.

## Rules
- New agents start at L0 or L1 unless promoted with evidence.
- Promotion to L3 requires at least 10 logged successful runs at L2.
- L4 actions are not permitted to any agent. Period.
- Demotion is automatic on a single doctrine violation.
- Autonomy level is per action class, not per agent globally.

## Metrics
- Number of agents at each autonomy level.
- Promotions and demotions per quarter.
- Doctrine violations per autonomy level.
- Founder time saved per agent per week.

## Evidence
- Agent registry in `docs/agents/REGISTRY.md`.
- Promotion / demotion log entries in `trust/approval_log.csv` (private ops).
- Friction log for autonomy-related incidents.

## The Five Levels

### L0 Manual
The founder does the entire action. AI does not act, does not draft. Used for first-of-kind actions.

### L1 Assisted
AI prepares a draft. Founder edits and sends. Every artifact has founder signature.

### L2 Semi-Auto
AI sends within a pre-approved batch or sequence. Founder approves the batch, not each item. Logged per action.

### L3 Auto
AI acts within a defined scope and reports outcomes. Founder reviews the log, not each action. Used for internal compilation, dashboards, research.

### L4 Prohibited
Reserved class. No agent runs at L4. Any attempt is blocked and alerted.

## Default Autonomy per Action Class

| Action Class | Default Autonomy | Promotion Threshold |
|---|---|---|
| Internal research compilation | L3 | n/a |
| Pipeline tracker enrichment | L3 | n/a |
| Daily Command Brief generation | L2 | 30 successful runs |
| Outbound DMs to known leads | L1 | Never auto-promote |
| Outbound DMs to cold contacts | L0 | Never promote — qualification first |
| Proposals under 5,000 SAR | L1 | Never auto-promote |
| Proposals 5,000–25,000 SAR | L0 | Never promote |
| Customer-facing artifacts | L1 | Never auto-promote |
| Payments / refunds | L0 | Never promote |
| Public statements | L0 | Never promote |
| Cold scraping | L4 Prohibited | n/a |
| Mass automated outreach | L4 Prohibited | n/a |

## Last Reviewed
2026-05-23
