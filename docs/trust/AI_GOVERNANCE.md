# AI Governance

> Inspired by NIST AI RMF (Govern, Map, Measure, Manage) and applied to a
> founder-led, Saudi-native revenue operating system.

## Govern

- Founder is the accountable executive.
- Trust OS is the cross-cutting governance layer; no workflow ships without it.
- All workflows are risk-classified before deployment
  (see `WORKFLOW_RISK_CLASSIFICATION.md`).

## Map

We map every AI-touched workflow to:
- Inputs and data sources.
- Outputs and downstream consumers.
- Human reviewer (if any).
- Risk class (Low / Medium / High / Critical).
- Approval level (A0–A3).

The map lives in `docs/agents/AGENT_REGISTRY.md`.

## Measure

We measure agent and workflow quality on:
- Accuracy on a held-out evaluation set.
- Hallucination rate (false claims).
- Useful-output rate (founder-rated 1–5).
- Risk-detection rate (Trust Guard recall).
- Approval correctness (no A2/A3 bypass).

Eval cadence and methodology: `docs/agents/AGENT_EVALUATION.md`.

## Manage

When measurement reveals a drop:
- Pause the workflow if risk class is High or Critical.
- Lower the automation level (e.g., L3 → L1) for Medium risk.
- Always file a learning entry in `docs/learning/EXPERIMENT_LOG.md`.

## Out of Scope

Pretending Dealix holds AI compliance certifications it does not hold.
Marketing language that implies regulatory approval. See `NO_OVERCLAIM_POLICY.md`.

## Reference

- NIST AI Risk Management Framework (AI RMF 1.0).
- Dealix Approval Matrix.
- Dealix Workflow Risk Classification.
