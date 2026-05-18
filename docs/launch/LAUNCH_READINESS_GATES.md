# Launch Readiness Gates — Executive Go/No-Go Scorecard — بوابات جاهزية الإطلاق — لوحة قرار المضي

**Status:** ACTIVE — launch decision surface.
**As of:** 2026-05-18.
**Owner of the decision:** Founder.
**Freeze compliance:** This document is a market-motion / operating artifact. It
authorizes selling and Rung 0–1 delivery only. See
[`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md).

This is the **executive scorecard** for the Dealix launch. It records every
launch gate, its owner, its current status, and what closes it. It is the
single page the Founder reads to answer one question: *can Dealix launch now?*
For the step-by-step operational checklist that closes the technical gates, use
[`../sales-kit/DEALIX_LAUNCH_GATES.md`](../sales-kit/DEALIX_LAUNCH_GATES.md).

---

## EN — The launch rule

Launch is authorized **only when every BLOCKING gate is GREEN or explicitly
Founder-waived in writing**. AMBER and RED non-blocking gates do not stop the
launch but must be visible in the go/no-go record. There is no "partial launch":
the launch is either authorized under this rule or it is not.

**Critical path:** **Moyasar payment account activation (G1) is the one true
blocker.** Until a test-mode charge passes, Dealix cannot accept a paid Rung 1
engagement, and the launch cannot be authorized. G2 (ZATCA / VAT) is the second
blocking gate and its status must be confirmed, not assumed.

## AR — قاعدة الإطلاق

يُسمح بالإطلاق **فقط عندما تكون كل بوابة حاجبة خضراء أو يتنازل عنها المؤسس صراحةً
وكتابةً**. البوابات غير الحاجبة بالحالة الكهرمانية أو الحمراء لا توقف الإطلاق لكن
يجب أن تكون ظاهرة في سجل قرار المضي. لا يوجد «إطلاق جزئي»: إما أن يكون الإطلاق
مُصرَّحًا به وفق هذه القاعدة أو لا.

**المسار الحرج:** **تفعيل حساب الدفع Moyasar (البوابة 1) هو الحاجب الحقيقي
الوحيد.** حتى تنجح عملية شحن في وضع الاختبار، لا تستطيع Dealix قبول ارتباط مدفوع
للدرجة 1، ولا يمكن التصريح بالإطلاق. البوابة 2 (هيئة الزكاة والضريبة / ضريبة
القيمة المضافة) هي البوابة الحاجبة الثانية، ويجب تأكيد حالتها لا افتراضها.

---

## EN — Gate scorecard

| Gate | Description | Owner | Blocking? | Status | What closes it |
|---|---|---|---|---|---|
| G1 | Moyasar payment account live + a test-mode charge passes end-to-end | Founder | Yes | **RED** | Complete Moyasar KYC, activate the account, run the test-mode charge in Gate 3 of the step-by-step checklist |
| G2 | ZATCA e-invoicing / VAT registration confirmed | Founder | Yes | **AMBER** | Confirm VAT registration status and ZATCA e-invoicing readiness; if not required at current revenue, record that finding in writing |
| G3 | Canonical Money Ladder published | Agent / done | No | **GREEN** | Closed — `docs/MONEY_LADDER.md` is the single canonical offer ladder |
| G4 | Narrative reconciled, launch-path assets on-doctrine | Agent / done | No | **GREEN (launch path) / AMBER (overall)** | Launch-path assets are on-doctrine; 61 legacy files carry legacy-narrative language and are flagged for later cleanup — non-blocking |
| G5 | Rung 0–1 delivery dry-run passed | Agent / done | No | **GREEN (with caveats)** | Closed — verdict GO; carries the G1 import-cascade fix and the G3 completeness-only proof-score caveats from the dry-run |
| G6 | Founder sales kit present and reconciled | Agent / done | No | **GREEN** | Closed — `docs/sales-kit/` and `docs/distribution/` are populated and reconciled to doctrine |
| G7 | Warm list qualified + outreach drafts queued | Agent / done | No | **GREEN (with flag)** | Closed — 20 leads qualified and drafts queued; flag: leads are cold-sourced and need a genuine warm path before any send |
| G8 | Doctrine-guard tests pass | Agent / CI | No | **VERIFY BEFORE LAUNCH** | Run the `tests/test_no_*.py` doctrine guards in CI and confirm all pass on the launch commit |
| G9 | Trust page published | Agent / done | No | **GREEN** | Closed — `docs/distribution/TRUST_PAGE_COPY.md` is published |
| G10 | Founder go/no-go recorded | Founder | Yes | **PENDING** | Founder reviews this scorecard and records a dated go/no-go decision |

## AR — لوحة البوابات

| البوابة | الوصف | المالك | حاجبة؟ | الحالة | ما يُغلقها |
|---|---|---|---|---|---|
| G1 | حساب الدفع Moyasar مُفعّل + نجاح شحن في وضع الاختبار من البداية للنهاية | المؤسس | نعم | **أحمر** | إكمال اعرف عميلك في Moyasar، تفعيل الحساب، تنفيذ شحن وضع الاختبار في البوابة 3 من قائمة الخطوات |
| G2 | تأكيد الفوترة الإلكترونية لهيئة الزكاة والضريبة / تسجيل ضريبة القيمة المضافة | المؤسس | نعم | **كهرماني** | تأكيد حالة تسجيل ضريبة القيمة المضافة وجاهزية الفوترة الإلكترونية؛ إن لم تكن مطلوبة عند مستوى الإيراد الحالي، يُسجَّل ذلك كتابةً |
| G3 | نشر سُلّم المال المرجعي | الوكيل / منجز | لا | **أخضر** | مُغلقة — `docs/MONEY_LADDER.md` هو سُلّم العروض المرجعي الوحيد |
| G4 | توحيد السردية، وأصول مسار الإطلاق مطابقة للعقيدة | الوكيل / منجز | لا | **أخضر (مسار الإطلاق) / كهرماني (إجمالًا)** | أصول مسار الإطلاق مطابقة للعقيدة؛ 61 ملفًا قديمًا يحمل لغة السردية القديمة ومُعلَّم للتنظيف لاحقًا — غير حاجب |
| G5 | اجتياز التشغيل التجريبي لتسليم الدرجة 0–1 | الوكيل / منجز | لا | **أخضر (مع تحفّظات)** | مُغلقة — القرار مضٍ؛ تحمل تحفّظ إصلاح تتابع الاستيراد G1 وتحفّظ درجة الإثبات المقيسة بالاكتمال فقط G3 من التشغيل التجريبي |
| G6 | حقيبة مبيعات المؤسس حاضرة ومُوحَّدة | الوكيل / منجز | لا | **أخضر** | مُغلقة — `docs/sales-kit/` و`docs/distribution/` مُعبّأة ومُوحَّدة مع العقيدة |
| G7 | القائمة الدافئة مؤهَّلة + مسودّات التواصل مُجهّزة | الوكيل / منجز | لا | **أخضر (مع تنبيه)** | مُغلقة — 20 عميلًا مؤهَّلًا والمسودّات مُجهّزة؛ تنبيه: العملاء من مصدر بارد ويحتاجون مسار تعارف حقيقي قبل أي إرسال |
| G8 | نجاح اختبارات ضوابط العقيدة | الوكيل / التكامل المستمر | لا | **تحقَّق قبل الإطلاق** | تشغيل ضوابط `tests/test_no_*.py` في التكامل المستمر وتأكيد نجاحها كلها على إصدار الإطلاق |
| G9 | نشر صفحة الثقة | الوكيل / منجز | لا | **أخضر** | مُغلقة — `docs/distribution/TRUST_PAGE_COPY.md` منشورة |
| G10 | تسجيل قرار المضي من المؤسس | المؤسس | نعم | **معلَّقة** | يراجع المؤسس هذه اللوحة ويُسجّل قرار مضٍ مؤرَّخ |

---

## EN — Dry-run caveats carried into launch (G5)

The Rung 0–1 delivery dry-run reached a GO verdict, but two honest conditions
from [`DELIVERY_DRYRUN_REPORT.md`](DELIVERY_DRYRUN_REPORT.md) travel with the
launch and must be visible to whoever runs delivery:

- **G1 caveat (import cascade).** A Python import-cascade pulls the full
  application stack into the canonical OS modules. This must be fixed — ship the
  dependencies or decouple the imports — **before** a delivery operator runs the
  Sprint on a clean box. Until then the delivery runbook must pin the
  environment. This is a delivery-side fix and is distinct from the G1 payment
  gate above; both happen to be numbered "G1" in their own documents.
- **G3 caveat (proof score is completeness only).** The Proof Pack score
  measures section completeness, not evidence strength. A pack can score
  100 / `case_candidate` while containing no verified evidence. **A
  100 / `case_candidate` pack must never be shown to a customer as verified
  proof.** Treat the score as a completeness gate; verified-evidence status
  depends on `client_confirmed` value events, not section fill.

## AR — تحفّظات التشغيل التجريبي المنقولة إلى الإطلاق (G5)

بلغ التشغيل التجريبي لتسليم الدرجة 0–1 قرار المضي، لكن شرطين صادقين من
[`DELIVERY_DRYRUN_REPORT.md`](DELIVERY_DRYRUN_REPORT.md) يرافقان الإطلاق ويجب أن
يكونا ظاهرين لمن يُنفّذ التسليم:

- **تحفّظ G1 (تتابع الاستيراد).** تتابع استيراد في بايثون يجرّ حزمة التطبيق
  الكاملة إلى وحدات النظام المرجعية. يجب إصلاح ذلك — شحن التبعيات أو فك ارتباط
  الاستيرادات — **قبل** أن يُنفّذ مُشغّل التسليم السبرنت على جهاز نظيف. حتى ذلك
  الحين يجب أن يُثبّت دليل التسليم البيئة. هذا إصلاح في جانب التسليم ويختلف عن
  بوابة الدفع G1 أعلاه؛ صودف ترقيمهما «G1» كلٌّ في وثيقته.
- **تحفّظ G3 (درجة الإثبات تقيس الاكتمال فقط).** درجة حزمة الإثبات تقيس اكتمال
  الأقسام لا قوة الأدلة. قد تبلغ الحزمة 100 / `case_candidate` وهي خالية من أي
  دليل مُتحقَّق. **يجب ألا تُعرض حزمة بـ 100 / `case_candidate` على عميل بوصفها
  إثباتًا مُتحقَّقًا أبدًا.** تُعامَل الدرجة كبوابة اكتمال؛ وحالة الدليل
  المُتحقَّق تعتمد على أحداث قيمة `client_confirmed` لا على تعبئة الأقسام.

---

## EN — How to use this scorecard

1. The Founder closes **G1** and **G2** — the two blocking gates that depend on
   external accounts. G1 is the critical path.
2. The Agent / CI confirms **G8** on the launch commit.
3. The Founder reviews the full scorecard and records **G10** with a date.
4. If a blocking gate is GREEN by waiver rather than by closure, the waiver is
   written into the G10 record with the reason.
5. Re-link from [`../sales-kit/DEALIX_LAUNCH_GATES.md`](../sales-kit/DEALIX_LAUNCH_GATES.md)
   for the operational steps; this page stays at the executive level.

## AR — كيف تُستخدم هذه اللوحة

1. يُغلق المؤسس **G1** و**G2** — البوابتين الحاجبتين المعتمدتين على حسابات
   خارجية. G1 هو المسار الحرج.
2. يؤكّد الوكيل / التكامل المستمر **G8** على إصدار الإطلاق.
3. يراجع المؤسس اللوحة كاملةً ويُسجّل **G10** بتاريخ.
4. إن صارت بوابة حاجبة خضراء بتنازل لا بإغلاق، يُكتب التنازل في سجل G10 مع السبب.
5. ارجع من [`../sales-kit/DEALIX_LAUNCH_GATES.md`](../sales-kit/DEALIX_LAUNCH_GATES.md)
   للخطوات التشغيلية؛ تبقى هذه الصفحة على المستوى التنفيذي.

---

## EN — Related documents

- [`../sales-kit/DEALIX_LAUNCH_GATES.md`](../sales-kit/DEALIX_LAUNCH_GATES.md) — step-by-step gate checklist.
- [`LAUNCH_MASTER_INDEX.md`](LAUNCH_MASTER_INDEX.md) — the full launch command surface.
- [`DELIVERY_DRYRUN_REPORT.md`](DELIVERY_DRYRUN_REPORT.md) — Rung 0–1 delivery dry-run, source of the G5 caveats.
- [`../MONEY_LADDER.md`](../MONEY_LADDER.md) — canonical offer ladder.
- [`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md) — what is permitted during the freeze.

## AR — وثائق ذات صلة

- [`../sales-kit/DEALIX_LAUNCH_GATES.md`](../sales-kit/DEALIX_LAUNCH_GATES.md) — قائمة البوابات خطوة بخطوة.
- [`LAUNCH_MASTER_INDEX.md`](LAUNCH_MASTER_INDEX.md) — سطح قيادة الإطلاق الكامل.
- [`DELIVERY_DRYRUN_REPORT.md`](DELIVERY_DRYRUN_REPORT.md) — التشغيل التجريبي لتسليم الدرجة 0–1، مصدر تحفّظات G5.
- [`../MONEY_LADDER.md`](../MONEY_LADDER.md) — سُلّم العروض المرجعي.
- [`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md) — ما هو مسموح أثناء التجميد.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
