# Partner Strategy — استراتيجية الشراكات

## Purpose
Define when partners enter Dealix's go-to-market, what they do, and what they don't. Partners join after proof, not before. They amplify what works; they do not invent the product.

## Owner
Founder. Strategy reviewed quarterly.

## Inputs
- Proof gates passed (`docs/founder/CEO_90_DAY_STRATEGIC_PLAN.md`).
- Case study library.
- Sector signals.
- Capacity to support partners (founder time + ops).

## Outputs
- This document.
- Partner entry decision (Yes/No) per quarter.

## Entry Gate — Partners Only After
1. Proof of Delivery gate passed: at least 1 paid sprint delivered and accepted.
2. At least 1 case study (Track A or B) published.
3. Productization candidate at Template stage or later.
4. Founder capacity to run partner reviews weekly without dropping client quality.
5. Standard referral terms documented (`docs/partners/REFERRAL_TERMS.md`).

## Partner Types
| Type | Role | Earning |
|---|---|---|
| Agency partner | Co-delivers under Dealix brand | Hourly or per-sprint share |
| Sector specialist | Provides domain insight on engagement | Per-engagement honorarium |
| Referral partner | Introduces qualified buyers | Referral fee per `docs/partners/REFERRAL_TERMS.md` |
| Reseller (post-SaaS only) | Resells Dealix products | Revenue share |

## Rules
1. No partner before entry gate.
2. No exclusivity, no equity, no guarantees.
3. No partner speaks for Dealix without written approval.
4. Partners follow Dealix non-negotiables (no scraping, no automation, PDPL).
5. Partner contracts include termination-for-cause and PII clauses.
6. Reseller path is dormant until a SaaS product is live.
7. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to partner economic projections.

## Metrics
- Partners active by type.
- Partner-sourced revenue share.
- Time from partner onboarding to first deal (target ≤ 90 days).
- Partner dispute count.

## Cadence
- Quarterly strategy review.
- Monthly partner portfolio review.

## Evidence
- `evidence/partners/strategy/<YYYY-Qn>.md`.

## Verifier
Founder.

## Runtime Command
`make partner-strategy-review` — prints entry-gate status and current portfolio.

## Arabic Summary — ملخص عربي
الشركاء يدخلون بعد إثبات التسليم، لا قبله. لا حصرية، لا ضمانات. أربعة أنواع: وكالة، متخصص قطاع، مُحيل، موزِّع (لاحقًا فقط). القيم التقديرية ليست مُتحقَّقة.
