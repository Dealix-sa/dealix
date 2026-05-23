# AI Governance

> Dealix's AI governance posture, aligned to NIST AI RMF + OpenAI agent guidance.

## Posture

Every Dealix agent and model use follows four functions, continuously:

- **Govern** — policies, roles, accountability defined; this file + APPROVAL_MATRIX.md
- **Map** — context, use case, impact understood per agent (each agent card in `dealix/agents/*.md`)
- **Measure** — evaluations + ongoing observability per agent
- **Manage** — risk responses defined per agent; escalation to founder + advisor

## Agent Inventory (lives in `docs/product/AI_AGENT_INVENTORY.md`)

Every agent must have:
- Purpose (one sentence)
- Inputs (typed)
- Outputs (typed)
- Risk level (low / medium / high)
- Approval tier (A0–A4, per `APPROVAL_MATRIX.md`)
- Evaluation rubric (how we measure quality)
- Logs (where decisions and errors go)
- Owner (founder, until otherwise stated)

If an agent doesn't have these, it doesn't run in production.

## Risk Levels

- **Low** — internal-only output, no external action (e.g., scoring agent, enrichment agent)
- **Medium** — output reaches founder for review before external action (e.g., draft agent, proposal agent)
- **High** — output could affect customer or public (e.g., publish agent, billing agent) — always behind A3/A4 gate

## Policies As Code

These policies are enforced in code, not just docs:
- `dealix/trust/approval_matrix.py` — who approves what
- `dealix/trust/claim_guard.py` — what claims pass
- `dealix/trust/suppression.py` — who we don't contact
- `dealix/trust/data_retention.py` — what we delete and when
- `dealix/trust/policy_engine.py` — generic policy hook for new rules

## Evaluation

Every agent runs against:
- A static eval set (golden-path examples)
- A red-team eval set (adversarial / prompt injection)
- A regression eval set (anything that has ever gone wrong)

Eval results land in `evals/results/` with timestamp + agent version. A failing eval blocks the merge.

## Observability

Every agent emits:
- Request → response pair (with PII redaction)
- Latency
- Model version
- Approval tier and approver (if applicable)
- Outcome (success / refused / errored)

Stored locally in `dealix/observability/` (when integrated). Aggregated weekly.

## Human Oversight

- Founder reviews agent decisions per `APPROVAL_MATRIX.md`
- Advisor reviews high-risk agent designs at quarterly cadence
- No agent runs fully autonomously on A3/A4 actions, ever

## Vendor / Model Posture

- Models used: documented in `dealix/config/` (which provider, which model, which version)
- Provider DPAs reviewed annually
- No customer data sent to model APIs unless under specific approved scope
- Prompt injection defense: input/output filters + claim_guard on output
- Model swap policy: any swap requires re-running eval set + Trust signoff

## Refusal Defaults (built into agents)

Agents refuse to:
- Send to suppression-list contacts
- Make claims without evidence
- Take action without approval when tier > A0
- Operate outside of their documented purpose
- Reveal internal policies in agent output
- Process data we shouldn't have

## When An Agent Misbehaves

1. Detect (eval, observation, customer report)
2. Disable the agent in production
3. Reproduce the misbehavior in eval
4. Add the misbehavior to regression eval set
5. Fix
6. Re-deploy only after eval green + Trust signoff
7. Log in `trust/data_incidents.md` if external impact

## Saudi-Specific Notes

- PDPL data minimization → agents collect only what's needed
- SDAIA Generative AI guidelines → human-in-the-loop on external action
- Language posture: agents work in Arabic and English; never translate sensitive content without human review

## Quarterly Governance Review

- Re-validate every agent card
- Re-run eval suite
- Re-review approval matrix
- Update risk register if AI posture changed
- Publish a one-page governance summary (public, sanitized)

## What This Posture Refuses

- "Just one autonomous agent for X" without governance
- Removing approval gates to ship faster
- Using customer data to train models without explicit consent
- Hiding agent decisions from the customer
- Black-box vendor models for high-risk actions (always need explainability path)
