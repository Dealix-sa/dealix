# قرار دخول السوق — Market Entry Decision

> Current beachhead: Saudi B2B mid-market. Stage rule: 3 paid sprints, 2 deliveries, 1 retainer attempt before any new market.

## Purpose
Resist premature expansion. Saudi is large, undermined, and matches the moat strategy. New markets cost focus.

## Owner
Founder/CEO.

## Inputs
- ICP performance (`ICP_STRATEGY.md`).
- North star count (`NORTH_STAR.md`).
- Sector report coverage (`docs/sector-reports/`).
- Existing market docs (`docs/strategy/MENA_EXPANSION_LOGIC.md`, `MARKET_MAP_SAUDI.md`).

## Outputs
- Current beachhead declaration (this file).
- Not-Now list (this file).
- Per-candidate market checklist (filled when stage rule is met).

## Rules
1. Saudi B2B mid-market is the only active market until further notice.
2. No new market is opened without all stage rule items completed in the candidate market.
3. Any "expansion" deal that requires Dealix to operate from outside Saudi triggers an A3 Go/No-Go gate.
4. Customer demand alone is not sufficient for expansion. The stage rule must be met.
5. "Not-Now" items are not "Never" — but their addition requires the stage rule, not nostalgia.

## Metrics
- Markets active: 1 (target until further notice).
- Saudi PSDE per quarter: tracked, target ≥ 3 floor.
- Out-of-market deals declined: tracked.

## Cadence
Reviewed Quarterly.

## Evidence
This file + per-candidate market checklists if any.

## Verifier
`make market-entry-verify` — checks active market count is 1 and any candidates have a completed stage rule checklist.

## Runtime Command
`make market-entry-review`

---

## Current beachhead

**Saudi Arabia, B2B mid-market.**

Why:
- Largest unmet operational-discipline market in the region.
- Buyer culture rewards evidence over slideware.
- Vision 2030 creates a 5-year tailwind for operational rigor.
- Bilingual AR/EN matches Dealix's native posture.
- Regulatory environment is workable and improving.

## The Stage Rule (entry to any new market)

A new market is opened only after **all** are true in that candidate market:

1. **3 paid sprints** delivered to customers based in that market.
2. **2 successful deliveries** with case-safe evidence shipped.
3. **1 retainer attempt** (whether accepted or not — the attempt itself proves operational readiness).
4. **Legal review** completed for that jurisdiction (`docs/legal/`).
5. **Disclosure surfaces** translated to local primary language if not AR/EN.
6. **Cash reserve** of ≥ 6 months runway after estimated expansion cost.

If any single condition is missing, the market remains Not-Now.

## Not-Now list (candidates with reasons)

| Market | Why interesting | Why not now |
|---|---|---|
| UAE | Adjacent, mature B2B, English-leaning | No 3 paid sprints; would split focus |
| Egypt | Large, AR-native | Decision cycles longer; payment risk higher pre-evidence |
| Kuwait, Bahrain, Oman | Small but accessible | Stage rule unmet; Saudi capacity not full |
| North Africa | AR-native, growing | Regulatory environment varies; far from beachhead |
| Levant | AR-native | Macro uncertainty; payment infrastructure |

## When to revisit Not-Now items
- Saudi PSDE saturates (≥ 50/year and capacity-constrained).
- Stage rule items achieved in a candidate market organically (e.g., 3 inbound paid sprints from one market in a year).
- A specific moat (e.g., sector data) needs cross-market data to remain credible.

## Out-of-market deal handling
- Polite decline with a written explanation referencing this file.
- Optional referral to a partner if one exists.
- The deal counts as a signal in the Not-Now log for that market.

## A3 Go/No-Go trigger
Any of these triggers an A3 gate before action:
- Hiring outside Saudi.
- Opening a legal entity outside Saudi.
- Localizing public content for a non-Saudi market.
- Public statements implying multi-market posture before the stage rule is met.

## القواعد العربية
1. الموطن الحالي هو السوق السعودي للأعمال متوسطة الحجم. فقط.
2. لا سوق جديد دون استيفاء قاعدة المرحلة (3 سبرنتات مدفوعة + تسليمَين + محاولة احتفاظ + مراجعة قانونية + إفصاحات + احتياطي نقدي).
3. طلب العميل وحده لا يكفي لفتح سوق.

## Cross-links
- `STRATEGIC_THESIS.md`
- `ICP_STRATEGY.md`
- `NORTH_STAR.md`
- `docs/strategy/MENA_EXPANSION_LOGIC.md`
- `docs/founder/GO_NO_GO_DECISION_SYSTEM.md`
