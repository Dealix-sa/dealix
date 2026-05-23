# Dealix Execution Roadmap (Final)

## North star
Dealix becomes a company when it touches the market, not when every doc is perfect.

## Horizon 1 — Activation (Week 1–2)
Goal: stand up the operating skeleton.
- Complete Sprints 0–8.
- Bootstrap `dealix-ops-private/` working tree.
- Run all sprint verifiers to green.
- Founder reviews `DEALIX_DEFINITION_OF_DONE.md` and signs off.

## Horizon 2 — First market loop (Week 2–4)
Goal: produce evidence that the system can touch the market.
- Sprint 9: 25 leads / 25 DMs / 3 samples / 1 proposal / payment-or-PO follow-up.
- Weekly close: business score, control tower brief, learning ledger update.
- One system update committed back into the public repo (a doc, a verifier, or a schema).

## Horizon 3 — First delivery (Week 4–6)
Goal: complete the first paid (or written-approved) engagement.
- Sprint 10: intake → delivery report → QA pass → handoff → feedback → retainer ask.
- Capture proof artifacts (with approval) into the content library.
- Decide whether to repeat or evolve the offer based on win/loss data.

## Horizon 4 — Repeatability (Week 6–12)
Goal: a second and third paying engagement using the same offer.
- Productization candidates documented in `productization/candidates.csv`.
- Sub-agent assistance enabled where the founder is the bottleneck.
- Delegation ladder moves at least one task from founder → contractor.

## Horizon 5 — SaaS readiness (post-Week 12)
Goal: only after repeatability is proven.
- SaaS architecture gate passed: `docs/product/SAAS_ARCHITECTURE_GATE.md`.
- Trust + finance + delivery proven over at least 3 paying customers.
- Capital plan documented before any code is written for SaaS surface.

## Decision gates (do not skip)
1. **Activation gate**: all verifiers green.
2. **Market gate**: at least one paid contract OR written PO.
3. **Repeatability gate**: 3 paying customers in same offer.
4. **SaaS gate**: SAAS_ARCHITECTURE_GATE.md signed by founder.

## Weekly cadence (every Sunday evening, KSA time)
- Run `make ceo-weekly`, `make weekly-close`, `make business-score`, `make assurance`.
- Update `dealix-ops-private/business_audit/score_history.csv`.
- Choose next week's one bet and document it.
