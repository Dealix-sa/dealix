# Evidence System

Every strong claim made by Dealix — to a customer, in a proposal, in
public content, or in a recommendation to the founder — must have evidence.

## Required Evidence For

- A-priority leads
- Public claims (capability, results, compliance)
- Client recommendations
- Pricing changes
- Case studies
- Product roadmap decisions

## Evidence Types

- Customer message
- Lead source URL
- Public company page
- Call note (dated, with attendees)
- Payment record
- Delivery result (report, dashboard)
- Client feedback (written)
- Test output (CI run, smoke test)
- Public-safety check result

## Rule

**No evidence, no strong claim.** A recommendation that cites no evidence
is downgraded to a hypothesis and routed for further data collection
before action.

## Storage

- Public artifacts (case studies, anonymized results) → `docs/proof/`
- Private artifacts (raw lead lists, payment records, call notes) →
  `dealix-ops-private/`

## Doctrine Link

The Evidence System is enforced by:
- `scripts/verify_public_safety.py` — banned claims with no evidence
- Trust Guard agent in `docs/agents/AGENT_REGISTRY.md`
- The `claims_needing_review` field in `TrustState`
