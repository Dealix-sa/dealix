# تعلُّم الربح والخسارة — Dealix Win/Loss Learning

هذا الملف يحدّد **الحقول المسجَّلة** عند كل نتيجة و**الأسئلة الأسبوعية**. الكيان `win_loss` يحمل الحقول حرفياً: `id`, `company`, `sector`, `offer`, `channel`, `outcome`, `reason`, `objection`, `lesson`, `next_change`.

This file defines the **fields logged** for every outcome and the **weekly questions**. The `win_loss` entity carries the fields above verbatim.

روابط / Related: [PROSPECT_OS_AR.md](PROSPECT_OS_AR.md) · [DISTRIBUTION_METRICS_AR.md](DISTRIBUTION_METRICS_AR.md) · [../commercial/OFFER_LADDER_AR.md](../commercial/OFFER_LADDER_AR.md) · [REVENUE_EXECUTION_OS_AR.md](REVENUE_EXECUTION_OS_AR.md)

---

## الحقول المسجَّلة / Fields logged

يُسجَّل كل عميل وصل إلى `won` أو `lost` (راجع [PROSPECT_OS_AR.md](PROSPECT_OS_AR.md)):

Every prospect that reached `won` or `lost` is logged:

| الحقل / Field | الوصف / Description |
|---|---|
| `id` | معرّف السجل. / Record id. |
| `company` | اسم/تسمية مجهَّلة للشركة (لا PII). / Anonymized company label (no PII). |
| `sector` | القطاع. / Sector. |
| `offer` | العرض المربوط بمنتج كتالوج. / The offer, linked to a catalog product. |
| `channel` | القناة التي قادت النتيجة. / The channel that led to the outcome. |
| `outcome` | `won` أو `lost`. / `won` or `lost`. |
| `reason` | السبب الرئيسي للنتيجة. / The main reason. |
| `objection` | الاعتراض الأبرز إن وُجد. / The key objection, if any. |
| `lesson` | الدرس المستخلَص. / The lesson learned. |
| `next_change` | التغيير العملي التالي في المنظومة. / The next concrete change to the system. |

> لا أسماء أفراد ولا بيانات تعريف؛ تُستخدَم تسميات مجهَّلة على مستوى الشركة. / No individual names or identifiers; anonymized company-level labels only.

---

## الأسئلة الأسبوعية / Weekly questions

تُراجَع كل أسبوع لتحويل النتائج إلى تحسين:

Reviewed weekly to turn outcomes into improvement:

1. أي عروض ربحنا بها هذا الأسبوع، ولماذا؟ / Which offers won this week, and why?
2. أي عروض خسرنا، وما السبب الجذري (`reason`)؟ / Which lost, and what was the root cause?
3. ما الاعتراض المتكرّر (`objection`) الذي يجب أن نعالجه في المسودات/العروض؟ / Which recurring objection should we address in drafts/proposals?
4. أي قناة (`channel`) تعطي أفضل النتائج بلا مخاطر امتثال؟ / Which channel performs best without compliance risk?
5. أي قطاع (`sector`) يُظهِر نمطاً يستحق تركيزاً؟ / Which sector shows a pattern worth focus?
6. ما الدرس (`lesson`) الأهم، وما التغيير التالي (`next_change`)؟ / What is the top lesson and the next change?
7. هل أي خسارة سببها سعر خارج النطاق أو وعد لا ندعمه؟ / Did any loss stem from out-of-band price or an unsupported promise?
8. ما الذي نوقفه أو نضاعفه الأسبوع القادم؟ / What do we stop or double down on next week?

---

## كيف يُغذّي التحسين / How it feeds improvement

- `objection` المتكرّر ⇒ تحديث [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md) أو زوايا العرض. / Recurring objections update draft angles.
- `reason` لخسارة السعر ⇒ مراجعة مع [../commercial/PRICING_GUARDRAILS_AR.md](../commercial/PRICING_GUARDRAILS_AR.md) (لا كسر للأرضية). / Price-loss reasons reviewed against guardrails (no floor break).
- `next_change` ⇒ بند في [DISTRIBUTION_METRICS_AR.md](DISTRIBUTION_METRICS_AR.md) للأسبوع التالي. / Next change becomes a metric item for the following week.

---

## قواعد ملزمة / Binding rules

1. لا PII في سجل الربح/الخسارة. / No PII in the win/loss record.
2. كل `offer` مربوط بمنتج كتالوج. / Every offer links to a catalog product.
3. لا تفسير خسارة بادعاء غير مدعوم؛ السبب واقعي وموثَّق. / No loss explained by an unsupported claim.
4. الدروس تتحول إلى تغييرات عملية لا شعارات. / Lessons become concrete changes, not slogans.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
