---
title: Build / Defer / Kill
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Build / Defer / Kill — ابنِ / أجِّل / أوقف

## Purpose
Decision framework that turns triaged feature requests into a portfolio call: build now, defer to next quarter, or kill. The framework is bounded so the founder cannot drift into platform-building.

## Definitions
- **Build** — work scheduled this quarter; resourced; release gate set.
- **Defer** — accepted in principle, no resources this quarter; re-scored next quarter.
- **Kill** — closed permanently; re-open requires new evidence.

## Scoring criteria
| Criterion | Weight | Range |
|---|---|---|
| Paying-customer demand | 30% | 0 = none, 5 = ≥3 paying asks |
| Manual success count | 25% | 0 = none, 5 = ≥10 successes |
| Revenue impact (90 days) | 20% | 0 = none, 5 = ≥SAR 50k upside |
| Build cost (inverse) | 15% | 5 = ≤1 week, 0 = >1 month |
| Strategic fit | 10% | aligns with current ICP/sector focus |

Score ≥ 3.5 → Build. 2.0–3.4 → Defer. < 2.0 → Kill.

## Rules
- Anything on [`NO_OVERBUILD_POLICY.md`](NO_OVERBUILD_POLICY.md) is auto-killed regardless of score until the unlocking precondition is met.
- A Build decision needs founder approval. Above SAR 30k estimated build cost it requires written A2 approval per `docs/governance/APPROVAL_MATRIX.md`.
- Decisions are logged inline (one row per item) with date and score breakdown.

## Operations
- Items enter from [`FEATURE_INTAKE.md`](FEATURE_INTAKE.md) after weekly triage.
- Quarterly portfolio review re-scores every Defer item. Items deferred twice are auto-killed unless evidence improved.
- Killed items archive to `docs/product/kill_log/` (folder created on first kill).

## Evidence
- Each row links: intake ID, score breakdown, decision date, decider, rationale.
- Build decisions also link to release plan in [`RELEASE_POLICY.md`](RELEASE_POLICY.md).

## Owner & cadence
- Owner: Founder.
- Cadence: weekly add-to-list; quarterly portfolio re-score.

## Cross-links
- [`FEATURE_INTAKE.md`](FEATURE_INTAKE.md)
- [`NO_OVERBUILD_POLICY.md`](NO_OVERBUILD_POLICY.md)
- [`RELEASE_POLICY.md`](RELEASE_POLICY.md)

---

## القسم العربي

**الغرض:** إطار قرار يحوّل الطلبات المُفرزة إلى: ابنِ الآن، أجِّل، أو أوقف.

**معايير التقييم:** طلب العملاء الدافعين 30%، عدد النجاحات اليدوية 25%، أثر الإيراد خلال 90 يومًا 20%، تكلفة البناء عكسيًا 15%، التوافق الاستراتيجي 10%.

**العتبات:** ≥3.5 ابنِ، 2.0–3.4 أجِّل، <2.0 أوقف.

**القواعد:** أي بند في `NO_OVERBUILD_POLICY.md` يُوقف تلقائيًا؛ البناء بتكلفة >30 ألف ريال يتطلب موافقة A2.

**المالك:** المؤسس. **الإيقاع:** مراجعة محفظة ربعية.
