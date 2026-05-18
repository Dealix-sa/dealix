# Dealix — برج تحكم التدشين · Master Launch OS

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `CANONICAL_NARRATIVE_AND_PRICE.md` · `LAUNCH_90_DAY_SEQUENCE.md` · `../commercial/COMMERCIAL_CONTROL_TOWER.md`

---

## لماذا توجد هذه الـOS · Why this OS exists

المنصة جاهزة مادياً: 117 router، و3,881 اختباراً، و9 وحدات OS، و97 سكربتاً، و9+ تدفقات cron. الكود ليس عنق الزجاجة. عنق الزجاجة هو **التماسك والتفعيل** — رواية واحدة، سعر واحد، تسلسل تنفيذ واحد، وأول pilot مدفوع يخرج من الباب. هذه الوثيقة هي برج التحكم الذي يربط ثماني وثائق تدشين شقيقة ويمنع التشتت.

The platform is materially ready: 117 routers, 3,881 tests, 9 OS modules, 97 scripts, 9+ cron workflows. Code is not the bottleneck. The bottleneck is **coherence and activation** — one narrative, one price, one execution sequence, and the first paid pilot out the door. This document is the control tower that binds eight sibling launch docs and prevents drift.

---

## مبادئ التشغيل · Operating doctrine

أربعة مبادئ تحكم كل قرار تدشين:

1. **مصدر واحد للحقيقة · One source of truth.** السعر هو **499 ريال** (`revenue_proof_sprint_499`) والرواية هي "approval-first". أي تعارض يُحسم لصالح [`CANONICAL_NARRATIVE_AND_PRICE.md`](CANONICAL_NARRATIVE_AND_PRICE.md).
2. **الأتمتة = تحضير وصفّ · Automation = preparation and queuing.** Dealix يجهّز المسودات والتشخيصات والـProof Packs ويصفّها؛ الإنسان يوافق عند كل حدّ خارجي. لا إرسال آلي.
3. **احترام التجميد التجاري · Respect the Commercial Freeze.** التجميد أداة تركيز: لا بناء جديد للطبقات Tier 2–5 قبل أول pilot مدفوع وأول Proof Pack.
4. **إضافي فقط · Additive only.** لا تغييرات محفوفة بالمخاطر على كود التسليم أو الدفع الحيّ — نُضيف ولا نعيد كتابة المسارات الحيّة.

Four principles govern every launch decision:

1. **One source of truth.** The price is **499 SAR** (`revenue_proof_sprint_499`) and the narrative is approval-first. Any conflict resolves in favour of [`CANONICAL_NARRATIVE_AND_PRICE.md`](CANONICAL_NARRATIVE_AND_PRICE.md).
2. **Automation = preparation and queuing.** Dealix prepares and queues drafts, diagnostics, and Proof Packs; a human approves at every external boundary. No auto-send.
3. **Respect the Commercial Freeze.** The freeze is a focusing tool: no new Tier 2–5 build before the first paid pilot and the first Proof Pack.
4. **Additive only.** No risky changes to live delivery or payment code — we add, we do not rewrite live paths.

---

## مسارات العمل الستة · The 6 workstreams

| المسار · Workstream | الوصف · Description |
|---|---|
| WS1 — توحيد الحقيقة · Truth Unification | تثبيت السعر والرواية الرسميين عبر كل أصل — [`CANONICAL_NARRATIVE_AND_PRICE.md`](CANONICAL_NARRATIVE_AND_PRICE.md). |
| WS2 — تفعيل سكة الإيراد · Revenue Rail Activation | تشغيل Moyasar وتسليم أول pilot مدفوع — `MOYASAR_ACTIVATION_RUNBOOK.md` · `FIRST_PILOT_PLAYBOOK.md`. |
| WS3 — تنسيق الآلة · Machine Orchestration | خريطة السكربتات وتدفقات cron التي تحضّر العمل للموافقة — `MACHINE_ORCHESTRATION_MAP.md`. |
| WS4 — قمرة قيادة المؤسس · CEO Cockpit | لوحة القرار اليومية للمؤسس — `CEO_LAUNCH_COCKPIT.md`. |
| WS5 — تفعيل الذهاب للسوق · GTM Activation | تسلسل التدشين 90 يوماً والطلب — [`LAUNCH_90_DAY_SEQUENCE.md`](LAUNCH_90_DAY_SEQUENCE.md). |
| WS6 — جاهزية التدشين · Launch Readiness | قياس الجاهزية قبل الإطلاق العلني — `LAUNCH_READINESS_SCORECARD.md`. |

---

## فهرس وثائق Master Launch OS · Master Launch OS Doc Index

ثماني وثائق في مجلد `docs/launch/`، كلها جزء من طبقة Master Launch OS:

| الوثيقة · Doc | الغرض · Purpose |
|---|---|
| [`MASTER_LAUNCH_OS.md`](MASTER_LAUNCH_OS.md) | برج التحكم — نموذج التشغيل والفهرس والتسلسل. · The control tower — operating model, index, sequencing. |
| [`CANONICAL_NARRATIVE_AND_PRICE.md`](CANONICAL_NARRATIVE_AND_PRICE.md) | المصدر الوحيد للسعر والرواية الرسميين. · The single source of truth for canonical price and narrative. |
| `MOYASAR_ACTIVATION_RUNBOOK.md` | خطوات تفعيل بوابة الدفع للوضع الحيّ. · Steps to activate the payment gateway for live mode. |
| `FIRST_PILOT_PLAYBOOK.md` | دليل إغلاق وتسليم أول pilot مدفوع. · Playbook for closing and delivering the first paid pilot. |
| `MACHINE_ORCHESTRATION_MAP.md` | خريطة السكربتات وتدفقات cron التحضيرية. · Map of preparatory scripts and cron workflows. |
| `CEO_LAUNCH_COCKPIT.md` | لوحة قرار المؤسس اليومية أثناء التدشين. · The founder's daily decision cockpit during launch. |
| [`LAUNCH_90_DAY_SEQUENCE.md`](LAUNCH_90_DAY_SEQUENCE.md) | خطة التدشين 90 يوماً معاد ضبطها على 499 ريال. · The 90-day launch plan rebased to 499 SAR. |
| `LAUNCH_READINESS_SCORECARD.md` | بطاقة قياس جاهزية التدشين قبل الإطلاق العلني. · The launch readiness scorecard before go-live. |

---

## الرقم الوحيد الذي يهمّ · The single number that matters

رقم واحد يحكم نجاح التدشين: **عدد الـpilots المدفوعة المُسلَّمة عند 499 ريال، والـMRR المتراكم منها**. كل نشاط آخر — منشور، demo، محادثة شريك — يُقاس بمساهمته في هذا الرقم. لا رقم بديل، ولا مقياس عُجب.

A single number governs launch success: **the count of paid pilots delivered at 499 SAR, and the MRR accrued from them**. Every other activity — a post, a demo, a partner conversation — is measured by its contribution to that number. No vanity metric stands in for it.

---

## التسلسل ثلاثي المراحل · 3-Phase Sequencing

| المرحلة · Phase | المدى · Window | المخرجات · Outputs |
|---|---|---|
| Phase 1 | الأيام 1–3 · Days 1–3 | توحيد الحقيقة (WS1) وقياس الجاهزية (WS6)؛ المؤسس يبدأ تفعيل Moyasar بالتوازي. · Truth unification (WS1) and readiness measure (WS6); founder starts Moyasar activation in parallel. |
| Phase 2 | الأيام 3–7 · Days 3–7 | تنسيق الآلة (WS3)، قمرة القيادة (WS4)، وتجربة تسليم جافة لطبقة Tier 0–1. · Machine orchestration (WS3), CEO cockpit (WS4), and a delivery dry-run for Tier 0–1. |
| Phase 3 | اليوم 7 فما بعد · Day 7+ | إطلاق الذهاب للسوق علنياً (WS5)، أول pilot مدفوع، وأول Proof Pack. · GTM go-live (WS5), the first paid pilot, and the first Proof Pack. |

المراحل لا تُقفز. لا تنتقل Phase 2 إلى Phase 3 قبل اكتمال تجربة التسليم الجافة.

Phases are not skipped. Phase 2 does not advance to Phase 3 before the delivery dry-run is complete.

---

## الربط بطبقة Commercial Scale OS · Link to the Commercial Scale OS layer

طبقة التدشين تُسلِّم العميل المدفوع الأول؛ بعدها تتسلّم طبقة "Commercial Scale OS" حلقة التوسع. راجع [`../commercial/COMMERCIAL_CONTROL_TOWER.md`](../commercial/COMMERCIAL_CONTROL_TOWER.md) لنموذج التحويل من اهتمام إلى دفع إلى Proof إلى توسّع.

The launch layer delivers the first paid customer; the "Commercial Scale OS" layer then takes over the expansion loop. See [`../commercial/COMMERCIAL_CONTROL_TOWER.md`](../commercial/COMMERCIAL_CONTROL_TOWER.md) for the interest → payment → proof → expansion model.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
