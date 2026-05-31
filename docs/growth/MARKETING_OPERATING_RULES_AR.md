# Marketing Operating Rules — قواعد تشغيل التسويق

> Section 49. تسع قواعد تشغيليّة، كل قاعدة لها: rule، rationale، violation pattern، fix.
> Module path: `dealix/growth_os/marketing_rules/`

---

## مقدّمة — Introduction

التسويق في Dealix يخضع لـ نفس حوكمة التسليم. كل قاعدة من التسع أدناه ملزمة، ولها فحص آلي/يدوي في `growth_os_master_verify`.

---

## Rule 1 — No content without CTA — لا محتوى بدون دعوة

- **Rule.** كل أصل محتوى ينتهي بـ CTA واحد محدَّد.
- **Rationale.** القارئ يحتاج خطوة تالية. المحتوى بلا CTA يستهلك وقت بلا قياس.
- **Violation looks like.** مقال ينتهي بـ "شكراً للقراءة" أو سؤال مفتوح بلا رابط.
- **Fix.** أضف CTA يربط بـ OfferCard موجود + UTM tag.

---

## Rule 2 — No CTA without an offer — لا دعوة بدون عرض

- **Rule.** كل CTA يقود إلى OfferCard معتمد.
- **Rationale.** CTA يقود إلى "تواصل معنا" فقط يخفّض conversion ويُربك الـ attribution.
- **Violation looks like.** "احجز مكالمة" بلا تحديد ما الذي يحدث في المكالمة.
- **Fix.** اربط الـ CTA بـ offer محدَّد: "احجز Governance Snapshot — تقرير 14 يوم."

---

## Rule 3 — No offer without tracking — لا عرض بدون تتبّع

- **Rule.** كل OfferCard له UTM tags + attribution_tag + tracking link مُسجَّل.
- **Rationale.** بدون tracking، لا attribution. بدون attribution، لا قرار scale/kill.
- **Violation looks like.** OfferCard منشور بلا campaign_id ولا UTMs ثابتة.
- **Fix.** سجّل tracking عند إنشاء OfferCard، ارفض النشر بلا فحص.

---

## Rule 4 — No tracking without outcome — لا تتبّع بدون نتيجة

- **Rule.** كل tracking link يُراجَع شهريّاً مقابل نتيجة (meeting / proposal / revenue).
- **Rationale.** tracking بلا review يصبح ضوضاء.
- **Violation looks like.** UTM تحت كل أصل لكنّ التقارير الشهريّة لا تُفتح.
- **Fix.** ضع review شهري على التقويم. أصول بلا outcome 90 يوم → retire أو optimize.

---

## Rule 5 — No claim without source — لا ادعاء بدون مصدر

- **Rule.** كل رقم، إحصائيّة، أو ادعاء له مصدر علني أو تصنيف "estimated".
- **Rationale.** Claim-safety = الأساس القانوني والثقة التسويقيّة.
- **Violation looks like.** "70% من الشركات تستخدم AI" بلا رابط مصدر.
- **Fix.** أضف الرابط، أو حوّل الجملة إلى تقديريّة موسومة، أو احذفها.

---

## Rule 6 — No customer name without consent — لا اسم عميل بدون إذن

- **Rule.** اسم العميل العلني (حالة، شعار، اقتباس) يحتاج إذن مكتوب موقَّع.
- **Rationale.** PDPL + ثقة العميل + سمعة Dealix.
- **Violation looks like.** شعار عميل في صفحة hero بلا email موافقة محفوظ.
- **Fix.** ConsentRecord لكل استخدام علني. بدون consent → استخدم "Agency X".

---

## Rule 7 — No external send without human approval — لا إرسال خارجي بلا موافقة بشرية

- **Rule.** كل رسالة خارجيّة (DM, email, WhatsApp) تمرّ بموافقة المؤسس أو مفوَّض.
- **Rationale.** يمنع automation drift + يحمي العلاقات + يُلزم بـ Constitution.
- **Violation looks like.** Agent يرسل مباشرة بلا approval_log.
- **Fix.** اربط الإرسال بـ governance gate. agent يكتب، إنسان يضغط "أرسل".

---

## Rule 8 — No paid before organic validation — لا مدفوع قبل التحقّق العضوي

- **Rule.** لا حملة مدفوعة لـ offer لم يُبَع organically 3 مرّات على الأقل.
- **Rationale.** المدفوع يضخّم. يضخّم الجيد والسيّئ بنفس القوّة. validate أوّلاً.
- **Violation looks like.** صرف على LinkedIn Sponsored لعرض جديد بلا close واحد سابق.
- **Fix.** أرجع الميزانية. شغّل ABM لـ 30 يوم. ادفع فقط بعد 3 closes.

---

## Rule 9 — No vanity metric on a leadership slide — لا مؤشّر استعراضيّ في شريحة قيادة

- **Rule.** Founder dashboard + leadership decks لا تحتوي followers، likes، أو impressions.
- **Rationale.** القرار يُتَّخذ على pipeline + revenue + RQS، لا على virality.
- **Violation looks like.** شريحة "وصلنا لـ 10K متابع" في monthly review.
- **Fix.** استبدل بـ "10K visit → 120 meeting request → 14 signed sprint" — مع attribution.

---

## فحص الامتثال — Compliance Self-Check

كل أصل/حملة قبل النشر يُجيب على 9 أسئلة:

1. هل يوجد CTA؟
2. هل CTA مرتبط بـ OfferCard؟
3. هل tracking مُسجَّل؟
4. هل في تقويم review شهري؟
5. هل كل ادعاء موصوف بمصدر؟
6. هل أسماء العملاء بإذن أو anonymized؟
7. هل الإرسال الخارجي يمرّ بموافقة بشريّة؟
8. هل المدفوع مسبوق بـ 3 closes organic؟
9. هل المؤشّرات قراريّة لا استعراضيّة؟

9/9 → ينشر. أقل → لا.

---

## How to verify

```bash
bash scripts/growth_os_master_verify.sh
```

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
