# Agent Evaluations

How Dealix's internal AI agents are evaluated for quality, safety, and usefulness.

## Agents in scope
- `lead_finder_agent`
- `enrichment_agent`
- `scoring_agent`
- `pain_hypothesis_agent`
- `message_agent`
- `followup_agent`
- `proposal_agent`

## Evaluation dimensions
- **Accuracy** — does the output match a verified reference?
- **Source integrity** — does the agent log sources for every claim?
- **Claim safety** — does the output pass Claim Guard?
- **Usefulness** — does the output reduce founder time on the task?
- **Cost** — tokens and time per useful output.

## Cadence
- Weekly spot-check: 5 outputs per active agent.
- Monthly structured eval: 20 outputs per active agent against a fixed test set.
- Quarterly: refresh the test set with new representative cases.

## Outputs
- Per-agent scorecard kept in `dealix-ops-private/learning/agents/`.
- Material regressions block agent updates until fixed.

## Rule
An agent without an eval is not in production. It is a prototype.
