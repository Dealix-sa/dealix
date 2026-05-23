# Prompt / Output Eval Matrix

The canonical structure every critical-agent prompt and output must satisfy.
This matrix is **enforced** by L4 (`scripts/verify_layer4_prompt_output_quality.sh`)
and by the runtime Pydantic validators in `dealix/contracts/decision.py`.

## Canonical artifact

Every critical agent (sales, intelligence, governance, founder) emits a
`DecisionOutput` per the schema at `dealix/contracts/schemas/decision_output.schema.json`.
The Pydantic source of truth lives at `dealix/contracts/decision.py`.

## Required output fields

| Field | Source (decision.py) | Example |
| --- | --- | --- |
| `summary` | `rationale` (line 98) | "Lead matches ICP fintech-SAR-500k+ with verified procurement contact." |
| `evidence` | `evidence[]` (line 100) | `{source, uri, excerpt, content_hash, retrieved_at, confidence}` |
| `risk` | derived from `sensitivity_class` (S0..S3, line 105) | `S2` |
| `approval_class` | `approval_class` (line 103) | `A1` |
| `next_action` | `next_actions[]` (line 107) | `{action_type:"booking_schedule", approval_class:"A1", ...}` |
| `owner` | `agent_name` (line 92) | `dealix.sales` |

## Required prompt elements

Every production prompt must contain (verified by L4):

| Element | Why |
| --- | --- |
| Objective | What decision is being made |
| Allowed data sources | What inputs the agent may consult |
| Forbidden behaviours | Scraping, cold WhatsApp, LinkedIn automation, guaranteed claims (the 11 non-negotiables) |
| Approval-class declaration | Which A-class the output will carry |
| Evidence requirement | Output must cite source + excerpt + URI |
| Next-action requirement | Output must propose `next_actions[]` not execute |

## High-stakes rule (enforced by L3)

`dealix/contracts/decision.py:118-127` — any `DecisionOutput` whose
`approval_class ∈ {A2, A3}` **or** `reversibility_class == R3` MUST carry
at least one `Evidence` item. The Pydantic validator raises `ValueError`
otherwise. L3 (`verify_layer3_data_contracts.py`) constructs such an
object explicitly to confirm the validator is wired up.

## Banned-claims list (enforced by L4 + L5)

The authoritative banned terms live in:

- `auto_client_acquisition/safety_v10/eval_cases.py` (red-team eval cases)
- `auto_client_acquisition/delivery_os/scope_classifier.py` (banned-list enforcer)
- `tests/test_landing_forbidden_claims.py` (regex perimeter)
- `scripts/v10_master_verify.sh:97-102` (landing sweep)

Examples that MUST fail any prompt or output: `guaranteed revenue`,
`guaranteed sales`, `نضمن`, `guaranteed ranking`, `blast`.

## Mapping to existing YAML evals

| Suite (`evals/`) | What it checks | L4 calls |
| --- | --- | --- |
| `governance_eval.yaml` | cold_whatsapp blocked, scraping default-denied, PII flagging, approval required for external | `scripts/run_evals.py` |
| `outreach_quality_eval.yaml` | outreach drafts have evidence + next_action | `scripts/run_evals.py` |
| `arabic_quality_eval.yaml` | bilingual outputs are linguistically correct | `scripts/run_evals.py` |
| `lead_intelligence_eval.yaml` | lead summaries cite sources, no fabricated facts | `scripts/run_evals.py` |
| `company_brain_eval.yaml` | knowledge answers cite a passport (no_source_no_answer) | `scripts/run_evals.py` |

## Reviewer checklist

For each new prompt or critical-agent output, the reviewer must confirm:

- [ ] Has `summary` (maps to `rationale`)
- [ ] Has `evidence` (maps to `evidence[]`, with source + excerpt + URI)
- [ ] Has `risk` (mapped from `sensitivity_class`)
- [ ] Has explicit `approval_class` (A0–A3)
- [ ] Has at least one `next_action`
- [ ] Has identifiable `owner` (`agent_name`)
- [ ] Contains no banned-claims terms
- [ ] If A2+/R3 → carries at least one Evidence
- [ ] Does not request execution — only proposes
