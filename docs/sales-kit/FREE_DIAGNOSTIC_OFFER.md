# Free Mini Diagnostic — التشخيص المصغّر المجاني (Rung 0)

> **دكترين (2026-05-18):** Dealix = عمليات إيراد و AI مُحوكَمة. النظام يحلّل
> ويرتّب ويصيغ المسودات؛ المؤسس/العميل يراجع ويعتمد كل إجراء خارجي. لا مندوب
> آلي، لا إرسال تلقائي، لا وعود بأرقام. التشخيص مجاني (0 ريال)؛ السبرنت بعده
> خياري (499 ريال). النتائج التقديرية ليست نتائج مضمونة.
>
> Cross-link: [START_HERE.md](START_HERE.md) · [WARM_LIST_WORKFLOW.md](WARM_LIST_WORKFLOW.md) · [QUALIFICATION_CHECKLIST.md](QUALIFICATION_CHECKLIST.md) · [dealix_demo_script_30min.md](dealix_demo_script_30min.md) · [dealix_pilot_agreement.md](dealix_pilot_agreement.md)

---

## 1. ما هو التشخيص المجاني — What it is

**العربية:** التشخيص المصغّر المجاني هو أول مخرج ملموس يستلمه العميل المحتمل.
موجز ثنائي اللغة، يُسلَّم خلال 24 ساعة من استلام نموذج الطلب، يُظهر للعميل
أين الإيراد المتسرّب في عمليته الحالية — قبل أي التزام مالي. الغرض منه إثبات
القيمة، لا البيع. إن ناسب العميل، يُختَم الموجز بدعوة لسبرنت إثبات الإيراد
499 ريال (rung 1).

**English:** The Free Mini Diagnostic is the first tangible deliverable a
prospect receives. A bilingual brief, delivered within 24 hours of intake
submission, showing the customer where revenue is leaking in their current
motion — before any financial commitment. Its purpose is to prove value, not
to sell. If it fits, the brief closes with an invitation to the 499 SAR
7-Day Revenue Proof Sprint (rung 1).

---

## 2. الحدود — Scope and exclusions

**يشمل / Includes:**
- مراجعة لعينة واحدة من قائمة فرص العميل (حتى 10 حسابات).
- تحديد 3 نقاط تسرّب إيراد قابلة للمعالجة.
- توصية واحدة واضحة: هل السبرنت يناسبكم الآن، أو لاحقاً، أو لا.
- نسخة عربية أساسية + نسخة إنجليزية.

**لا يشمل / Excludes:**
- لا scraping، لا تجميع قوائم، لا إثراء بيانات من مصادر غير مملوكة للعميل.
- لا تواصل بارد نيابة عن العميل، لا واتساب آلي، لا أتمتة LinkedIn.
- لا وعود برقم إيراد، لا ضمان نتائج، لا "1 ريال" كسعر معروض.
- لا إرسال خارجي — كل مخرج مسودة باعتماد بشري.
- لا عمل من الطبقات 2–5 ضمن هذا التشخيص.

---

## 3. مسار التسليم — Delivery path

| الخطوة | المسؤول | المدة |
|---|---|---|
| 1. العميل يقول "نعم، أرسل التفاصيل" بعد رسالة القائمة الدافئة | المؤسس | — |
| 2. المؤسس يرسل رابط نموذج طلب التشخيص | المؤسس | فوري |
| 3. العميل يعبّئ النموذج (قطاع، حجم، مشكلة، تأكيد ملكية البيانات، الموافقة) | العميل | — |
| 4. تأكيد استلام تلقائي (transactional، مُدرَج في القائمة البيضاء) | النظام | فوري |
| 5. المؤسس يشغّل `qualification.qualify(...)` — انظر [QUALIFICATION_CHECKLIST.md](QUALIFICATION_CHECKLIST.md) | المؤسس | < 24 ساعة |
| 6. يُولَّد الموجز التشخيصي ثنائي اللغة، المؤسس يراجع ويعتمد | المؤسس | < 24 ساعة من الطلب |
| 7. الموجز يُرسَل، يتضمن دعوة سبرنت 499 ريال إن كانت التوصية ACCEPT | المؤسس | — |

عند القرار `DIAGNOSTIC_ONLY`: يُسلَّم التشخيص بدون دعوة سبرنت؛ حقل التوصية
في الموجز يقرّر هل تُرسَل الدعوة لاحقاً.

---

## 4. عرض التشخيص في رسالة — The offer line

تُستخدم فقط بعد رد "أخبرني أكثر" من جهة في القائمة الدافئة.

**العربية:**
> التشخيص المجاني يُسلَّم خلال 24 ساعة، ثنائي اللغة، باعتمادي الشخصي. يُظهر
> لكم أين يتسرّب الإيراد في عمليتكم الحالية. لا التزام مالي. إن ناسبكم بعده،
> هناك سبرنت إثبات إيراد 7 أيام بـ 499 ريال — خياري تماماً.

**English:**
> The free diagnostic is delivered in 24 hours, bilingual, with my personal
> sign-off. It shows you where revenue leaks in your current motion. No
> financial commitment. If it fits afterward, there is a 7-day Revenue Proof
> Sprint at 499 SAR — entirely optional.

---

## 5. ما الذي يحوّل التشخيص إلى سبرنت — Diagnostic to Sprint gate

التشخيص يدعو إلى السبرنت **فقط** عند توفّر إشارات rung 1 من
[QUALIFICATION_CHECKLIST.md](QUALIFICATION_CHECKLIST.md):
- ألم واضح + مالك قرار حاضر + بيانات جاهزة.
- العميل يقبل الحوكمة ولا يطلب طرقاً غير آمنة.

عند القبول، يقدّم الموجز عرض سبرنت 499 ريال بشروط 50/50 (50% عند القبول،
50% عند تسليم حزمة الإثبات) — التفاصيل في [dealix_pilot_agreement.md](dealix_pilot_agreement.md).

---

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
