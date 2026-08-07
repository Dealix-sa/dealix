# V14 Agent Operations

## Design principles
1. **Deterministic by default.** No external call required to produce output.
2. **LLM-assist is opt-in.** `--use-ai` flag + provider env var.
3. **Fail-safe.** Provider failure → deterministic fallback with metadata tagging.
4. **Auditable.** Every call records provider, model, prompt version, review_status.
5. **Banned-claim filtered.** Pre-call safety check refuses unsafe prompts.

## Modules
- `scripts/lib/ai_router.py` — the routing entry point.
- `scripts/lib/ai_providers.py` — provider registry.
- `scripts/lib/prompt_registry.py` — versioned prompts.
- `scripts/lib/ai_safety.py` — pre-call refusal checks.
- `scripts/lib/ai_memory.py` — append-only audit log.
- `scripts/lib/ai_eval.py` — output evals.

## Task classes
lead_scoring_explanation, weakness_hypothesis, outreach_draft, proposal_section, objection_response, proof_report_summary, client_status_summary, sales_call_summary, compliance_review, translation_ar_en, market_research_summary.

## Activation gates (for live LLM calls)
- `AI_PROVIDER_DEFAULT` env var set.
- `AI_MODE_DEMO` env var explicitly set to `false`.
- Customer SOW allows LLM-assist.
- Founder approves the activation PR.

## Out of scope
- Streaming completions.
- Tool-use / function calling beyond text generation.
- Multi-agent autonomous loops.
