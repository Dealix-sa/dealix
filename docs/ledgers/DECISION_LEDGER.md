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
| D-003 | 2026-05-18 | Correct the product narrative across launch + sales-kit copy | `launch_content_queue.md` and four sales-kit files (`dealix_pitch_deck.md`, `dealix_onepager.md`, `dealix_onepager.html`, audited `dealix_investor_faq.md`) marketed Dealix as an "AI sales rep" that replies in 45 seconds, auto-books demos, auto-qualifies BANT, with a "1 SAR pilot" — contradicting current doctrine (approval-first revenue ops radar, draft-only, 499 SAR 7-Day Revenue Proof Sprint) | Old copy breaches the doctrine non-negotiables: no exaggerated claims, no auto-send, no guaranteed outcomes (`docs/DISTRIBUTION_OS.md`, `docs/OFFER_LADDER_AND_PRICING.md`) | High — false external claims expose Dealix to compliance and trust failure | Founder | Corrected: `launch_content_queue.md` fully rewritten with a canonical positioning section; sales-kit false lines corrected in place with `<!-- CORRECTED -->` notes. Freeze-allowed as a doctrine hotfix + market-motion artifact |

Tie to [`../company/DECISION_OPERATING_SYSTEM.md`](../company/DECISION_OPERATING_SYSTEM.md).
