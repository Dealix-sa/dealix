# Offer Architect Agent

The Offer Architect agent helps the founder design new packages and revise existing ones. It compares against the published ladder, checks margin against unit economics, and drafts inclusions and exclusions. It does not publish offers.

**Source of truth:** `registries/agent_registry.yaml` entry `offer_architect`
**Owner:** Founder
**Trust gate:** A2 — every package activation is a founder decision.

## Spec

| Field | Value |
|-------|-------|
| `id` | `offer_architect` |
| `name` | Offer Architect |
| `purpose` | Design and revise packages against ladder and unit economics |
| `approval_class_max` | A1 |
| `tools` | `read_ladder`, `read_unit_economics`, `read_pricing_guardrails`, `draft_package`, `write_proposal` |
| `outputs` | `package_draft`, `pricing_proposal` |
| `external_action_allowed` | false |
| `kill_switch` | true |
| `eval_required` | true |
| `audit_required` | true |
| `owner` | founder |
| `allowed_write_targets` | `$PRIVATE_OPS/package_drafts/`, `$PRIVATE_OPS/pricing_drafts.csv` |

## What it does

1. Reads the current ladder (`docs/product/DEALIX_PRODUCT_LADDER.md`) and packages (`docs/product/OFFER_PACKAGING.md`).
2. Reads unit economics (`docs/finance/AI_UNIT_ECONOMICS_SYSTEM.md`) to compute floor pricing.
3. Reads pricing guardrails (`docs/product/PRICING_GUARDRAILS.md`) to compute custom-pricing bands.
4. Drafts a package with `objective`, `inclusions`, `exclusions`, `deliverables`, `timeline_weeks`, `price_sar`, `payment_terms`, `eligibility`, `proof_anchors`.
5. Submits the draft to the founder for review.

## OWASP LLM Top 10 posture

- **Excessive agency (LLM08).** The agent cannot publish a package to the public site, cannot issue a proposal, cannot change reference prices.
- **Prompt injection (LLM01).** The agent is fed structured data (CSV) and policy docs. It does not accept untrusted user prompts at runtime.
- **Insecure output handling (LLM02).** Drafts are markdown only; activation is a manual step.

## Eval

The eval suite tests:

- Floor-pricing math correctness.
- Exclusion-list length (at least as long as inclusion list).
- Disclosure-line presence.
- Hype / guarantee absence.
- Ladder consistency (no overlap with adjacent rungs).

## Failure modes

- **Margin breach:** drafted price below floor. Detection: pricing engine. Recovery: regenerate with corrected floor.
- **Sponge package:** inclusions outpace exclusions. Detection: structural lint. Recovery: extend exclusions or narrow inclusions.
- **Rung confusion:** package overlaps an adjacent rung. Detection: ladder comparison. Recovery: relocate or merge.

## Recovery path

If the agent drafts margin-unsafe packages, the founder kills it and packages are designed manually with finance review.

## Metrics

- Drafts produced per quarter.
- Drafts accepted on first revision.
- Time from request to founder-ready draft.
- Margin-error rate (target: 0).

## Disclaimer

Offer Architect is a drafting tool. Activation is a founder decision. Dealix does not guarantee revenue from any offer. Estimated value is not Verified value.
