# Proof Pack Template

> **Status:** Every proof-bearing claim needs a proof pack.
> **Schema:** `schemas/launch/proof_pack.schema.json`.
> **Companion:** `docs/proposal/ROI_DISCUSSION_WITHOUT_GUARANTEE_AR.md`.

## What is a proof pack

A proof pack is a structured record of one claim + its evidence. It exists so:

- The sales team can defend the claim.
- The trust preflight can check the claim.
- The audit trail shows what was promised.

## The structure

```json
{
  "proof_id": "proof_2024_audit_001",
  "claim": "10 فرص ضايعة في 5 أيام.",
  "evidence_level": "L3",
  "evidence_type": "case_study",
  "source": "first_audit_with_agency_x",
  "limitation": "n=1; not generalizable",
  "approved_for_sales_use": true,
  "owner": "founder",
  "review_date_iso": "2024-12-01",
  "expiry_date_iso": "2025-06-01",
  "client_logo_used": false,
  "client_name_used": false,
  "anonymized": true,
  "excerpt": "After 5 days of read-only analysis, the agency identified 12 missed follow-ups...",
  "supporting_files": ["proof_2024_audit_001.pdf"]
}
```

## The 5 evidence levels

| Level | Definition | Use |
| --- | --- | --- |
| L0 | No evidence (placeholder) | Internal draft only. Never for client-facing. |
| L1 | Anecdote (founder's experience) | Internal only. |
| L2 | One case (n=1) | Allowed in proposals, with the limitation stated. |
| L3 | Multiple cases (n=3+) | Strong. Allowed without limitation. |
| L4 | External benchmark (research, industry data) | Strong. Cite the source. |
| L5 | Audited, published, or peer-reviewed | Strongest. Use when available. |

## The 4 evidence types

| Type | Definition | Example |
| --- | --- | --- |
| `case_study` | A specific client engagement | "In 5 days we found 12 missed follow-ups." |
| `benchmark` | Industry data | "The average agency loses 20% of inbound leads." |
| `audit_finding` | The output of an audit | "10 specific leaks tagged in the data." |
| `expert_opinion` | A named expert's view | Cite the expert. |

## The hard rules

1. **L0/L1 claims are never used in client-facing copy.** They are placeholders.
2. **L2 claims must state the limitation** (n=1, single sector, etc.).
3. **L3+ claims can be used without limitation.**
4. **Client logos** can only be used with written permission (logged in the proof pack).
5. **Client names** can only be used with written permission.
6. **Anonymized excerpts** are the default.
7. **Numbers** must be verifiable. Made-up numbers = L0.
8. **Time-bound:** every proof pack has an `expiry_date_iso`. After expiry, re-approve or retire.

## The review process

1. Sales or founder drafts the proof pack.
2. Trust preflight runs on the claim.
3. Founder approves.
4. The pack moves to the proof pack library.
5. Marketing can reference the pack in any draft.
6. Every 6 months, the pack is reviewed for freshness.

## The library

`templates/launch/proof_pack.example.json` is the canonical entry. The full library lives in `data/launch/proof_packs/<proof_id>.json`.

## The sales copy

When a draft uses a claim:

- The draft references the `proof_id` (e.g. "proof_2024_audit_001").
- The trust preflight verifies the `proof_id` exists in the library.
- The trust preflight verifies the pack is not expired.
- The trust preflight verifies the `evidence_level` is at least L2 for client-facing copy.

If any of these fail, the draft is rejected.

## When to update the library

- Every new case study = new proof pack.
- Every new benchmark = new proof pack.
- Every 6 months = review for expiry.
- Every retirement of a client = remove the proof pack (or anonymize more).

## When NOT to use a proof pack

- In cold outreach. The reader has not earned the right to see proof.
- In a first discovery call. The proof is what you build IN the call.
- In a breakup email. The proof is not the point of a breakup.
- In a pricing message. Pricing is a founder-approved number, not a proof.
