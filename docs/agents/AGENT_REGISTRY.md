# Agent Registry

> Single source of truth for which agents exist, what they do, and what
> they are allowed to do.

## Registry

| Agent | Purpose | Input | Output | Risk | Approval | Eval Suite |
|---|---|---|---|---|---|---|
| Founder Brief Agent | Daily CEO summary | metrics, logs, pipeline | DAILY_COMMAND_BRIEF draft | Medium | A1 | accuracy, usefulness |
| Lead Finder Agent | Find P0 leads from public sources | ICP rubric, sector filter | Lead candidates | Low | A0 | relevance |
| Scoring Agent | Score leads A/B/C | Lead data, ICP rubric | Score + reason | Low | A0 | precision |
| Message Agent | Draft outreach | Lead + offer | Message draft | Medium | A1 / A2 (claims) | quality, hallucination |
| Proposal Agent | Draft proposals from call notes | Call notes, offer template | Proposal draft | High | A2 | scope accuracy |
| Trust Guard Agent | Flag risky outputs before send | Any drafted artifact | Risk flags | High | A2 / A3 | recall |
| Learning Agent | Analyze results, suggest experiments | Logs, metrics | Recommendations | Medium | A1 | usefulness |
| Delivery QA Agent | Pre-handoff QA on deliverables | Deliverable + checklist | QA report | Medium | A1 | precision |

## Registry Rules

1. A new agent is registered before it is deployed. No "shadow agents".
2. Each agent has a versioned prompt, model, and guardrail set.
3. Each agent has a measurable eval suite in `evals/`.
4. Each agent maps to a specific approval level per `docs/trust/APPROVAL_MATRIX.md`.

## Companion Files

- `AGENT_EVALUATION.md` — how we evaluate agents.
- `AGENT_PERMISSIONS.md` — what each agent can read and write.
- `AGENT_HANDOFFS.md` — how agents pass work to each other and to humans.
- `AGENT_LOGGING.md` — what every agent must log.
