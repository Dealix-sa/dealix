# Ads Readiness Gate — بوابة جاهزية الإعلانات

> Cross-link: [Ads OS](10_ADS_OS.md), [Brand Voice](01_BRAND_VOICE.md), [Social Metrics](14_SOCIAL_METRICS.md).

## English — Purpose

No paid ad goes live until every item below passes and the compliance owner signs off. Ads are **not launched from the repo**. This gate is the single approval point. A failure on any line is a hard stop.

## العربية — الغرض

لا يُطلق أي إعلان مدفوع حتى يجتاز كل بند أدناه ويعتمد مالك الامتثال. الإعلانات **لا تُطلق من المستودع**. هذه البوابة نقطة الاعتماد الوحيدة. فشل أي سطر يعني توقّفًا صارمًا.

## English — The Gate Checklist

| # | Check | Pass condition |
|---|---|---|
| 1 | Tracking installed | Tags fire correctly in a test environment |
| 2 | Consent banner | Loads before any tracking, on every landing page |
| 3 | Conversion events defined | `lead_form_submit`, `qualified_reply`, `meeting_booked` validated |
| 4 | UTM taxonomy applied | Every link follows [Ads OS](10_ADS_OS.md) format |
| 5 | Claims reviewed | No forbidden claims; modest, qualified wording |
| 6 | Disclosure present | Standard disclosure above the fold on each landing page |
| 7 | Landing page QA | Loads on mobile + desktop; forms submit; no broken links |
| 8 | Budget caps set | Daily and monthly caps configured per scenario |
| 9 | Compliance owner sign-off | Founder records explicit approval per creative |
| 10 | Negative keywords loaded | Search campaigns include the negative list |

## العربية — قائمة البوابة

| # | الفحص | شرط النجاح |
|---|---|---|
| 1 | تركيب التتبّع | الوسوم تعمل بشكل صحيح في بيئة اختبار |
| 2 | لافتة الموافقة | تظهر قبل أي تتبّع على كل صفحة هبوط |
| 3 | تعريف أحداث التحويل | `lead_form_submit`، `qualified_reply`، `meeting_booked` مُتحقَّقة |
| 4 | تطبيق تصنيف UTM | كل رابط يتبع صيغة [نظام الإعلانات](10_ADS_OS.md) |
| 5 | مراجعة الادعاءات | بلا ادعاءات محظورة؛ صياغة متواضعة ومُحدَّدة |
| 6 | وجود الإفصاح | الإفصاح المعياري أعلى كل صفحة هبوط |
| 7 | فحص صفحة الهبوط | تعمل على الجوال والحاسب؛ النماذج تُرسل؛ بلا روابط مكسورة |
| 8 | ضبط سقوف الميزانية | سقف يومي وشهري مُعَدّ حسب السيناريو |
| 9 | اعتماد مالك الامتثال | المؤسس يسجّل اعتمادًا صريحًا لكل إبداع |
| 10 | تحميل الكلمات السلبية | حملات البحث تتضمّن القائمة السلبية |

## English — Launch No-Go Conditions (Hard Stop)

Do not launch if any is true:
- Tracking unverified or consent banner missing.
- Any forbidden claim present (guaranteed ROI, "100%", "replace your team", "automate everything", "no human needed", fake urgency).
- Landing page missing the standard disclosure.
- Conversion events undefined or unvalidated.
- No budget cap set.
- No recorded compliance owner sign-off.
- Any PII or named customer used without written consent.

## العربية — شروط عدم الإطلاق (توقّف صارم)

لا تُطلق إذا تحقّق أيٌّ مما يلي:
- التتبّع غير مُتحقَّق أو لافتة الموافقة غائبة.
- وجود أي ادعاء محظور (عائد مضمون، "100%"، "استبدل فريقك"، "أتمتة كل شيء"، "بلا بشر"، إلحاح زائف).
- صفحة الهبوط بلا الإفصاح المعياري.
- أحداث التحويل غير معرَّفة أو غير مُتحقَّقة.
- بلا سقف ميزانية.
- بلا اعتماد مُسجَّل لمالك الامتثال.
- استخدام أي بيانات شخصية أو عميل مسمّى دون موافقة مكتوبة.

## English — Sign-Off Block (To Be Completed Manually)

- Compliance owner (founder): __________
- Date: __________
- Campaign reviewed: __________
- Result: PASS / NO-GO

## العربية — خانة الاعتماد (تُكمَل يدويًا)

- مالك الامتثال (المؤسس): __________
- التاريخ: __________
- الحملة المُراجَعة: __________
- النتيجة: اجتياز / عدم إطلاق

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
