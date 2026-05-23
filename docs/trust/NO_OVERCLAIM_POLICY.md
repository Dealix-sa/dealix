# No-Overclaim Policy

> Every claim Dealix makes externally must be supported by evidence.
> Enforced by `dealix/trust/claim_guard.py`.

## What Counts As A Claim

- Numerical claim ("X% increase", "saved Y hours")
- Comparison claim ("faster than X", "better than Y")
- Compliance claim ("PDPL compliant", "SDAIA aligned")
- Capability claim ("our AI does X")
- Outcome claim ("clients see Y")
- Time claim ("delivered in N days")

If a sentence makes an assertion that affects a buying decision, it's a claim.

## Required Evidence For Each Claim

| Claim type | Required evidence |
|---|---|
| Numerical | Source URL or internal data with computation |
| Comparison | Both sides cited; date of comparison |
| Compliance | Pointer to the relevant clause + how we satisfy it |
| Capability | Working demonstration or test result |
| Outcome | n ≥ 3 evidence packs, anonymized |
| Time | Logged delivery records (n ≥ 1, preferably n ≥ 3) |

## Banned Language

These phrases are blocked at draft level by `claim_guard.py`:
- "industry-leading"
- "best-in-class"
- "revolutionary"
- "10x", "100x", "1000x" (without source)
- "guaranteed" (without contract enforceability)
- "AI-powered" (alone — must specify what)
- "set and forget"
- "autonomous" (alone — must specify human gates)
- "transformational"
- "synergy"
- Up-to-X% language without source
- ROI numbers without backing

## Allowed Patterns

- "In our last 3 sprints, average delivery time was 6 days (range 5–7)."
- "Our trust gate blocks N% of automated sends pending founder review (logged 2026-05)."
- "Pricing: SAR 499 per Sprint (productized, fixed scope per `OFFER.md`)."
- "Saudi PDPL alignment via data retention policy in `docs/trust/DATA_RETENTION_POLICY.md` (review with your DPO)."

## The Evidence Pack Rule

Any A3 claim (public) must have a corresponding evidence pack:
- A markdown file in `content/proof_library/` (private repo)
- Containing: claim text, supporting data/links, methodology, date
- Approved by founder + claim_guard pass

If a claim appears in public without an evidence pack on file → Trust incident.

## Test At Three Points

1. **At draft generation** (agent layer) — claim_guard runs on every generated text
2. **At founder approval** (human review) — founder verifies evidence pack exists
3. **At publish** (publish layer) — final claim_guard pass + log

## When A Claim Fails

- Block the publish
- Surface the failure reason to founder
- Either: edit the claim to fit evidence OR strengthen the evidence
- Never: override claim_guard without logged decision + DECISION_LOG entry

## Existing Public Surfaces (must comply)

- LinkedIn posts (per `docs/content/LINKEDIN_SYSTEM.md`)
- Landing page (`landing/`)
- README
- Case studies
- Sales decks
- Proposals
- Sample artifacts
- Sector reports
- Email signatures

Any new public surface must enumerate its claims and prove each.

## Specifically About Saudi Compliance Claims

Saudi compliance claims (PDPL, SDAIA, ZATCA, ZATCA invoicing) carry **elevated risk**:
- Never claim "compliant" without legal review
- Always claim "aligned with" + specific clause
- Defer to client's own counsel on definitive applicability
- Log every compliance claim in `trust/claim_approval_log.csv`

## What This Policy Refuses

- Aspirational language presented as fact
- Composite outcomes presented as a single customer's result
- AI capability claims without working test
- Pricing comparison without showing both sides
- "We will soon..." claims without committed dates
