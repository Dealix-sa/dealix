# Sector Query Library — مكتبة قطاعات وقوالب البحث

> المصادر: [`data/targeting/sectors.yml`](../../data/targeting/sectors.yml) ·
> [`data/targeting/cities.yml`](../../data/targeting/cities.yml) ·
> [`data/targeting/queries.txt`](../../data/targeting/queries.txt) ·
> يبنيها: [`scripts/targeting_query_factory.py`](../../scripts/targeting_query_factory.py)

## القطاعات (Phase 1 أولًا)

| id | القطاع | phase | العرض الافتراضي |
|---|---|---:|---|
| b2b_consulting | استشارات أعمال B2B | 1 | Command Sprint |
| training_companies | شركات التدريب المؤسسي | 1 | Proof OS |
| marketing_agencies | وكالات تسويق | 1 | Command Sprint |
| software_companies | شركات برمجيات | 1 | Command OS |
| it_service_providers | مزودو خدمات تقنية | 1 | Command OS |
| recruitment_agencies | شركات التوظيف | 2 | Client OS |
| logistics_service_providers | خدمات لوجستية | 2 | Delivery OS |
| facility_management | إدارة المرافق | 2 | Delivery OS |
| accounting_firms | مكاتب محاسبة | 2 | Governance OS |
| legal_business_advisory | استشارات قانونية وأعمال | 2 | Governance OS |

## المدن

Phase 1: الرياض، جدة — Phase 2: الدمام، الخبر — Phase 3: مكة، المدينة.

## قوالب queries منسّقة

```
"شركة استشارات أعمال الرياض"
"وكالة تسويق B2B الرياض"
"شركة تدريب مؤسسي الرياض"
"شركة حلول تقنية للشركات السعودية"
site:.sa "خدماتنا" "تواصل معنا" "الرياض"
site:.sa "دراسات حالة" "خدمات" "الشركات"
site:.sa "عملاؤنا" "حلول" "تواصل"
```

## كيف تُبنى الـ queries

`build_queries(phase, sectors, cities, seed_queries, limit)` يدمج:
1. الـ queries المنسّقة من `queries.txt` (أعلى intent، أولًا).
2. حاصل ضرب `keywords_ar` للقطاع × المدن، مرتّبًا حسب `priority`.
3. probe واحد بصيغة `site:.sa` لكل قطاع/مدينة لاكتشاف فجوة الإثبات.

كل النتائج **مُزالة التكرار**، وكلها **research فقط** ضد مصادر مسموحة (تحترم
robots.txt وشروط الموقع — راجع الحوكمة).

## توسيع المكتبة

أضف قطاعًا بإضافة عنصر في `sectors.yml` (id, name_ar/en, phase, priority,
default_offer, keywords_ar). لا تُضِف قطاعات حساسة هنا — تُدار عبر
[`blocked_sources.yml`](../../data/targeting/blocked_sources.yml).
