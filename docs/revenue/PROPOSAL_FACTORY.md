# Proposal Factory

The Proposal Factory drafts proposals from a parametric template,
embeds approved proof, and queues the draft for founder approval.
Proposals are sent manually after approval. The factory never sends.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. Purpose

Produce proposals that are specific, accurate, audit-friendly, and
priced from sanctioned offers — without ever including guaranteed-
outcome or "guaranteed revenue" language.

## 2. Input

Sources:

- `sales/pipeline.csv` (opportunity at stage = sample_reviewed or
  beyond).
- `sales/sample_queue.csv` (the sample that preceded this proposal).
- `product/offer_ladder.csv` (sanctioned offers and prices).
- `growth/personas.csv`, `growth/icp_segments.csv`.
- `proof/proof_library.csv`.
- `marketing/objection_library.csv` (proposal anticipates objections).
- `legal/proposal_terms_library.csv` (standard terms and clauses).

A proposal is produced only on operator request, on a specific named
opportunity, with a sanctioned offer.

## 3. Output

Two outputs:

- The proposal document (PDF and editable source) under
  `proposals/{opportunity_id}/`.
- The queue row in `sales/proposal_queue.csv`.

`sales/proposal_queue.csv` columns:

- `proposal_id`
- `opportunity_id`
- `account_id`
- `persona_id`
- `offer_id`
- `price_band`
- `payment_terms_id`
- `language`
- `embedded_proof_refs`
- `state` — drafted | reviewed | approved | sent | won | lost | hold
- `approval_state`
- `drafted_by`
- `drafted_at`
- `sent_at`
- `decision_window_close_at`
- `notes`

## 4. Source of truth

`sales/proposal_queue.csv` for state; `proposals/` for the document.

## 5. Approval class

A2. Drafting autonomous; founder approval required before any external
send. Price and term commits are explicitly guarded by policy rule
`pricing_commit_requires_approval` — no agent may commit pricing.

## 6. Trust gate

- Guarantee scan: any guaranteed-outcome language blocks the draft.
- Brand voice check.
- Offer integrity: the offer_id must be a sanctioned offer at the
  stated price band.
- Payment terms integrity: payment_terms_id must reference a sanctioned
  terms entry; any deviation requires founder approval and a ledger
  entry (policy rule `payment_terms_require_escalation`).
- Proof integrity: every embedded proof is approved.
- Legal terms: every clause must come from `proposal_terms_library.csv`
  unless approved as a one-off by the founder.
- Confidentiality: no other-account data referenced.
- Bilingual integrity (where applicable).

## 7. Owner

`delivery_copilot` agent. Allowed write target: `sales/`. Coordinates
with `finance_copilot` on price and terms, `proof_safety_agent` on
embedded proof, and `offer_architect` on the offer ladder.

## 8. Worker

`scripts/dealix_proposal_factory.py` (planned). The worker:

1. Reads the opportunity and offer selection.
2. Drafts the proposal from parametric templates.
3. Embeds approved proof and citations.
4. Writes document and queue row.
5. Sets `decision_window_close_at` per the offer's standard window.

## 9. KPI

- Proposal Win Rate.
- Proposal Cycle Time (days from sent to decision).
- Brand voice first-pass rate.
- Confidentiality violations (target: 0).
- Term-deviation incidents (target: 0 without approval).

## 10. Failure mode

- Proposal contains a guarantee. Brand Guardian blocks.
- Proposal references unapproved proof. Worker rejects.
- Off-menu price quoted. Worker rejects without founder approval entry.
- Off-menu payment terms. Same.
- Legal clause not in library. Same.
- Bilingual mismatch. Worker holds.

## 11. Recovery path

- For guarantee scan failure: rewrite; ledger entry; root cause.
- For unapproved proof: proof safety agent expedites or proposal omits
  the proof.
- For off-menu price or terms: founder approval recorded; ledger entry;
  proposal re-drafted.
- For legal clause drift: legal lead reviews; library updated only
  with approval.
- For bilingual mismatch: copy aligned.

## 12. Cadence

| Cadence | Activity |
|---|---|
| Daily | Proposals drafted on operator request |
| Weekly | Win/loss review |
| Monthly | Template and clause library audit |
| Quarterly | Offer ladder calibration |

## 13. Saudi specifics

- Many Saudi buyers require Arabic-primary proposals; the worker
  defaults to the buyer's operating language.
- Standard payment terms align with PDPL and ZATCA invoicing rules;
  deviations are rare and explicit.
- Decision windows are bounded but realistic; the default close is
  14-30 days depending on offer.

## 14. Non-negotiables

- No guaranteed outcomes anywhere.
- No off-menu price or terms without founder approval.
- No clause not in the library without approval.
- No external send.
- A3 not used.

The proposal is the only document the buyer reads before saying yes or
no. It is worth getting right.
