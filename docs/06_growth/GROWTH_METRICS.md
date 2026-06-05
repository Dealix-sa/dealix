# Growth Metrics — مقاييس النمو

ما لا يُقاس لا يُحسّن. هنا أحداث التتبّع، نسب القمع وأهدافها، ولوحات القيادة اليومية والأسبوعية. الأرقام للقرار، والأهداف تقديرات تشغيلية لا وعود.

> القاعدة: كل هدف رقم موسوم "تقدير تشغيلي وليس وعدًا بنتيجة". نقيس لنقرّر، لا لنزيّن. لا تتبّع ينتهك PDPL — لا بيانات شخصية تُستخدم للتدريب.

---

## 1) قائمة أحداث التحليلات

| الحدث | متى يُسجّل |
| --- | --- |
| `tool_started` | بدء الزائر لأي أداة مجانية |
| `tool_completed` | إكمال الأداة وعرض الدرجة |
| `score_viewed` | مشاهدة الدرجة وأضعف 3 محاور |
| `sample_viewed` | مشاهدة Sample Output |
| `diagnostic_requested` | حجز Free Diagnostic |
| `diagnostic_completed` | إتمام جلسة Diagnostic |
| `sprint_checkout_started` | بدء دفع Command Sprint |
| `sprint_paid` | دفع Sprint مؤكّد |
| `sprint_delivered` | تسليم مخرجات Sprint الأربعة |
| `proof_pack_reviewed` | مراجعة Proof Pack مع العميل |
| `managed_started` | بدء اشتراك Managed |
| `referral_requested` | طلب إحالة (بعد Proof) |

---

## 2) نسب القمع وأهدافها

| النسبة | الهدف | تقدير تشغيلي |
| --- | --- | --- |
| Tool completion (started → completed) | 40%+ | ✓ |
| Score → Diagnostic | 5–15% | ✓ |
| Diagnostic → Sprint | 20–40% | ✓ |
| Sprint → Managed | 20–30% | ✓ |
| Client → Referral | 20%+ | ✓ |

أي نسبة تحت الهدف = موضوع لتجربة في [GROWTH_EXPERIMENTS.md](./GROWTH_EXPERIMENTS.md).

---

## 3) لوحة القيادة اليومية

| المؤشر | لماذا يوميًا |
| --- | --- |
| أدوات بدأت / اكتملت | نبض أعلى القمع |
| Diagnostics محجوزة | إشارة طلب فوري |
| Sprints مدفوعة | إيراد اليوم |
| تسليمات قيد التنفيذ | حمل التشغيل اليدوي |

---

## 4) لوحة القيادة الأسبوعية

| المؤشر | القرار المرتبط |
| --- | --- |
| كل نسب القمع الخمس | أين الاختناق هذا الأسبوع؟ |
| أعلى مصدر للـ Scores | ضاعف القناة الفائزة |
| Sprint → Managed | جودة التسليم و Proof Pack |
| عدد Referrals | صحّة الثقة بعد Proof |
| نتائج التجارب الـ10 | نُبقي / نوقف / نوسّع |

---

## الحواجز في هذه الصفحة

- لا أرقام CRM مختلقة في اللوحات.
- كل هدف موسوم تقدير تشغيلي.
- لا تتبّع ينتهك PDPL.

روابط: [GROWTH_EXPERIMENTS.md](./GROWTH_EXPERIMENTS.md) · [WEBSITE_FUNNEL_MAP.md](./WEBSITE_FUNNEL_MAP.md) · [CONVERSION_PLAYBOOK.md](./CONVERSION_PLAYBOOK.md)

> **CTA واحد:** اقرأ اللوحة، اختر الاختناق، شغّل تجربة لرفع التحويل نحو Score / Diagnostic / Sprint.
