# Prompt × Output × Eval Matrix

This matrix is the systematic view of which prompts produce which outputs and which evals certify them. It is the map every engineer reads before changing a prompt.

**Source of truth:** `$PRIVATE_OPS/prompt_eval_matrix.csv` (mirror of `evals/` + `docs/06_llm_gateway/PROMPT_REGISTRY.md`)
**Owner:** Engineering Lead
**Trust gate:** A1 — matrix updates reviewed weekly.

## Matrix dimensions

| Dimension | Source |
|-----------|--------|
| Prompt | `docs/06_llm_gateway/PROMPT_REGISTRY.md` |
| Output schema | `docs/06_llm_gateway/SCHEMA_VALIDATION.md` |
| Eval suite | `evals/*.yaml` |
| Pass criteria | `evals/gates/dealix_agent_eval_gate.yaml` |
| Owner agent | `registries/agent_registry.yaml` |

## Example matrix (excerpt)

| Prompt id | Output schema | Eval suite | Pass criteria | Agent |
|-----------|--------------|------------|---------------|-------|
| `copy.lint.v3` | `review_decision.v1` | `brand_guardian_eval_v1` | 0.97 | brand_guardian |
| `copy.lint.v3` | `review_decision.v1` | `brand_guardian_red_team_v1` | 1.00 | brand_guardian |
| `growth.analyse.v2` | `growth_analysis.v1` | `growth_strategist_eval_v1` | 0.90 | growth_strategist |
| `growth.analyse.v2` | `experiment_proposal.v1` | `growth_strategist_eval_v1` | 0.90 | growth_strategist |
| `content.brief.v4` | `content_brief.v2` | `content_strategist_eval_v1` | 0.92 | content_strategist |
| `package.draft.v1` | `package_draft.v1` | `offer_architect_eval_v1` | 0.95 | offer_architect |
| `perf.read.v3` | `weekly_performance_read.v2` | `performance_analyst_eval_v1` | 0.95 | performance_analyst |
| `copilot.brief.v2` | `daily_briefing.v1` | `ceo_copilot_eval_v1` | 0.95 | ceo_copilot |
| `policy.check.v2` | `policy_decision.v1` | `trust_guardian_eval_v1` | 0.98 | trust_guardian |
| `policy.check.v2` | `policy_decision.v1` | `trust_guardian_red_team_v1` | 1.00 | trust_guardian |

## What a row means

Each row says: "If you change this prompt or this schema, these evals must re-pass at this threshold for this agent." The matrix prevents silent prompt drift.

## Change discipline

A prompt change PR must include:

1. Prompt diff with rationale.
2. Schema diff (if any).
3. Eval suite update or expansion.
4. Evidence the existing suite still passes.

A schema change is a breaking change unless backwards compatibility is proven; consumers must be updated in the same PR.

## Failure modes

- **Orphan prompt:** a prompt is registered but no eval covers it. Detection: weekly diff. Recovery: write eval or retire prompt.
- **Orphan suite:** a suite exists for a prompt that no longer ships. Detection: weekly diff. Recovery: archive suite.
- **Threshold inconsistency:** the matrix says 0.95 but the gate file says 0.90. Detection: nightly check. Recovery: gate file is canonical; matrix updated.

## Recovery path

If the matrix and the source registries diverge, the founder freezes prompt changes until alignment.

## Metrics

- Matrix row count.
- Orphan-prompt count (target: 0).
- Orphan-suite count (target: 0).
- Threshold-inconsistency count (target: 0).

## Disclaimer

The matrix is a coverage map. It does not guarantee absence of defects. Estimated value is not Verified value.
