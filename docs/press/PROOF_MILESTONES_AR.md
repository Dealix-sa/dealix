# معالم الإثبات — Proof Milestones

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المالك:** المؤسس (سامي)
**يُغذّي:** docs/press/PRESS_OUTREACH_OS_AR.md (المحفّزات) و docs/BRAND_PRESS_KIT.md §8 (القواعد الصارمة).
**آخر تحديث:** 2026-06-02

---

## الغرض

ربط كل معلَم **قابل للتحقّق** بالمحفّز الإعلامي الذي يفتحه. القاعدة الواحدة الحاكمة: **لا يُعلَن شيء قبل أن يصبح صحيحاً.** لا «N عميل» قبل أن يدفع N. لا «أول شريك» قبل توقيع أول شريك.

## جدول المعالم → المحفّزات

| المعلَم | الشرط القابل للتحقّق | حالة النظام | المحفّز الإعلامي المفتوح |
|---------|----------------------|-------------|--------------------------|
| المنتج جاهز هندسياً | الخدمات LIVE + بوّابات الأمان مفروضة في الكود | سجل الـ registry | سيرة «منتج جاهز» (لا إعلان مبيعات) |
| أول 3 تجارب مدفوعة | 3 عملاء `payment_confirmed` | سجل العملاء | محفّز «أول شركاء تأسيس» |
| أول حزمة إثبات | حزمة 14 قسماً مُسلَّمة + إذن نشر موقّع | سجل التسليم | محفّز «منهجية الإثبات» + دراسة حالة |
| 10 عملاء مدفوعين | 10 عملاء `payment_confirmed` | سجل العملاء | محفّز «نموّ بصفر cold outreach» |
| أول تجديد شريك | شريك جدّد بعد دورة كاملة | سجل الشركاء | محفّز «نموذج شراكة مستدام» + يفتح زاوية Magnitt |
| معلَم امتثال سعودي | تسجيل/مراجعة منظِّم مكتملة وموثّقة | وثيقة المنظِّم | محفّز «الامتثال كميزة معمارية» |

## قاعدة الصدق (Honesty Gate)

- **العدّ يطابق الواقع.** الرقم المُعلَن = عدد العملاء بحالة `payment_confirmed`، لا أكثر.
- **«صفر» يُقال مباشرة.** قبل أول عميل، الجواب الصحيح في أي مقابلة: «لا عملاء مدفوعين بعد» — صدق لا ضعف (يطابق docs/BRAND_PRESS_KIT.md §6).
- **لا أرقام معايير مُختلَقة.** إن لم تكن البيانات موجودة: «لا نملك بيانات على ذلك بعد».
- **لا أسماء بلا إذن.** اسم أي عميل في أي تغطية يتطلّب `signed_publish_permission`.
- **لا ضمانات.** النتائج تقديرية والإثبات موثَّق؛ لا «نضمن» ولا أرقام مبيعات كحقيقة.

## التحقّق قبل الإعلان

قبل فتح أي محفّز إعلامي:

1. أكّد الشرط القابل للتحقّق من سجل النظام المذكور أعلاه (لا تقدير، لا «قريباً»).
2. تأكّد من إذن النشر إن كان المعلَم يخصّ عميلاً.
3. سجّل تاريخ التحقّق، ثمّ افتح الحملة عبر docs/press/PRESS_OUTREACH_OS_AR.md.

## الخطوة التالية

عند اقتراب أي معلَم: راقب الشرط القابل للتحقّق، ولا تجهّز طرحاً إعلامياً قبل أن يتحوّل الشرط من «متوقَّع» إلى «محقَّق» في سجل النظام.

## English summary

This doc maps each verifiable milestone to the press trigger it unlocks, governed by one rule: nothing is announced before it is true. Engineering-complete unlocks a "product ready" bio (not a sales claim); first 3 payment-confirmed customers unlock the "founding partners" trigger; a delivered, publish-approved Proof Pack unlocks the methodology and case-study triggers; 10 payment-confirmed customers unlock "growth with zero cold outreach"; a first partner renewal unlocks the sustainable-partnership angle (and the Magnitt funding-readiness angle); a documented Saudi compliance milestone unlocks the compliance-as-architecture angle. The honesty gate is strict: announced counts equal payment-confirmed counts only, "zero" is said plainly when true, no invented benchmarks, no customer names without signed publish permission, no guarantees. Verify the condition from the system record before opening any campaign via docs/press/PRESS_OUTREACH_OS_AR.md.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
