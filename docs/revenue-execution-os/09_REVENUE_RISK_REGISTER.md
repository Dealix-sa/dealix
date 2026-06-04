# Revenue Risk Register — سجل مخاطر الإيرادات

## الغرض (AR)
يوثّق هذا المستند المخاطر التي قد تهدد الإيرادات أو سلامة النظام، مع احتمالها وأثرها وإجراءات التخفيف والمسؤول عنها. الهدف هو إدارة استباقية للمخاطر دون أي تجاوز لقواعد السلامة.

## Purpose (EN)
This document records the risks that could threaten revenue or system safety, with likelihood, impact, mitigation, and owner. The aim is proactive risk management with zero compromise on safety rules.

## مفتاح التقييم / Rating Key
- الاحتمال / Likelihood: منخفض / متوسط / عالٍ (Low / Medium / High)
- الأثر / Impact: منخفض / متوسط / عالٍ (Low / Medium / High)

## سجل المخاطر / Risk Register

| المخاطرة / Risk | الاحتمال / Likelihood | الأثر / Impact | التخفيف / Mitigation | المسؤول / Owner |
|---|---|---|---|---|
| إرسال خارجي تلقائي عن طريق الخطأ / Accidental automated sending | منخفض / Low | عالٍ / High | لا قنوات إرسال في الكود؛ تحقق آلي؛ تنفيذ يدوي فقط / No send channels in code; automated verify; manual-only | المؤسس / Founder |
| ادعاءات غير مثبتة أو ضمان عائد / Unproven claims or ROI guarantees | متوسط / Medium | عالٍ / High | قوالب خالية من الضمانات؛ مراجعة المؤسس لكل مسودة / Guarantee-free templates; founder review | المؤسس / Founder |
| تسرب بيانات العميل في أصول الإثبات / Client data leak in proof assets | متوسط / Medium | عالٍ / High | إخفاء الهوية؛ موافقة قبل النشر / Anonymization; consent before publishing | المؤسس / Founder |
| ملاحقة فرص ضعيفة / Chasing weak opportunities | عالٍ / High | متوسط / Medium | بوابة الجودة وحد الجمود / Quality gate and stall threshold | المؤسس / Founder |
| تعثر الصفقات في مرحلة واحدة / Deals stuck at one stage | متوسط / Medium | متوسط / Medium | مراقبة stuck_stage أسبوعيًا / Weekly stuck_stage monitoring | المؤسس / Founder |
| اعتماد مفرط على قطاع واحد / Over-reliance on one vertical | متوسط / Medium | عالٍ / High | تنويع القطاعات؛ مراقبة top_vertical / Diversify; monitor top_vertical | المؤسس / Founder |
| كشف أسرار أو مفاتيح / Secrets/keys exposure | منخفض / Low | عالٍ / High | لا أسرار في المستودع؛ فحص آلي / No secrets in repo; automated scan | المؤسس / Founder |
| فشل التسليم بعد البيع / Delivery failure after sale | متوسط / Medium | عالٍ / High | نطاق محدد ومعايير نجاح مكتوبة / Fixed scope and written success criteria | المؤسس / Founder |

## مبادئ التخفيف / Mitigation Principles
- **الوقاية بالتصميم** / Prevention by design: لا قنوات إرسال خارجية في الكود أصلًا.
- **التحقق الآلي** / Automated verification: يُشغّل `scripts/revenue_execution_verify.py` للكشف عن أي انحراف.
- **حاجز المؤسس** / Founder gate: كل إجراء خارجي يمرّ بموافقة بشرية صريحة.
- **التوثيق اليدوي** / Manual attestation: كل حدث يُسجّل بأحرف المؤسس الأولى.

The strongest mitigation is structural: there are no external send channels in the code, automated verification catches drift, the founder gate requires explicit human approval, and every event carries a manual attestation.

## المراجعة / Review
يُراجَع هذا السجل في المراجعة الأسبوعية للإيرادات، وتُحدَّث الحالات والمخففات والمسؤولون، وتُضاف مخاطر جديدة عند ظهورها.
This register is reviewed in the weekly revenue review; statuses, mitigations, and owners are updated, and new risks are added as they emerge.

## السلامة / Safety
لا تبرّر أي مخاطرة تجاوز قواعد السلامة: لا إرسال تلقائي، لا كشط، لا ضمانات، لا أسرار، مهما كانت قيمة الفرصة.
No risk justifies bypassing the safety rules: no auto-sending, no scraping, no guarantees, no secrets, regardless of opportunity value.
