# ICP Matrix — Ideal Customer Profile — مصفوفة العميل المثالي

**Dealix — نظام تشغيل الإيرادات للشركات السعودية / Saudi B2B Revenue Operating System.**

هذه المصفوفة تحدّد **من نخاطب ومن نتجاوز** قبل اللمسة الأولى، وكيف نسجّل كل احتمال. الأسعار والعروض مرجعها: [./PRODUCT_CATALOG_AR.md](./PRODUCT_CATALOG_AR.md) و [./DEALIX_REVOPS_PACKAGES_AR.md](./DEALIX_REVOPS_PACKAGES_AR.md). القطاعات: [../sectors/README.md](../sectors/README.md).

This matrix defines **who we address and who we skip** before first touch, and how we score every prospect. Offers and prices: [./PRODUCT_CATALOG_AR.md](./PRODUCT_CATALOG_AR.md) and [./DEALIX_REVOPS_PACKAGES_AR.md](./DEALIX_REVOPS_PACKAGES_AR.md). Sectors: [../sectors/README.md](../sectors/README.md).

## Firmographics — السمات المؤسسية

| البُعد / Dimension | المثالي / Ideal | مقبول / Acceptable | خارج النطاق / Out |
|---|---|---|---|
| القطاع / Sector | أحد القطاعات العشرة المعرّفة B2B خدمي بمتابعة مبيعات | قطاع B2B مجاور بألم متابعة | B2C صرف بلا pipeline حسابات |
| الحجم / Size | 10–200 موظفاً، فريق مبيعات 2–20 | حتى 500 موظف بوحدة مبيعات واضحة | منشأة دون فريق مبيعات |
| المنطقة / Region | **السعودية (KSA)** — عمليات محلية | خليجي بعمليات سعودية | خارج السعودية بلا وجود محلي |
| البيانات / Data | CSV/CRM export جاهز للرفع | بيانات قابلة للتجميع خلال أيام | لا بيانات قابلة للمراجعة |
| القناة / Channel | يقبل موافقة بشرية على الرسائل | يقبل المسودات + المراجعة | يطلب إرسالاً بارداً آلياً |

القطاعات العشرة المعتمدة وأول عرض لكل منها في [../sectors/README.md](../sectors/README.md).

## إشارات التأهيل / Qualifying signals

- **ألم متابعة واضح ومتكرر:** فرص تضيع بعد أول اتصال، لا أحد يعرف من يلاحق ولماذا.
- **بيانات حاضرة:** تصدير CSV/CRM فعلي (بلا بيانات لا يوجد Sprint).
- **جهة قرار واضحة:** مؤسس/مدير عام أو قائد مبيعات يملك الميزانية أو الصلاحية.
- **قدرة دفع:** القطاع والحجم يحتملان العرض الافتراضي (Sprint 9,500) أو يبدآن بـ Diagnostic (3,500).
- **إشارة دافئة:** مقدمة شخصية، inbound، أو إشارة شراء/توظيف حديثة.
- **قبول الحوكمة:** يرضى بالموافقة على المسودات وبحدود المصادر وPDPL.

## مُبعِدات (Disqualifiers) — لا نخاطب

- خارج السعودية بلا عمليات محلية.
- طلب **scraping** أو شراء قوائم أو **إرسال بارد آلي** (واتساب/LinkedIn) — نرفض صراحة.
- توقّع **ضمان نتائج رقمي** كشرط للتعاقد.
- لا جهة قرار، أو لا قدرة دفع حتى للأرضية.
- لا بيانات قابلة للمراجعة ولا استعداد لتجميعها.
- صناعة محظورة أو حساسة لا نخدمها، أو تعارض امتثال لا يُحل.

## رُبريك تسجيل الاحتمال (0–100) / Prospect scoring rubric

**يُؤهَّل الاحتمال عند ≥ 60 / Qualify at ≥ 60.** هذا الرُّبريك يحكم من نلمس أولاً، ويُطبَّق قبل أي مسودة.

| المعيار / Criterion | الوزن / Weight | ما نقيسه / What we measure |
|---|---:|---|
| sector_fit — ملاءمة القطاع | 20 | ضمن القطاعات العشرة بألم متابعة واضح |
| expected_leads — الفرص المتوقعة | 20 | حجم وجودة الحسابات القابلة للتشغيل |
| decision_maker_clear — وضوح صانع القرار | 15 | جهة قرار محددة بالاسم والدور |
| pain_clear — وضوح الألم | 15 | ألم تشغيلي محدد وقابل للقياس |
| payment_capacity — القدرة على الدفع | 15 | ميزانية أو صلاحية للأرضية على الأقل |
| personalization — قابلية التخصيص | 10 | معلومات كافية لرسالة شخصية (لا قالب عام) |
| low_risk — انخفاض المخاطر | 5 | لا تعارض امتثال، لا قناة محظورة، مصدر نظيف |
| **المجموع / Total** | **100** | |

**القراءة / Reading:**

- **≥ 60** — مؤهّل: جهّز مسودة شخصية وارفعها لقائمة الموافقة.
- **40–59** — مسودة فقط، لا أولوية لمسة هذا الأسبوع؛ اجمع إشارة دافئة أولاً.
- **< 40** — لا تُلامس الآن.

**ملاحظة توافق / Alignment note:** يوجد رُبريك قطاعي مبسّط (pain_fit/budget_fit/data_readiness/channel_ok/warm_signal) في [../sectors/README.md](../sectors/README.md) لترتيب **القطاعات**؛ هذا الرُّبريك المئوي لترتيب **الاحتمال الفردي**. استخدم القطاعي للأولوية العامة، والمئوي قبل اللمسة.

## القناة بعد التأهيل / Channel after qualifying

- القناة الأساسية للاكتساب = **البريد البارد** (وفق الامتثال).
- واتساب **بعد الرد/الموافقة فقط** — ليس قناة باردة.
- LinkedIn **يدوي فقط** — لا أتمتة.
- كل رسالة تمرّ على بوّابات الموافقة في [../market_production_os/README.md](../market_production_os/README.md).

## القواعد غير القابلة للمساومة / Non-negotiables

- لا scraping، لا إرسال بارد آلي، لا أتمتة LinkedIn، لا قوائم مشتراة.
- لا ضمان نتائج — **فرص مُثبتة بأدلة / evidenced opportunities**.
- لا PII في السجلّات. لا إجراء خارجي بلا موافقة.

## روابط مرجعية / Related docs

- [./PRODUCT_CATALOG_AR.md](./PRODUCT_CATALOG_AR.md) · [./BUYER_PERSONAS_AR.md](./BUYER_PERSONAS_AR.md) · [./OFFER_LADDER_AR.md](./OFFER_LADDER_AR.md)
- [../sectors/README.md](../sectors/README.md) — القطاعات العشرة والرُّبريك القطاعي
- [./DEALIX_REVOPS_PACKAGES_AR.md](./DEALIX_REVOPS_PACKAGES_AR.md) · [../market_production_os/README.md](../market_production_os/README.md)

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
