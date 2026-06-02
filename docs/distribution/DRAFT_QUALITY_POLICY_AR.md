# سياسة جودة المسودات — Dealix Draft Quality Policy

هذا الملف يحدّد **قواعد جودة المسودة** التي يجب أن تجتازها كل مسودة قبل أن تصبح `ready` وقبل وصولها للمؤسس. أي مخالفة تُسجَّل في الحقل `quality_issues` على كيان `draft` وتمنع الموافقة.

This file defines the **draft quality rules** every draft must pass before becoming `ready` and before reaching the founder. Any violation is logged in `quality_issues` on the `draft` entity and blocks approval.

روابط / Related: [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md) · [../commercial/APPROVAL_POLICY_AR.md](../commercial/APPROVAL_POLICY_AR.md) · [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md) · [REVENUE_EXECUTION_OS_AR.md](REVENUE_EXECUTION_OS_AR.md)

---

## قواعد الجودة / The quality rules

كل قاعدة مرفوضة تُدوَّن في `quality_issues` بالرمز المقابل، وتمنع `status = ready` و`governance_status = approved`.

Each failed rule is recorded in `quality_issues` with its code and blocks `ready` and `approved`.

| الرمز / Code | القاعدة / Rule | الشرح / Explanation |
|---|---|---|
| `no_guarantee` | لا ضمان / No guarantee | لا «نضمن»، لا «مضمون»، لا التزام بنتيجة. تُستبدَل بـ«فرص مُثبتة بأدلة». / No "نضمن", no "guaranteed"; replace with "evidence-backed opportunities". |
| `no_hundred_percent` | لا «100%» / No "100%" | لا ادعاءات اكتمال أو نجاح مطلق. / No absolute-success or 100% claims. |
| `no_dhaman_word` | لا «نضمن» / No "نضمن" | حظر صريح لصيغة الضمان بالعربية. / Explicit ban on the Arabic guarantee phrasing. |
| `no_roi_without_proof` | لا ROI بلا دليل / No ROI without proof | لا رقم عائد/تحويل إلا بمستوى دليل يدعمه (L≥3). / No ROI/conversion figure without a supporting evidence level (L≥3). |
| `no_excess_pii` | لا PII زائدة / No excess PII | لا بريد/هاتف/هوية/أسماء حقيقية زائدة عن الحاجة. / No email/phone/ID/real names beyond need. |
| `not_too_long` | ليس طويلاً / Not too long | الرسالة موجزة بحسب القناة؛ لا إطالة مرهِقة. / Concise per channel; no tiring length. |
| `no_annoying_pressure` | لا ضغط مزعج / No annoying pressure | لا إلحاح أو ندرة مصطنعة أو تهديد بفوات الفرصة. / No badgering, fake scarcity, or FOMO pressure. |
| `no_forbidden_channel` | لا قناة محظورة / No forbidden channel | لا واتساب بارد، لا أتمتة LinkedIn، لا scraping، لا اتصال آلي. / No cold WhatsApp, LinkedIn automation, scraping, or robo-calling. |
| `no_send_without_approval` | لا إرسال بلا موافقة / No send without approval | لا صياغة تفترض إرسالاً آلياً؛ كل إرسال يدوي بعد موافقة. / No phrasing assuming auto-send. |
| `no_claim_without_evidence_level` | لا ادعاء بلا مستوى دليل / No claim without evidence level | كل ادعاء قابل للتحقق مربوط بـ`evidence_level` كافٍ. / Every verifiable claim ties to a sufficient evidence level. |

---

## كيف يُطبَّق الفحص / How the check applies

1. تُصاغ المسودة بحالة `status = draft`. / The draft starts at `draft`.
2. تنتقل إلى `in_review` ويُجرى فحص القواعد العشر. / It moves to `in_review` and the ten rules run.
3. أي مخالفة ⇒ `status = needs_edit` مع رمز في `quality_issues`. / Any violation sets `needs_edit` with a code.
4. بعد التصحيح وخلوّ `quality_issues` ⇒ `status = ready`. / After fixing and a clean `quality_issues` list, it becomes `ready`.
5. عندها فقط يدخل طابور الموافقة (`governance_status = pending_approval`). / Only then does it enter the approval queue.

> لا تصل أي مسودة للمؤسس وفيها مخالفة جودة قائمة. / No draft with an open quality violation reaches the founder.

---

## ربط الدليل / Evidence linkage

- مستويات الدليل L0–L5 معرَّفة في [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md). / Levels L0–L5 are defined in the proof pack factory.
- الادعاءات الرقمية (تحويل/عائد/توفير) لا تُذكَر إلا عند `evidence_level ≥ L3` ومع مصدر القياس. / Numeric claims appear only at `evidence_level ≥ L3` with a measurement source.
- في غياب الدليل، تُصاغ القيمة كـ«فرصة تقديرية» لا كنتيجة. / Without evidence, value is framed as an "estimated opportunity," not a result.

---

## قواعد ملزمة / Binding rules

1. خلوّ `quality_issues` شرط للوصول إلى `ready` و`approved`. / A clean issue list is required for `ready` and `approved`.
2. لا تجاوز للفحص لأي نوع مسودة (`draft_type`). / No bypass for any draft type.
3. لا قناة محظورة ولا إرسال آلي. / No forbidden channel, no auto-send.
4. لا ادعاء يتجاوز `evidence_level`. / No claim beyond the evidence level.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
