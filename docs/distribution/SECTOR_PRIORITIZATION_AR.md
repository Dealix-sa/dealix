# Dealix Sector Prioritization — تحديد أولوية القطاعات

التصريف الحقيقي يبدأ من اختيار القطاع. **لا تستهدف كل الناس.**

البيانات في `data/distribution/sectors.yaml`؛ المنطق في
`dealix/distribution/sectors.py`. الأولوية **تُحسب** من مكوّنات موزونة (لا رقم
سحري مكتوب يدويًا).

## صيغة الدرجة (0–100)

| المكوّن | الوزن |
| --- | ---: |
| Pain intensity | 20 |
| Lead volume | 15 |
| Decision-maker access | 15 |
| Budget ability | 15 |
| Proof speed | 15 |
| Delivery simplicity | 10 |
| Saudi localization advantage | 10 |

`priority = Σ min(score_component, weight_component)`

## القطاعات (مرتّبة بالأولوية المحسوبة)

تشمل: وكالات التسويق، شركات التدريب، العيادات، فرق العقار، وكالات التوظيف،
الخدمات المهنية، مزودو التعليم، مجموعات المطاعم، شركات اللوجستيك، شركات
الخدمات/البرمجيات المحلية. لكل قطاع: `pain`, `offer`, `offer_ref` (يشير لعرض في
`os/03_OFFERS.yml`)، `first_workflow`, و`proof_speed_days`.

## بوابة الدخول لقطاع جديد

لا تدخل قطاعًا جديدًا إلا إذا توفّر **كل** ما يلي:

- pain واضح وموثّق (call / Proof / اعتراض)
- offer واضح من الكتالوج (`offer_ref`)
- draft sequence جاهز (قالب القطاع في `data/templates/distribution/`)
- proof angle محدد (أين التسرب)
- delivery checklist بسيط (أول workflow)

## التحقق
```python
from dealix.distribution.sectors import load_sectors
for s in load_sectors()[:3]:
    print(s["key"], s["priority"], s["offer_ref"])
```
