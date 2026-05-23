# Proof-to-Demand Machine

## purpose
Take every closed deal and convert it — with consent — into the
outbound, content, and proposal patterns that win the next ten deals.

## inputs
- `proof/proof_pack_registry.csv` (consented case studies).
- Look-alike accounts identified by sector + size + persona.
- Existing outbound and proposal templates.

## outputs
`distribution/proof_to_demand.csv`:
```
proof_id,lookalike_account_id,channel_hint,draft_id,
content_id,proposal_template_id,expected_resonance,
fallback_share,created_at,status
```

## source
- Proof pack registry (consent-required).
- Account scoring data.

## approval_class
per-batch — a batch is approved as a campaign.

## trust_gate
- Proof can only be referenced when the originating customer has
  granted explicit re-use consent.
- Look-alike outreach drafts go through the standard per-message
  approval flow.

## owner
content_strategist + distribution_operator → founder.

## worker
`distribution_proof_to_demand_worker` (weekly).

## KPI
- Look-alike outreach approval rate.
- Conversion lift vs non-proof-anchored drafts.
- Net new proof packs created per quarter.

## failure_mode
- Consent expired or revoked.
- Look-alike scoring miss.

## recovery_path
- Block any draft referencing a revoked proof.
- Refresh look-alike scoring.

## kill_switch
`make growth-kill-proof-to-demand`.

## audit
`audit/distribution_proof_to_demand_runs.jsonl`.
