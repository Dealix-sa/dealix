# مواصفة نظام المسودات — Dealix Draft System Spec

هذا الملف يحدّد **أنواع المسودات**، **حالات المسودة**، **جدول سياسة القنوات** (بريد/واتساب/LinkedIn/هاتف/عرض × v1/v2/v3)، وقاعدة أن **الإصدار الأول = مسودات فقط**. الكيان `draft` يحمل الحقول حرفياً: `id`, `prospect_id`, `draft_type`, `channel`, `locale`, `subject`, `body`, `status`, `governance_status`, `quality_issues`, `evidence_level`, `created_at`, `product_id`.

This file defines **draft types**, **draft states**, the **channel policy table** (Email/WhatsApp/LinkedIn/Phone/Proposal × v1/v2/v3), and the rule that **v1 = drafts only**.

روابط / Related: [REVENUE_EXECUTION_OS_AR.md](REVENUE_EXECUTION_OS_AR.md) · [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md) · [../commercial/APPROVAL_POLICY_AR.md](../commercial/APPROVAL_POLICY_AR.md) · [PROSPECT_OS_AR.md](PROSPECT_OS_AR.md)

---

## أنواع المسودات / Draft types (`draft_type`)

| `draft_type` | الوصف / Description | القناة الافتراضية / Default channel |
|---|---|---|
| `intro` | تواصل أول مع جهة warm. / First contact with a warm party. | بريد / Email |
| `followup` | متابعة وفق الإيقاع. / Cadence follow-up. | بريد / Email |
| `reply` | رد على رسالة العميل. / Reply to the prospect. | حسب المحادثة / per thread |
| `discovery_invite` | دعوة لجلسة اكتشاف. / Discovery invitation. | بريد / Email |
| `call_script` | سكربت مكالمة لبشر. / Call script for a human. | هاتف / Phone |
| `proposal_cover` | رسالة مرافِقة للعرض. / Proposal cover note. | بريد / Email |
| `linkedin_note` | رسالة/تعليق LinkedIn. / LinkedIn message or note. | LinkedIn |
| `whatsapp_warm` | رسالة واتساب لجهة warm فقط. / Warm-only WhatsApp message. | واتساب / WhatsApp |

> كل مسودة تُربَط بعميل (`prospect_id`) ومنتج (`product_id`) ولغة (`locale`: `ar` / `en`). / Every draft links to a prospect, a product, and a locale.

---

## حالات المسودة / Draft states

تُمثَّل عبر حقلين: `status` (دورة حياة المحتوى) و`governance_status` (دورة الموافقة).

Represented by two fields: `status` (content lifecycle) and `governance_status` (approval lifecycle).

| `status` | المعنى / Meaning |
|---|---|
| `draft` | مُصاغ ابتدائياً. / Initially drafted. |
| `in_review` | تحت فحص الجودة. / Under quality check. |
| `needs_edit` | يحتاج تعديل (مخالفة في `quality_issues`). / Needs edits (issue in `quality_issues`). |
| `ready` | اجتاز الجودة وجاهز للموافقة. / Passed quality, ready for approval. |
| `archived` | محفوظ/متروك. / Archived or dropped. |

`governance_status` يتبع [../commercial/APPROVAL_POLICY_AR.md](../commercial/APPROVAL_POLICY_AR.md): `pending_approval` → `approved` / `changes_requested` / `rejected` / `on_hold` → `sent`.

---

## جدول سياسة القنوات / Channel policy table

الإصدارات تعني نضج القدرة، لا أسماء معروضة للعميل. **v1 = مسودات فقط؛ لا إرسال خارجي آلي.**

Versions mean capability maturity, not customer-facing labels. **v1 = drafts only; no automated external send.**

| القناة / Channel | v1 | v2 | v3 |
|---|---|---|---|
| بريد / Email | مسودة فقط؛ إرسال يدوي بعد موافقة | إرسال يدوي مُيسَّر بعد موافقة + سجل | إرسال مُجدوَل بموافقة مسبقة لكل رسالة (RFC منفصل) |
| واتساب / WhatsApp | مسودة warm فقط؛ يرسلها بشر | قالب warm معتمَد يرسله بشر | — لا أتمتة إرسال (يبقى يدوياً) |
| LinkedIn | مسودة فقط؛ ينشرها المؤسس يدوياً | مسودة + جدول يدوي للمؤسس | — لا أتمتة (محظور) |
| هاتف / Phone | سكربت فقط؛ المكالمة بشرية | سكربت + ملاحظات نتيجة | — لا اتصال آلي (محظور) |
| عرض / Proposal | مسودة كاملة + سعر ضمن النطاق؛ بانتظار موافقة | مسودة + تجميع تلقائي للأقسام | إرسال يدوي بعد موافقة على السعر النهائي |

> العمود v1 هو الوضع الحالي الملزِم. الأعمدة v2/v3 خارطة قدرة مستقبلية **لا تُفعَّل** إلا عبر RFC وموافقة، وتظل أتمتة LinkedIn/الهاتف **محظورة** دائماً. / The v1 column is the current binding posture. v2/v3 are a future capability map activated only via RFC and approval; LinkedIn/phone automation stays forbidden.

---

## قاعدة الإصدار الأول / The v1 rule

> **في v1: كل ما ينتجه مصنع المسودات يبقى مسودة بانتظار موافقة. لا قناة خارجية تُرسِل آلياً.**
>
> **In v1: everything the draft factory produces stays a draft pending approval. No external channel auto-sends.**

- `governance_status` الابتدائي دائماً `pending_approval`. / Initial governance status is always `pending_approval`.
- الانتقال إلى `sent` لا يحدث إلا يدوياً بعد `approved`. / A move to `sent` happens only manually after `approved`.
- لا واتساب بارد، لا أتمتة LinkedIn، لا scraping، لا اتصال آلي. / No cold WhatsApp, no LinkedIn automation, no scraping, no robo-calling.

---

## قواعد ملزمة / Binding rules

1. كل مسودة تجتاز [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md) قبل `ready`. / Every draft passes the quality policy before `ready`.
2. كل مسودة تحمل `evidence_level` ولا تتجاوز ادعاءاتها مستواه. / Every draft carries an evidence level and makes no claim beyond it.
3. لا PII زائدة في `body` أو `subject`. / No excess PII in body or subject.
4. كل مسودة مربوطة بمنتج عبر `product_id`. / Every draft links to a product.
5. القرار النهائي بالإرسال للمؤسس. / Final send decision belongs to the founder.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
