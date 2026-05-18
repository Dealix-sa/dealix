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

Tie to [`../company/DECISION_OPERATING_SYSTEM.md`](../company/DECISION_OPERATING_SYSTEM.md).
