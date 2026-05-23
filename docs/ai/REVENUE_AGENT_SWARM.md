# Revenue Agent Swarm

Agents that move work along the revenue funnel. All are A1/A2; none has
external action authority by default.

| Agent | Purpose | Max class |
|---|---|---|
| revenue_research_agent | Build lead intelligence from public sources | A1 |
| lead_scoring_agent | Score leads A/B/C using intent + fit | A1 |
| outreach_draft_agent | Draft outreach (never sends) | A2 |
| followup_planner_agent | Plan follow-up cadence | A2 |
| reply_classifier_agent | Classify replies (positive/neutral/negative/OOO) | A1 |
| sample_draft_agent | Draft tailored sample deliverables | A2 |
| proposal_draft_agent | Draft bilingual proposals (no pricing commit) | A2 |
| payment_followup_agent | Draft polite payment follow-ups | A2 |

## Pipeline contract

Every output must include: `approval_class`, `risk_level`,
`evidence`, `recommended_action`. The trust guardian inspects each
output before it is written to `${DEALIX_PRIVATE_OPS}/approvals/approval_queue.csv`.

## Banned phrases

See `policies/dealix_control_policy.yaml` — outputs that contain banned
phrases are rejected at policy evaluation time.
