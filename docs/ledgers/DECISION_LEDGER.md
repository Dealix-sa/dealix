# Decision Ledger

Material decisions only (sell / don’t sell / build / block / price / enterprise). IDs: `D-###`.

## Every entry must include

```text
Decision
Context
Evidence
Risk
Owner
Outcome
Review Date (if time-bound)
```

| ID | Date | Decision | Context | Evidence | Risk | Owner | Outcome |
|----|------|-----------|---------|----------|------|-------|---------|
| D-001 | | Sell Lead Intelligence officially | Readiness stable | demo + QA + proof templates | Low | | Official |
| D-002 | | Do not build WhatsApp auto-send now | Compliance + product focus | governance policy; no repeat demand | High | | Blocked |
| D-003 | 2026-05-18 | Moyasar live-payment KYC is the #1 company blocker | First paid revenue and the commercial-freeze exit (first paid pilot) are blocked until live payments work. Founder-only manual action, 1–3 business days. | `docs/ops/MOYASAR_KYC_CHECKLIST.md` | High | Founder | In progress — tracked daily until `MOYASAR_MODE=production` |
| D-004 | 2026-05-18 | Unify product narrative on the current doctrine | Repo carried a conflicting old story ("AI rep replies in 45s / auto-books / 1 SAR"); current doctrine is approval-first, draft-only, 499 SAR Sprint. Conflicting claims violate `no_fake_proof` / `no_unverified_outcomes`. | `docs/ops/COMMERCIAL_FREEZE.md`, `docs/OFFER_LADDER_AND_PRICING.md` | Med | Founder | In progress — WS-0 narrative unification |
| D-005 | 2026-05-18 | WS-2 — rung 0–1 delivery verified ready; no code changes needed | Verified the Free Mini Diagnostic (rung 0) and the 499 SAR Revenue Proof Sprint (rung 1) ship real customer-facing rendered deliverables. Rung 0: `POST /api/v1/company-growth-beast/diagnostic` returns a real 7-section bilingual diagnostic rendered as an on-page HTML report by `landing/diagnostic.html`; the `/api/v1/diagnostic/report/pdf` surface also renders a diagnostic to PDF. Rung 1: `delivery_sprint.run_sprint` runs 8 orchestrated steps → 14-section ProofPack (`merge_proof_pack_v2`) → real PDF via `proof_pack_to_pdf` / `pdf_renderer` (15 KB PDF produced on a TEST customer). Payment→delivery audit link intact: `payment_ops` `delivery_kickoff_id` is passed as the Sprint `engagement_id` and stamped on the ProofPack. No minimum-scope gap found. | 140 tests pass (`test_delivery_sprint`, `test_sprint_runner_render`, `test_diagnostic_router`, `test_payment_ops_full_ops`, `test_wave6_payment_confirmation`, `test_proof_pack_render`, `test_proof_pack_assembler`, `test_beast_level`, `test_wave6_ai_ops_diagnostic`); in-process API smoke green | Low | Founder | Verified — rung 0–1 delivery-finish complete; no build needed |

Tie to [`../company/DECISION_OPERATING_SYSTEM.md`](../company/DECISION_OPERATING_SYSTEM.md).
