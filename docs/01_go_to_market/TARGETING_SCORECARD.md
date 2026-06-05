# Targeting Scorecard — بطاقة سكور الاستهداف

> يفرضها: [`scripts/targeting_scorecard.py`](../../scripts/targeting_scorecard.py) ·
> الأوزان: [`data/targeting/scoring_weights.yml`](../../data/targeting/scoring_weights.yml)

## 100 نقطة أساسية

| المحور | النقاط | كيف يُحسب |
|---|---:|---|
| ICP Fit | 25 | تطابق القطاع/المدينة/الحجم مع خطة المرحلة |
| Business Pain Signal | 20 | قوة إشارات الألم الموثّقة (`pain_signals`) |
| Timing / Intent | 15 | توظيف/أخبار/توسع (`intent_signals`) |
| Access / Contactability | 10 | وجود قناة تواصل رسمية قابلة للاستخدام |
| Dealix Fit by OS Layer | 10 | خريطة نظيفة لطبقة Dealix واحدة |
| Evidence Confidence | 10 | عدد واستقلال مصادر الأدلة |
| Strategic Value | 10 | حجم الحساب / قناة شراكة / إمكان توسع |

## الخصومات

| الخطر | الخصم |
|---|---|
| مصدر واحد فقط | −10 |
| بيانات ناقصة | −10 |
| قطاع حساس | −15 |
| لا توجد قناة رسمية | −10 |
| تخمين بدون دليل | −15 |
| مصدر غير مسموح | **Reject** |
| تكرار | **Merge/Reject** |

`Reject` يجبر الدرجة على D والحالة على رفض بغض النظر عن مجموع المحاور.

## بنوك الدرجات

| الدرجة | المدى | القرار |
|---|---|---|
| A+ | 90–100 | راجع اليوم |
| A | 80–89 | هدف قوي |
| B | 70–79 | يحتاج دليلًا إضافيًا |
| C | 60–69 | nurture |
| D | < 60 | لا يُستهدف الآن |

## ملاحظات هندسية

- الدالة `score_company(company, weights, signal_weights)` **نقية وحتمية** — لا
  شبكة ولا آثار جانبية، تُختبر في [`tests/test_targeting_scorecard.py`](../../tests/test_targeting_scorecard.py).
- كل محور يُرجّع كسرًا 0..1 يُضرب في وزنه؛ ثم تُطبّق الخصومات؛ ثم يُقصّ الناتج 0..100.
- أوزان المحاور **يجب أن تساوي 100** (يفرضه اختبار).

## روابط

- [Founder Shortlist Rules](FOUNDER_SHORTLIST_RULES.md)
- [Market Intelligence OS](MARKET_INTELLIGENCE_OS.md)
