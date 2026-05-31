## قالب قصص العملاء — Case Study Template (AR)

كل قصة عميل في ديلكس مبنية على هيكل ستّ مراحل: قبل / فعل / مخرج / نتيجة / تعلّم / تالٍ. لكل مرحلة فقرة عربية + إنجليزية متوازية، وكل رقم يستخدم Jinja2 placeholder. لا يُذكر اسم عميل حقيقي بلا إذن خطّي، وكل قصة بدون إذن تحمل تسمية "قالب آمن للحالة / Case-safe template".

### Jinja2 Placeholders (إلزامية)

```yaml
case_study_fields:
  customer_name: "{{customer_name}}"          # اسم العميل أو "عميل سعودي في قطاع X"
  sector: "{{sector}}"                          # القطاع
  tenant_id: "{{tenant_id}}"                    # معرّف tenant داخل ديلكس
  deal_value_sar: "{{deal_value_sar}}"          # قيمة الصفقة بالريال
  baseline_metric: "{{baseline_metric}}"        # المقياس قبل
  post_metric: "{{post_metric}}"                # المقياس بعد
  evidence_pack_url: "{{evidence_pack_url}}"    # رابط حزمة الأدلة
  offer_id: "{{offer_id}}"                      # العرض المُستخدم
  duration_days: "{{duration_days}}"            # مدة التنفيذ بالأيام
  consent_status: "{{consent_status}}"          # named | anonymized | case-safe
```

---

### Before — قبل (AR)

في {{sector}}، كان {{customer_name}} يواجه: [وصف الألم في 2–3 جملة]. خط الأساس: {{baseline_metric}}. لم يكن هناك سجل أدلة لقرارات AI، ولا مالك تنفيذ يومي.

### Before — Before (EN)

In {{sector}}, {{customer_name}} faced: [2–3 sentence pain description]. Baseline: {{baseline_metric}}. There was no evidence ledger for AI decisions and no daily execution owner.

---

### Action — فعل (AR)

اعتمد العميل {{offer_id}} خلال {{duration_days}} يوماً. الخطوات: [3–5 خطوات مرتّبة]. كل قرار سُجِّل في {{evidence_pack_url}}، وكل وكيل AI مرّ بـ Permission Matrix قبل التشغيل.

### Action — Action (EN)

The customer adopted {{offer_id}} over {{duration_days}} days. Steps: [3–5 ordered steps]. Every decision was logged in {{evidence_pack_url}}, and every AI agent passed through the Permission Matrix before activation.

---

### Output — مخرج (AR)

المخرجات الملموسة: [قائمة 3–5 مخرجات قابلة للقياس، مثلاً: 10 فرص محكومة، Permission Matrix بـ 14 صفّاً، تقرير تنفيذي ربعي]. كل مخرج له ملف ومالك ومراجعة.

### Output — Output (EN)

Tangible outputs: [list 3–5 measurable outputs, e.g. 10 governed opportunities, a 14-row Permission Matrix, a quarterly executive report]. Each output has a file, an owner, and a review.

---

### Outcome — نتيجة (AR)

النتيجة بعد {{duration_days}} يوماً: {{post_metric}} مقابل {{baseline_metric}}. القيمة المُسجَّلة: {{deal_value_sar}} ريالاً. **القيمة التقديرية ليست قيمة مُتحقَّقة** — التحقق يتم عبر سجل أدلة العميل، وأي تعميم خارج هذه الحالة يحتاج تكرار في ≥ 3 حالات.

### Outcome — Outcome (EN)

Outcome after {{duration_days}} days: {{post_metric}} vs {{baseline_metric}}. Recorded value: {{deal_value_sar}} SAR. **Estimated value is not Verified value** — verification runs via the customer's evidence ledger, and any generalization beyond this case requires replication in ≥ 3 cases.

---

### Learning — تعلّم (AR)

ما تعلّمناه: [2–3 دروس صريحة، بما فيها ما لم يعمل]. سنحدّث: [قاعدة Scale/Kill المُعدَّلة، أو قالب قابل لإعادة الاستخدام].

### Learning — Learning (EN)

What we learned: [2–3 explicit lessons, including what didn't work]. We will update: [the revised Scale/Kill rule or a reusable template].

---

### Next — تالٍ (AR)

الخطوة التالية مع العميل: [توسيع لـ Offer التالي، أو تجديد، أو إغلاق بإذن]. الأصل المُعاد توظيفه من هذه القصة: [قالب، شرح، أو منشور].

### Next — Next (EN)

Next step with the customer: [expansion to the next offer, renewal, or closure with consent]. Asset re-deployed from this story: [template, explainer, or post].

---

### قائمة الفحص (Required-Fields Checklist)

قبل النشر، تأكّد من:

- [ ] `consent_status` محدَّد (named / anonymized / case-safe).
- [ ] لا PII (بريد، هاتف، رقم وطني) في النص.
- [ ] كل رقم يستخدم placeholder، لا أرقام مفبركة.
- [ ] `evidence_pack_url` يشير لحزمة موجودة فعلاً.
- [ ] التسمية "قالب آمن للحالة / Case-safe template" حاضرة إذا `consent_status != named`.
- [ ] الإفصاح في نهاية الملف.
- [ ] مراجعة المؤسس قبل النشر العلني.
- [ ] رابط ↔ `docs/revenue_marketing/offers_ladder.md` يحدّد العرض المُستخدم.

---

## مثال داخلي مملوء — Sample Filled Internal Case Study

**Title:** "كيف استخدمنا ديلكس لتوليد 100 lead → 50 رسالة → 10 عروض → {{calls_count}} مكالمة خلال {{duration_days}} يوماً" — قالب آمن للحالة / Case-safe template.

### Before (AR)

في الفترة قبل تشغيل Revenue Marketing Engine، كان فريق ديلكس يعتمد على بحث يدوي للفرص، بلا ترتيب أولويات وبلا سجل أدلة لقرارات الاستهداف. خط الأساس: {{baseline_metric}} (≈ 0 فرصة محكومة موثَّقة شهرياً).

### Before (EN)

Before activating the Revenue Marketing Engine, the Dealix team relied on manual opportunity hunting with no prioritization and no evidence ledger for targeting decisions. Baseline: {{baseline_metric}} (≈ 0 governed documented opportunities per month).

### Action (AR)

شغّلنا الحلقة الكاملة على tenant `{{tenant_id}}` خلال {{duration_days}} يوماً: بناء قائمة 100 شركة دافئة → تطبيق Fit Score → اختيار 50 لمراسلة يدوية → تحويل 10 منها لعروض رسمية.

### Action (EN)

We ran the full loop on tenant `{{tenant_id}}` over {{duration_days}} days: built a warm list of 100 companies → applied Fit Score → selected 50 for manual outreach → converted 10 into formal proposals.

### Output (AR)

- 100 شركة في pipeline موثَّقة.
- 50 رسالة افتتاح يدوية، كل واحدة بسجل.
- 10 عروض رسمية مرسلة (mix من Revenue Hunter Pilot + AI Trust Diagnostic).
- {{calls_count}} مكالمة مكتشفة.
- أصل واحد قابل لإعادة الاستخدام: قالب رسالة افتتاح Revenue Hunter (راجع `docs/revenue_marketing/message_variants.md`).

### Output (EN)

- 100 companies documented in pipeline.
- 50 manual opening messages, each logged.
- 10 formal proposals sent (mix of Revenue Hunter Pilot + AI Trust Diagnostic).
- {{calls_count}} discovery calls.
- One reusable asset: Revenue Hunter opening-message template (see `docs/revenue_marketing/message_variants.md`).

### Outcome (AR)

النتائج: {{post_metric}} مقابل خط الأساس. قيمة الصفقات المفتوحة: {{deal_value_sar}} ريالاً (قيمة تقديرية، ليست مُتحقَّقة بعد). نسبة التحويل من رسالة إلى عرض: 20%، ومن عرض إلى مكالمة: {{call_rate_pct}}%.

### Outcome (EN)

Results: {{post_metric}} vs baseline. Open pipeline value: {{deal_value_sar}} SAR (estimated, not yet verified). Conversion rate from message to proposal: 20%; from proposal to call: {{call_rate_pct}}%.

### Learning (AR)

- التحويل من رسالة → عرض حسّاس لجودة الـ Fit Score؛ كل تعديل وزن أثّر ±5%.
- المتابعة في اليوم +3 رفعت معدّل الردّ بشكل ملحوظ، لكن نحتاج 3 شهور إضافية للتحقّق.
- نموذج White-label الافتراضي لم يصلح للوكالات الصغيرة (<3 موظفين). سنبني نموذج Solo Consultant منفصل.

### Learning (EN)

- Conversion message → proposal is highly sensitive to Fit Score quality; each weight change moved it by ±5%.
- A day-+3 follow-up materially lifted reply rate, but we need 3 more months to verify.
- The default white-label template did not fit micro-agencies (<3 staff). We will build a separate Solo Consultant variant.

### Next (AR)

- توسيع للحملة التالية (200 شركة) في الربع التالي.
- بناء قالب Solo Consultant.
- نشر هذا القالب علناً بعد إخفاء التفاصيل التجارية.

### Next (EN)

- Expand to the next campaign (200 companies) next quarter.
- Build a Solo Consultant template.
- Publish this case publicly after redacting commercial details.

---

**Disclosure / إفصاح:** Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة. Case-safe template / قالب آمن للحالة.

Cross-links: `docs/revenue_marketing/offers_ladder.md`, `docs/revenue_marketing/dashboard_glossary.md`, `docs/revenue_marketing/anti_vanity_rules.md`.
