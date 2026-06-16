# Delivery Decision

No **client-facing** output ships unless this gate passes.

## Required

| Gate | Requirement |
|------|----------------|
| QA | Score ≥ **85** (or service-specific threshold documented) |
| Governance | Check passed — [`../governance/GOVERNANCE_DECISION.md`](../governance/GOVERNANCE_DECISION.md) |
| Proof | Proof pack exists for the engagement (`06_proof_pack.md` + annexes) |
| Next action | Explicit next step for the client (not “contact us”) |
| Hard fails | None (see below) |

Artifacts: `clients/<client>/delivery_approval.md`, [`../quality/OUTPUT_QA_SCORECARD.md`](../quality/OUTPUT_QA_SCORECARD.md).

## Hard fail (automatic block)

- PII leakage or unlawful processing
- Unsupported / fake proof
- Knowledge answer **without** source when source is required ([`DEALIX_STANDARD.md`](../company/DEALIX_STANDARD.md))
- Unsafe automation (cold WhatsApp, etc.) — [`../governance/FORBIDDEN_ACTIONS.md`](../governance/FORBIDDEN_ACTIONS.md)
- Guaranteed sales / revenue claims without defensible basis
- **No next action** — even a “beautiful” report is **blocked**

## Delivery outcomes

```text
Approved
Needs Revision
Blocked
```

## Rule

The client pays for a **clear decision**, not decoration. No next action → **Blocked**.

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
