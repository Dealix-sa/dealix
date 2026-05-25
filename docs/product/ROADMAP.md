# Rolling Roadmap — خارطة الطريق المتجددة

## Purpose
A three-horizon roadmap (Now / Next / Later) explicitly tied to the four proof gates. No long-range commitments; the roadmap is rewritten when a proof gate is passed.

## Owner
Founder. Reviewed monthly; rewritten quarterly or on gate-pass.

## Inputs
- Current proof gate from `docs/founder/CEO_90_DAY_STRATEGIC_PLAN.md`.
- Productization candidates from `docs/product/PRODUCTIZATION_COMMAND_CENTER.md`.
- Build/Defer/Kill log.
- Cash and runway snapshot.
- Client and partner evidence.

## Outputs
- This file, dated and versioned.
- Items linked to intake IDs in `docs/product/FEATURE_INTAKE.md`.
- Public-safe summary for `docs/investor/ROADMAP.md`.

## The Horizons
### Now (this quarter — gate-bound)
- Items that directly serve the current proof gate.
- Each item: owner, kill criterion, evidence target.
- Max 5 items; if more, founder cuts to 5.

### Next (next quarter — conditional)
- Items unlocked only if Now items pass their kill criterion.
- Listed but not staffed.

### Later (12-month horizon — directional only)
- Themes, not deliverables.
- No promises, no dates.

## Rules
1. No item enters Now without passing `docs/product/BUILD_DEFER_KILL.md` as BUILD.
2. No Now item without a written kill criterion.
3. Items can move backward (Now → Next) but not skip forward.
4. Items in `docs/product/NO_OVERBUILD_POLICY.md` cannot appear at any horizon.
5. Public-safe summary omits client names and sensitive metrics.
6. Estimated value figures labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Metrics
- Now-item completion rate.
- Items killed mid-quarter (target ≥ 1; signals discipline).
- Roadmap-to-actual variance (planned vs delivered).
- Gate-pass count per year.

## Cadence
- Weekly: status check.
- Monthly: review and small reshuffles.
- Quarterly or gate-pass: full rewrite.

## Evidence
- `evidence/roadmap/v<n>_<YYYY-MM-DD>.md` snapshot per revision.

## Verifier
Founder. Delivery analyst checks ties to intake IDs.

## Runtime Command
`make roadmap-snapshot` — writes a dated snapshot, verifies all Now items have kill criteria.

## Arabic Summary — ملخص عربي
خارطة طريق بثلاث آفاق: الآن، التالي، لاحقًا. مرتبطة ببوابات الإثبات. لا التزامات طويلة. كل عنصر "الآن" له معيار إيقاف مكتوب. القيم التقديرية ليست مُتحقَّقة.
