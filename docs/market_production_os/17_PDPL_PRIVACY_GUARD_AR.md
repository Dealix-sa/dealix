# PDPL Privacy Guard — حارس خصوصية PDPL للتواصل الخارجي — Saudi PDPL Privacy Guard

> الموقف الحاسم: **وضوح PDPL ميزة تنافسية، لا عبء.** حيث تجعل المنصات الغربية الامتثال إعداداً يُطفأ، نجعله قيداً معمارياً في كل مسودة تخرج.

هذا المستند يحدّد موقف الخصوصية السعودي (PDPL) لطبقة التواصل الخارجي في Market Production OS: ماذا نجمع، على أي أساس، وكيف نحمي أصحاب البيانات. ليس استشارة قانونية — أي ادعاء «امتثال كامل» يمرّ بمحامٍ/DPO أولاً.

- العمود الفقري: [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md) (اللاء رقم 6: لا PII في السجلات)
- المراجعة القانونية الكاملة: [`../commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md`](../commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md)
- قائمة مرور المؤسس: [`../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md`](../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)
- الكتالوج (DPA قبل معالجة PII): [`02_PRODUCT_CATALOG_OS_AR.md`](02_PRODUCT_CATALOG_OS_AR.md)

---

## 1. المبادئ السبعة للتواصل الخارجي

| المبدأ | التطبيق في الطبقة |
|---|---|
| تقليل البيانات (Data Minimization) | لا نجمع إلا ما يلزم لمسودة مطابِقة لعرض واحد. لا حقول زائدة. |
| الأساس القانوني (Lawful Basis) | لكل قناة أساس موثّق: عقد/مصلحة مشروعة/موافقة — يُوثَّق per قناة. |
| لا PII غير ضرورية | لا national ID، لا تفاصيل حساسة في المسودة أو الـ prospect record. |
| احترام do-not-contact | فحص suppression قبل كل دفعة؛ من طلب التوقف يُضاف فوراً. |
| توفير opt-out | كل بريد يحمل رابط unsubscribe صالحاً — شرط إرسال إلزامي. |
| احتفاظ وحذف عند الطلب | مدة احتفاظ محددة + محو عند الطلب (مع استثناءات قانونية/ZATCA). |
| لا بيانات حساسة في prompts/logs | لا PII خام في موجهات النماذج ولا في السجلات. |

---

## 2. تقليل البيانات — Data Minimization

نجمع الحد الأدنى الذي تتطلبه مسودة مطابِقة لعرض واحد من الكتالوج: اسم الشركة، القطاع، إشارة ألم عامة، ومسؤول قرار (دور لا هوية كاملة حيث أمكن). لا نخزّن بيانات لا تخدم مسودة محدّدة. أي بحث عام يدوي عن شركة = `linkedin_company_search (manual, founder-approved per call)` — يدوي، لكل حالة، بموافقة المؤسس، وليس أداة آلية ولا scraping.

---

## 3. الأساس القانوني — Lawful Basis

- **عقد/مصلحة مشروعة:** تواصل B2B مع شركة في سياق عرض ذي صلة، بأساس موثّق لكل قناة.
- **موافقة:** واتساب لا يبدأ إلا **بعد رد العميل وبموافقته**؛ لا واتساب بارد إطلاقاً.
- **DPA قبل أي PII:** معالجة بيانات طرف ثالث (بيانات عملاء العميل) لا تبدأ قبل توقيع DPA — العميل = Controller، Dealix = Processor.

---

## 4. لا PII غير ضرورية + لا بيانات حساسة في prompts/logs

- لا أرقام هوية وطنية، لا بيانات بطاقات (الدفع عبر Moyasar خارج تخزين Dealix)، لا بيانات صحية، لا بيانات قُصّر في رسائل خارجية أو سجلات.
- موجهات النماذج اللغوية تُقلّل PII قبل الإرسال للمعالج؛ السجلات تُخزّن مراجع/أحداث لا PII خام (اللاء رقم 6).
- في قطاعات حساسة (عيادات، تعليم، توظيف) لا تدخل بيانات الأفراد المحميين أي مسودة أو log — انظر إشارات لا-تستهدف في [`03_SECTOR_INTELLIGENCE_OS_AR.md`](03_SECTOR_INTELLIGENCE_OS_AR.md).

---

## 5. احترام do-not-contact + توفير opt-out

شرط الإرسال (كلها معاً، من المرجع الرئيسي §7): موافقة + unsubscribe مُضمَّن + صحة دومين + فحص suppression + تخصيص ≥ P1 + مستوى مخاطرة منخفض/متوسط.

| الإجراء | القاعدة |
|---|---|
| فحص suppression | قبل كل دفعة؛ لا إرسال لأي عنوان في قائمة المنع. |
| opt-out | رابط unsubscribe صالح في كل بريد؛ غيابه = منع الإرسال. |
| طلب التوقف | يُضاف فوراً إلى suppression؛ لا تواصل لاحق. |
| do-not-target | إشارات القطاع الحساسة → `do_not_contact` تلقائياً. |

---

## 6. الاحتفاظ والحذف — Retention & Deletion

- مدة احتفاظ محددة لسجلات الـ prospect والمسودات، تُراجَع دورياً.
- محو عند الطلب وفق DSAR SOP (مع استثناءات قانونية/فوترة ZATCA).
- عند إنهاء العقد: إجراء محو/إرجاع موثّق (انظر المراجعة القانونية §3).
- لا بيع بيانات؛ المعالجة لأداء العقد فقط.

---

## 7. PDPL كميزة تنافسية — Competitive Advantage

نُحوّل وضوح PDPL إلى موقع بيعي:

- «مسودات وموافقة قبل أي إجراء خارجي» يطمئن قسم العميل القانوني قبل أن يسأل.
- «لا قوائم مشتراة ولا scraping» يفصلنا عن أدوات outbound تخالف الأساس القانوني.
- «صفر إرسال تلقائي، 250 مسودة/يوم» يثبت أن الكثافة لا تعني المخاطرة.

العبارات الآمنة (لا «معتمد من SDAIA»): «مصمم وفق مبادئ PDPL»، «إجراءات امتثال قابلة للتدقيق»، «قائمة معالجين فرعيين منشورة». أسئلة قسم القانوني العشرة جاهزة في [`../commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md`](../commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md) §8.

---

## 8. ما هو محظور (لا يُعرض كقدرة أبداً)

scraping إنتاجي · أتمتة LinkedIn · واتساب بارد · إرسال جماعي/بارد · قوائم بريد مشتراة · عناوين/مواضيع مضللة · إرسال بلا unsubscribe · تجاهل opt-out · PII حساسة في prompts/logs. أي طلب من هذا → **يُرفض ويُقترح البديل الآمن**، لا التفاف على البوابات.

---

## EN — PDPL Privacy Guard Summary

This document defines the Saudi PDPL posture for the outbound layer of Market Production OS, framing PDPL clarity as a competitive advantage rather than a burden. Seven principles govern every draft: data minimization (collect only what one catalog-matched draft needs), documented lawful basis per channel (contract / legitimate interest / consent), no unnecessary PII (no national IDs, no card data, no health or minors' data), honoring do-not-contact via suppression checks before every batch, providing a valid opt-out (unsubscribe link mandatory), retention with deletion on request (per DSAR SOP, with lawful ZATCA exceptions), and no sensitive data in prompts or logs. WhatsApp begins only after a reply with consent — never cold; third-party PII is processed only after a signed DPA (customer = Controller, Dealix = Processor). The send condition combines approval, unsubscribe, domain health, suppression check, personalization ≥ P1, and low/medium risk. Safe language avoids "SDAIA certified" in favor of "designed per PDPL principles" and "auditable compliance procedures". Forbidden as a capability and offered only as a refusal: scraping, LinkedIn automation, cold WhatsApp, bulk/cold outreach, purchased lists; any manual public-company lookup is `linkedin_company_search (manual, founder-approved per call)`. Cross-links: master spine, the existing PDPL legal review, the founder PDPL compliance pass, product catalog, and sector intelligence.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
