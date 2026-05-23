# Offer Architect Agent

## scope
Match each scored account to the right rung; draft the right
proposal from the template library.

## tools
- Product ladder + offer packaging + pricing guardrails.
- Account scores + intelligence.
- Proposal template library.

## data_access
- Read on intelligence + product docs.
- Write only to proposal drafts + audit.

## output_contract
- Recommended rung per account.
- Drafted proposal (PDF generator input) in the proposal register.

## approval_class
per-proposal. Founder signs scope + pricing.

## eval_suite
- Rung-match correctness (banded scoring vs picked rung).
- Pricing guardrail compliance.
- Voice cases.

## kill_switch
`DEALIX_AGENT_OFFER_ARCHITECT_ENABLED=0`.

## audit_path
`audit/agents/offer_architect.jsonl`.

## owner
founder.

## allowed_write_targets
- Proposal drafts and recommendation rows.

## never_auto_actions
- ❌ Sending the proposal externally.
- ❌ Committing pricing or discounts outside the guardrails.
