# 09 — Data OS — نظام البيانات

**الحالة — Status: `BETA` (تكامل PDPL موجود في الريبو؛ جرد المصدر والجودة قيد التشغيل)**

> قبل أي AI — وضوح المصدر والموافقة. البيانات التي لا نعرف مصدرها لا تدخل النظام.

## الغرض — Purpose

Data OS هو طبقة البيانات التأسيسية: كل سجل يدخل دِيليكس يحمل **مصدرًا، وموافقة، ومدة احتفاظ، وحق حذف**. الغرض هو أن تكون الخصوصية **صريحة من اليوم الأول**، لا بندًا قانونيًا مخفيًا.

## القيمة — Value

- يجعل الخصوصية ميزة تنافسية لا عبئًا: دِيليكس صريح حيث يصمت الآخرون.
- يمنع تلوّث البيانات (مصدر مجهول، موافقة مفقودة) قبل أن يصل للنماذج.
- يجعل طلبات الحذف والتصدير عملية معيارية لا أزمة.

## سياق خارجي — External Context

دراسة حديثة على عيّنة من **100 موقع تجارة إلكترونية سعودي** وجدت أن **31% فقط** أفصحت عن العناصر الأربعة للخصوصية مجتمعةً: **مدة الاحتفاظ، حق المحو (erasure)، حق الحصول على نسخة (copy)، آلية الشكاوى (complaints)**. *(هذا سياق خارجي يُستشهد به للتأطير، لا ادعاء عن دِيليكس.)* الفرصة: دِيليكس يكسب الثقة بأن يكون صريحًا على العناصر الأربعة منذ البداية.

## القدرات — Capabilities

- **استقبال البيانات (Intake)** مع `Source Passport` لكل دفعة.
- **الموافقة (Consent)** — افتراضي الرفض (default-deny)، لا استخدام بلا أساس قانوني.
- **تتبّع المصدر (Source tracking)** واحترام `robots.txt` وشروط المصدر.
- **إزالة التكرار (Deduplication)** ودرجة جودة البيانات (**Data Quality Score**).
- **الاحتفاظ والحذف والتصدير (Retention / Deletion / Export)** — معالجة طلبات DSAR.

## المُدخلات والمُخرجات — Inputs / Outputs

| المُدخل | المُخرج |
|---|---|
| دفعة بيانات + مصدر | سجل موثّق بـ Source Passport |
| أساس الموافقة | حالة استخدام مسموح/مرفوض |
| طلب حذف/تصدير (DSAR) | تنفيذ موثّق + سجل |

## البوابات والقواعد — Gates / Rules

- **لا scraping خلف تسجيل دخول.** احترام `robots.txt` وشروط المصدر.
- **لا استخدام لبيانات العميل في تدريب النماذج.**
- **افتراضي الرفض في الموافقة** — لا أساس قانوني = لا معالجة.
- **الإفصاح عن العناصر الأربعة** (احتفاظ/محو/نسخة/شكاوى) متاح للعميل دائمًا.

## الاتصالات — Connections to other OS

- **Governance OS** — أي طلب حذف/تصدير = إجراء A4: [GOVERNANCE_OS.md](GOVERNANCE_OS.md)
- **Market Intelligence** — كل هدف يحتاج `evidence_source`: [../01_go_to_market/MARKET_INTELLIGENCE_OS.md](../01_go_to_market/MARKET_INTELLIGENCE_OS.md)
- سياسات البيانات الفعلية في الريبو: [../04_data_os/SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md) · [../04_data_os/DATA_RETENTION_POLICY.md](../04_data_os/DATA_RETENTION_POLICY.md) · [../04_data_os/DATA_QUALITY_SCORE.md](../04_data_os/DATA_QUALITY_SCORE.md)
- PDPL التشغيلي: [../ops/PDPL_RETENTION_POLICY.md](../ops/PDPL_RETENTION_POLICY.md) · [../saudi/PDPL_AWARE_OPERATIONS.md](../saudi/PDPL_AWARE_OPERATIONS.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
