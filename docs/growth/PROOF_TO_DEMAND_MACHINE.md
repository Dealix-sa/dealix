# Proof-to-Demand Machine

The Proof-to-Demand Machine converts approved proof artefacts (case
studies, sample outputs, pilot results) into outbound drafts and content
references. It is the bridge between the Proof Approval OS and the
distribution layer.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Take a freshly approved proof artefact and produce a small set of
high-fit outbound drafts for accounts most likely to value that specific
proof.

## 2. Input

Sources:

- `proof/proof_library.csv` (rows with `approval_state = approved`).
- `growth/account_scores.csv`.
- `growth/icp_segments.csv`.
- `growth/personas.csv`.
- `outreach/suppression.csv`.
- `marketing/objection_library.csv` (link objections to relevant proof).

A proof artefact is eligible the moment it is approved by the Proof
Safety Agent and the trust ledger entry is written.

## 3. Output

`outreach/proof_demand_queue.csv` columns:

- `draft_id`
- `proof_id`
- `account_id`
- `persona_id`
- `channel_id` — EM | LI | WARM (CF allowed for invited only)
- `language`
- `subject`
- `body`
- `brand_voice_pass`
- `suppression_check`
- `guarantee_scan`
- `approval_state`
- `drafted_by`
- `drafted_at`

Default behaviour: produce 5-15 drafts per approved proof, targeted at
the accounts whose ICP and persona best match the proof's sector and
buyer shape.

## 4. Source of truth

`outreach/proof_demand_queue.csv` in the private ops runtime.

## 5. Approval class

A2. The proof is already approved; the outbound drafts referencing it
still require founder approval per A2 rules.

## 6. Trust gate

- Suppression check.
- Guarantee scan (proof is not a guarantee; copy may not claim it is).
- Brand voice check.
- Proof integrity: referenced proof must be approved and current.
- Confidentiality respect: drafts must respect the proof's redaction
  posture (e.g. "named customer" vs. "Saudi enterprise client").

## 7. Owner

`proof_safety_agent`. Allowed write target: `proof/`. Coordinates with
`distribution_operator` to land drafts in the outreach queues.

## 8. Worker

`scripts/dealix_proof_to_demand.py` (planned). Idempotent on
`(proof_id, account_id)`.

## 9. KPI

- Proof-driven Reply Rate (replies / approved sends referencing
  proof).
- Proof Approval Cycle Time (proof approved -> drafts queued).
- Confidentiality Bleed (target: 0; any redaction violation is a
  critical incident).
- Brand voice first-pass rate.

## 10. Failure mode

- Drafts overstate the proof outcome. Brand Guardian rewrites.
- Drafts reveal redacted information. Trust Guardian halts; critical
  incident opened.
- Outdated proof referenced after its review window. Worker checks
  freshness; expired proof not used.

## 11. Recovery path

- For overstatement: rewrite session; root cause review.
- For confidentiality bleed: incident opened; proof access reviewed.
- For expiry: proof safety agent re-validates and re-approves.

## 12. Cadence

| Cadence | Activity |
|---|---|
| On approval | Queue 5-15 drafts per fresh proof |
| Weekly | Proof freshness audit |
| Monthly | Proof-fit-to-ICP review |

## 13. Saudi-specific overlays

- Bilingual proof artefacts: drafts default to the buyer's primary
  language; proof reference matches.
- Sector references: Saudi buyers respond strongly to specific Saudi
  references when available; the worker prioritises Saudi-named proofs.
- Confidentiality: many Saudi customers prefer to remain unnamed;
  drafts respect this absolutely.

## 14. Non-negotiables

- No external send.
- No "guaranteed" framing of proof.
- No reveal of redacted information.
- A3 not used.

Proof is the strongest demand-creation asset Dealix has. Treating it
with care is the whole point of this machine.

## 15. Worker contract

- Reads inputs idempotently.
- Writes only to `outreach/proof_demand_queue.csv`.
- Cannot send messages.
- Cannot reference unapproved proof.
- Cannot bypass redaction posture.
- Logs every draft to the trust ledger.
- Honours the kill switch.

## 16. Audit trail

Every draft generates a ledger entry with `draft_id`, `proof_id`,
`account_id`, and the redaction posture used. The proof library is
cross-referenced so that any future revocation can sweep affected
drafts.

## 17. Revocation sweep

When a proof's `approval_state` flips to `revoked`, the worker
sweeps `outreach/proof_demand_queue.csv` and marks all drafts
referencing that proof as `approval_state = blocked`. A ledger entry
captures the sweep with the operator who is expected to retrieve the
sent items if any have left the door.

## 18. Cross-references

- `docs/proof/PROOF_APPROVAL_OS.md` for proof intake and approval.
- `docs/growth/CONTENT_TO_DEMAND_ENGINE.md` for content-side use of
  proof.
