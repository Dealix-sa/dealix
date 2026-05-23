# No-Overbuild Policy — سياسة عدم البناء المُفرط

## Purpose
Explicit, named list of things Dealix will not build before the four proof gates (Interest, Conversion, Delivery, Retention) are passed. Removes ambiguity. Stops founder tinkering and contractor scope creep.

## Owner
Founder. List can only be modified by founder, with written rationale.

## Inputs
- `docs/founder/CEO_90_DAY_STRATEGIC_PLAN.md` (which proof gate are we on).
- `docs/founder/CEO_NOT_NOW_LIST.md` (the broader Not Now list).
- Industry benchmark of premature scale failures.

## Outputs
- Auto-Kill flag in `docs/product/BUILD_DEFER_KILL.md` for any matching intake.
- Quarterly recertification of the list.

## The List — We Will Not Build Pre-Proof
1. **Full SaaS platform** — no multi-tenant product before 10 automated runs of a single workflow.
2. **Mobile app** — no native or hybrid app before any web product has paying retention.
3. **White-label / reseller portal** — no partner self-serve before 5 paid partner deals manual.
4. **Enterprise admin / RBAC console** — no admin UI before 3 paid enterprise contracts demand it in writing.
5. **Agent marketplace / agent expansion** — no public agent catalogue before one agent earns its keep on paid work.
6. **Long-form pitch deck (>10 slides)** — no investor deck before 1 paid sprint + 1 delivery + 1 written feedback.
7. **Hiring before repetition** — no full-time hire until the triggers in `docs/people/HIRING_TRIGGERS.md` fire.
8. **Public LLM gateway product** — no external sale of gateway access before internal usage demonstrates margin.
9. **Custom UI design system / branded component library** — defer until 3 paying customers see the same UI.
10. **Outbound automation (cold WhatsApp, LinkedIn bots, scraping)** — never offered as a service.
11. **Multi-language UI beyond AR + EN** — defer until paying demand in a third language.
12. **Self-serve onboarding** — defer until 10 manual onboardings show the same path.

## Rules
1. Anything matching the list is auto-Kill in `docs/product/BUILD_DEFER_KILL.md`.
2. Removing an item requires founder signature plus the evidence that unlocks it.
3. No marketing copy may imply these capabilities exist.
4. Contractors and partners are briefed on this list at onboarding.
5. Estimated savings from not-building are labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Metrics
- Count of intakes auto-Killed by this policy.
- Founder hours saved (estimated).
- Items removed from the list per quarter (target: 0-2; high churn signals weak discipline).

## Cadence
- Quarterly recertification.
- Immediate review when a proof gate is passed.

## Evidence
- Signed list version under `evidence/policy/no_overbuild_vN.md`.

## Verifier
Founder. Counter-checked by delivery analyst at quarterly review.

## Runtime Command
`make policy-check FT=<id>` — flags the intake if it matches any item on this list.

## Arabic Summary — ملخص عربي
هذه قائمة صريحة لما لن نبنيه قبل اجتياز بوابات الإثبات الأربع. أي طلب ميزة يطابقها يُلغى تلقائيًا. القيم التقديرية ليست مُتحقَّقة.
