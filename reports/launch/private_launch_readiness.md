# Private Launch Readiness — جاهزية الإطلاق الخاص

> Purpose — الغرض: the readiness checklist that separates a Private Manual Launch from a Public Launch. A Private Manual Launch is founder-operated, warm-list only, with every external action approved by hand. A Public Launch is broader and carries a higher bar — including a passing build.
>
> قائمة الجاهزية التي تفصل الإطلاق الخاص اليدوي عن الإطلاق العام. الإطلاق الخاص يديره المؤسس، لقائمة دافئة فقط، مع موافقة يدوية على كل إجراء خارجي. الإطلاق العام أوسع ويحمل سقفًا أعلى — يشمل بناءً ناجحًا.

Cross-link: [REVENUE_COMMAND_CENTER.md](../../docs/05_founder/REVENUE_COMMAND_CENTER.md), [NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md](../../docs/03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md), [FIRST_OUTREACH_PACK.md](../../sales/FIRST_OUTREACH_PACK.md).

---

## The two launch modes — وضعا الإطلاق

| Mode | Audience | External actions | Build requirement |
|---|---|---|---|
| Private Manual Launch | warm, permissioned contacts only | each one approved by hand | not required to be green |
| Public Launch | broader audience | governed, still approval-gated | `npm run build` must pass |

A Private Manual Launch can proceed while the public build is not yet green, **as long as governance, delivery, and end-to-end gates are green.** A Public Launch may not proceed until `npm run build` passes.

يمكن أن يمضي الإطلاق الخاص اليدوي بينما البناء العام ليس أخضر بعد، **ما دامت بوابات الحوكمة والتسليم والاختبار الشامل خضراء.** لا يمضي الإطلاق العام حتى ينجح `npm run build`.

---

## Gates for Private Manual Launch — بوابات الإطلاق الخاص اليدوي

These must all be green:

- [ ] **Governance gate** — the approval doctrine is in force; every outbound artifact defaults to `draft_only`. See `NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md`.
- [ ] **Delivery gate** — the paid-sprint handoff SOP and daily rhythm are documented and ready.
- [ ] **End-to-end dry run** — `run_dealix_e2e_dry_run.py` completes with simulated events only (no live sends).
- [ ] **Warm list ready** — `data/growth/first_30_targets.csv` populated with permissioned contacts; no cold names.
- [ ] **Proof discipline** — no upsell path is open without a delivered proof pack.
- [ ] **Revenue board** — `founder_daily_command.py` renders `reports/founder/daily_command.md`.

البوابات الواجب أن تكون خضراء: الحوكمة (المسودة افتراضيًا)؛ التسليم (إجراءات موثقة)؛ تشغيل شامل تجريبي بأحداث محاكاة فقط؛ قائمة دافئة جاهزة بلا أسماء باردة؛ انضباط الإثبات قبل أي بيع إضافي؛ لوحة الإيرادات تُولَّد.

---

## Additional gates for Public Launch — بوابات إضافية للإطلاق العام

Everything above, plus:

- [ ] **Build passes** — `npm run build` completes with no errors.
- [ ] **Full verification** — `run_dealix_full_verification.sh` passes.
- [ ] **Claim safety** — no public copy states a guaranteed return, conversion rate, or ROI as fact.
- [ ] **Bilingual coverage** — every customer-facing public artifact has balanced AR + EN sections.
- [ ] **PII review** — no public artifact exposes PII; case studies anonymized.

كل ما سبق، إضافةً إلى: نجاح `npm run build`؛ التحقق الكامل؛ سلامة الادعاءات؛ التوازن الثنائي اللغة؛ مراجعة البيانات الشخصية.

---

## Sign-off — الاعتماد

A launch mode is authorized only when its gates above are all checked and a founder approval is logged. Private and Public are separate authorizations; clearing Private does not authorize Public.

يُعتمَد وضع الإطلاق فقط عند تحقق جميع بواباته وتسجيل موافقة المؤسس. الخاص والعام اعتمادان منفصلان؛ اجتياز الخاص لا يعتمد العام.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
