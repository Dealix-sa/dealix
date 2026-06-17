# سياسة الموافقة — Dealix Approval Policy

هذا الملف يحدّد ما يحق للذكاء الاصطناعي **صياغته** وما الذي يحتاج **موافقة المؤسس** قبل أي إرسال خارجي، مع موقف لكل قناة (بريد/واتساب/LinkedIn/هاتف/عرض) وحالات طابور الموافقة.

This file defines what the AI may **draft** versus what needs **founder approval** before any external send, with a posture per channel (email/WhatsApp/LinkedIn/phone/proposal) and the approval-queue states.

روابط / Related: [PRICING_GUARDRAILS_AR.md](PRICING_GUARDRAILS_AR.md) · [PRODUCT_CATALOG_AR.md](PRODUCT_CATALOG_AR.md) · [../distribution/REVENUE_EXECUTION_OS_AR.md](../distribution/REVENUE_EXECUTION_OS_AR.md) · [../distribution/DRAFT_SYSTEM_SPEC_AR.md](../distribution/DRAFT_SYSTEM_SPEC_AR.md) · [../distribution/DRAFT_QUALITY_POLICY_AR.md](../distribution/DRAFT_QUALITY_POLICY_AR.md)

---

## القاعدة الأساسية / The core rule

> **الذكاء الاصطناعي يصوغ. المؤسس يوافق. النظام يتتبّع. الإرسال الخارجي يبقى محكوماً.**
>
> **AI drafts. Founder approves. System tracks. External send stays controlled.**

في الإصدار الأول (v1): **لا إرسال خارجي آلي إطلاقاً.** كل ما يخرج للعميل يكون قد مرّ بموافقة بشرية صريحة. / In v1: **no automated external send at all.** Everything customer-facing passes explicit human approval.

---

## ما يجوز للذكاء الاصطناعي صياغته / What the AI may draft

- مسودات بريد، رسائل واتساب (warm فقط)، رسائل LinkedIn، سكربتات مكالمات، وعروض — كلها بحالة `status` ابتدائية = مسودة و`governance_status = pending_approval`. / Email, warm-only WhatsApp, LinkedIn messages, call scripts, and proposals — all starting as a draft with `governance_status = pending_approval`.
- تقارير داخلية، خرائط إيراد، Proof packs، تحليلات pipeline. / Internal reports, revenue maps, proof packs, pipeline analytics.
- اقتراح سعر **ضمن** النطاق المعتمد (لا سعر نهائي، لا مفاوضة). / A price suggestion within the approved band (no final price, no negotiation).
- اقتراح الإجراء التالي (`next_action`) وتاريخه. / Suggested next action and date.

## ما يحتاج موافقة المؤسس / What needs founder approval

- أي **إرسال خارجي** عبر أي قناة. / Any external send on any channel.
- أي **سعر نهائي** أو خروج عن السعر الثابت (راجع [PRICING_GUARDRAILS_AR.md](PRICING_GUARDRAILS_AR.md)). / Any final price or deviation from fixed price.
- أي **عرض** قبل إرساله (`proposal.approval_status`). / Any proposal before sending.
- أي **انتقال للدفع** (راجع [../distribution/PAYMENT_HANDOFF_AR.md](../distribution/PAYMENT_HANDOFF_AR.md)). / Any payment handoff.
- أي **تسليم** لمخرج للعميل. / Any customer-facing deliverable.
- أي **ادعاء** يتجاوز مستوى الدليل المتاح. / Any claim beyond the available evidence level.

---

## الموقف لكل قناة / Per-channel posture

| القناة / Channel | يجوز للذكاء الاصطناعي / AI may | يحتاج موافقة / Needs approval | محظور في v1 / Forbidden in v1 |
|---|---|---|---|
| بريد / Email | صياغة المسودة بالكامل | الإرسال | الإرسال الآلي الجماعي / bulk auto-send |
| واتساب / WhatsApp | صياغة رسالة warm فقط (جهة وافقت/طلبت) | الإرسال | واتساب بارد، أتمتة إرسال / cold or automated |
| LinkedIn | صياغة رسالة/تعليق | الإرسال اليدوي بالمؤسس | أتمتة LinkedIn، اتصال جماعي / automation |
| هاتف / Phone | صياغة سكربت مكالمة فقط | المكالمة يجريها بشر | اتصال آلي / robo-calling |
| عرض / Proposal | صياغة كل الأقسام والسعر ضمن النطاق | السعر النهائي + الإرسال | إرسال بلا موافقة / send without approval |

> warm = جهة اتصال أبدت اهتماماً أو طلبت تواصلاً أو ضمن علاقة قائمة. لا scraping، لا قوائم مشتراة، لا تواصل بارد. / warm = a contact who expressed interest, requested contact, or is within an existing relationship. No scraping, no bought lists, no cold outreach.

---

## حالات طابور الموافقة / Approval-queue states

ينتقل كل مخرج عبر هذه الحالات على الحقل `governance_status`:

Every deliverable moves through these states on `governance_status`:

| الحالة / State | المعنى / Meaning |
|---|---|
| `pending_approval` | مُصاغ وينتظر مراجعة المؤسس. / Drafted, awaiting founder review. |
| `approved` | وافق المؤسس؛ مسموح بالخطوة التالية (إرسال يدوي/تسليم). / Founder approved; next step allowed. |
| `changes_requested` | يحتاج تعديل قبل إعادة العرض. / Needs edits before re-review. |
| `rejected` | مرفوض؛ لا يُرسَل ولا يُسلَّم. / Rejected; not sent or delivered. |
| `on_hold` | مؤجَّل (انتظار دليل/جهة قرار/مراجعة مخاطر). / Held pending evidence/decision-maker/risk review. |
| `sent` | أُرسِل يدوياً بعد الموافقة؛ يُسجَّل وقت ومرجع. / Manually sent after approval; logged with time and reference. |

> لا قفز بين الحالات يتجاوز `approved`. لا حالة `sent` بدون `approved` سابقة. / No state skip past `approved`. No `sent` without a preceding `approved`.

---

## فحوص جودة قبل الموافقة / Pre-approval quality checks

قبل أن يصل أي مخرج للمؤسس، يجب أن يجتاز فحوص [../distribution/DRAFT_QUALITY_POLICY_AR.md](../distribution/DRAFT_QUALITY_POLICY_AR.md): لا ضمان، لا «100%»، لا «نضمن»، لا ROI بلا دليل، لا PII زائدة، ليس طويلاً مزعجاً، لا قناة محظورة، لا ادعاء بلا مستوى دليل. أي مخالفة تُسجَّل في `quality_issues` وتمنع الوصول لحالة `approved`.

Before reaching the founder, every deliverable must pass the checks in [../distribution/DRAFT_QUALITY_POLICY_AR.md](../distribution/DRAFT_QUALITY_POLICY_AR.md). Any violation is logged in `quality_issues` and blocks `approved`.

---

## قواعد ملزمة / Binding rules

1. لا إرسال خارجي بلا `approved`. / No external send without `approved`.
2. لا تحصيل مالي بواسطة الذكاء الاصطناعي. / No charging by the AI.
3. لا PII (بريد/هاتف/هوية/أسماء حقيقية) في السجلات. / No PII in logs.
4. كل مخرج مربوط بمنتج (`product_id`) ومستوى دليل (`evidence_level`). / Every deliverable links to a product and an evidence level.
5. القرار النهائي للمؤسس في كل حالة سعر/إرسال/تسليم/دفع. / Founder holds the final decision on price/send/delivery/payment.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
