# Content Strategist Agent

The Content Strategist agent turns a founder thought, sector data, or factory observation into a structured content brief. It does not write final copy; it produces the brief that the Distribution Operator drafts from.

**Source of truth:** `registries/agent_registry.yaml` entry `content_strategist`
**Owner:** Marketing Lead
**Trust gate:** A1 — briefs are reviewed before they feed downstream drafting.

## Spec

| Field | Value |
|-------|-------|
| `id` | `content_strategist` |
| `name` | Content Strategist |
| `purpose` | Produce structured content briefs from founder input and operational data |
| `approval_class_max` | A1 |
| `tools` | `read_thoughts`, `read_factory_state`, `read_sector_data`, `write_brief` |
| `outputs` | `content_brief` |
| `external_action_allowed` | false |
| `kill_switch` | true |
| `eval_required` | true |
| `audit_required` | true |
| `owner` | marketing_lead |
| `allowed_write_targets` | `$PRIVATE_OPS/briefs/` |

## Brief schema

Each brief is a markdown document with these sections:

1. Format (post, carousel, long-form, sector excerpt).
2. Surface (LinkedIn, newsletter, site).
3. Audience persona.
4. Promise (one sentence).
5. Three supporting points with citations.
6. Avoid list (specific banned framings for this brief).
7. CTA (single, named action).
8. Disclosure requirement (yes / no, with reason).

## Inputs

- Founder thoughts queue (`$PRIVATE_OPS/founder_thoughts/`).
- Revenue Factory state (`$PRIVATE_OPS/revenue_factory_state.csv`).
- Sector data (`$PRIVATE_OPS/sector_data/`).
- Eval results (`$PRIVATE_OPS/eval_results/`).
- Performance signal (Growth Strategist recommendations).

## OWASP LLM Top 10 posture

- **Prompt injection (LLM01).** Founder thoughts may contain quoted client text. The agent treats quoted text as content under review, not as instructions.
- **Excessive agency (LLM08).** The agent cannot post, cannot send, cannot publish. It writes one type of artifact to one directory.
- **Sensitive information disclosure (LLM06).** Briefs never include client-identifying details unless consent is on file.

## Eval

The agent is evaluated on:

- Brief structure compliance.
- Citation presence on every supporting point.
- Avoid-list specificity (briefs that just say "no hype" without naming the risk are penalised).
- Bilingual readiness (the brief notes any AR-specific framing needs).

## Failure modes

- **Generic brief:** the brief reads like a template. Detection: human review. Recovery: prompt enrichment with sector and persona detail.
- **Citation omission:** a supporting point lacks a source. Detection: lint. Recovery: revise.
- **Avoid-list omission:** the brief does not name banned framings. Detection: lint. Recovery: extend prompt.

## Recovery path

If brief quality is consistently weak, the agent is killed and briefs are written by Marketing Lead until the agent is re-certified.

## Metrics

- Briefs produced per week.
- Briefs accepted on first draft.
- Downstream artifact win rate by brief (estimated).
- Average citations per brief.

## Disclaimer

Briefs are scaffolding. Draft and publish remain human decisions. Estimated value is not Verified value.
