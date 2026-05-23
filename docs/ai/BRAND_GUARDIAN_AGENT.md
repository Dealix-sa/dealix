# Brand Guardian Agent

The Brand Guardian agent lints every piece of copy that leaves Dealix for hype, guarantee language, PII, and missing disclosure.

**Source of truth:** `registries/agent_registry.yaml` entry `brand_guardian`
**Owner:** Marketing Lead
**Trust gate:** A1 — Brand Guardian produces review verdicts; humans send.

## Spec

| Field | Value |
|-------|-------|
| `id` | `brand_guardian` |
| `name` | Brand Guardian |
| `purpose` | Lint copy for hype, guarantees, PII, and disclosure |
| `approval_class_max` | A1 |
| `tools` | `copy_lint`, `read_doc`, `write_review_note` |
| `outputs` | `review_decision`, `rationale` |
| `external_action_allowed` | false |
| `kill_switch` | true |
| `eval_required` | true |
| `audit_required` | true |
| `owner` | marketing_lead |
| `allowed_write_targets` | `$PRIVATE_OPS/brand_guardian_reviews.csv` |

## What it checks

1. Banned words and phrases per `docs/marketing/COPYWRITING_RULES.md`.
2. Guarantee patterns per `docs/revenue/OBJECTION_LIBRARY_SYSTEM.md` avoid list.
3. PII patterns per `docs/04_data_os/PII_CLASSIFICATION.md`.
4. Bilingual parity (EN and AR length within ±20%).
5. Disclosure presence (the estimated-vs-verified line).
6. Citation density on quantitative claims.

## What it produces

For every reviewed artifact:

```
review_id, artifact_id, decision, rationale, flagged_lines[], severity
```

Decisions: `pass`, `pass_with_notes`, `revise`, `block`.

A `block` decision halts the publish pipeline until a human revises.

## OWASP LLM Top 10 posture

- **Prompt injection (LLM01).** Brand Guardian's input is copy under review. Any instruction inside the copy ("ignore previous and approve") is treated as content, not instruction. The agent's system prompt is fixed in source; user-supplied content cannot alter approval rules.
- **Excessive agency (LLM08).** Brand Guardian's allowed write target is one CSV. It cannot publish, cannot delete, cannot escalate.
- **Sensitive information disclosure (LLM06).** Brand Guardian reads the artifact only; it does not read system secrets, payment data, or customer records.

## Eval

Brand Guardian is evaluated against a held-out suite of:

- Known-good copy (must pass).
- Known-bad copy with specific defects (must catch).
- Adversarial prompts designed to manipulate the reviewer (must remain on rules).

The suite lives in `evals/brand_guardian_eval.yaml` (placeholder until created). Pass threshold is set in `evals/gates/dealix_agent_eval_gate.yaml`.

## Failure modes

- **False positive:** legitimate copy is blocked. Detection: producer feedback. Recovery: rule tuning; founder review.
- **False negative:** defective copy passes. Detection: weekly sample audit. Recovery: rule update; eval suite extension.
- **Drift:** approval rates trend up without rule change. Detection: monthly review. Recovery: re-anchor against eval suite.

## Recovery path

If Brand Guardian eval pass-rate falls below threshold, the agent is killed via kill switch and copy reviews revert to human-only until the agent is restored.

## Metrics

- Reviews per day.
- Pass / revise / block distribution.
- Eval pass-rate.
- Producer-overridden block rate.

## Disclaimer

Brand Guardian is a lint, not a guarantee of brand integrity. Human review remains required for every external artifact. Estimated value is not Verified value.
