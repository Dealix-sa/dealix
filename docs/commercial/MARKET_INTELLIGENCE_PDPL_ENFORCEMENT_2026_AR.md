# استخبارات سوق — إنفاذ PDPL 2026 (موجز صفحة واحدة)

**الحالة:** موجز تشغيلي للمؤسس · ليس استشارة قانونية
**التاريخ:** 2026-05-24
**الجمهور:** المؤسس · المبيعات · الهندسة قبل عروض القطاع المنظَّم
**Audience (EN):** Founder · Sales · Engineering pre-regulated-sector pitch

---

## 1) الإنفاذ أصبح فعلياً (Enforcement is live)

| المؤشر | الرقم | مصدر / مستوى دليل |
|--------|--------|---------------------|
| قرارات إنفاذ SDAIA حتى منتصف يناير 2026 | 48 قراراً | تصريحات SDAIA العلنية — Evidence L3 |
| سقف الغرامة للمخالفة الواحدة | حتى 5,000,000 ريال سعودي | نظام PDPL — Evidence L1 |
| مضاعَفة الغرامة عند التكرار | نعم | نظام PDPL — Evidence L1 |
| نافذة الرد على إشعار SDAIA | 5 أيام عمل | لائحة تنفيذية / تواصل SDAIA — Evidence L2 |
| المخالفات على البيانات الحساسة المتعمَّدة / المتكررة | ملاحقة جزائية + سجن حتى سنتين | نظام PDPL — Evidence L1 |

**الخلاصة:** انتهت مرحلة «PDPL على الورق». 2026 = إنفاذ تشغيلي بأرقام وقرارات.

**EN gloss:** PDPL enforcement is operational. Fines reach SAR 5M per breach, doubled on repeat. Criminal exposure up to 2 years for intentional/repeat violations on sensitive data. SDAIA gives 5 business days to respond to a notice.

---

## 2) المخالفات الشائعة المُعلَنة من SDAIA

استناداً إلى أنماط القرارات المُعلَنة (Evidence L3 — لا أرقام قضايا، لا أسماء شركات):

1. **معالجة بيانات شخصية بدون أساس قانوني** (غياب الموافقة أو العقد أو المصلحة المشروعة الموَثَّقة).
2. **إفصاح غير مصرَّح** لطرف ثالث / معالج فرعي غير مُدرَج.
3. **غياب الضمانات التقنية والتنظيمية** (لا تشفير، لا تحكم وصول، لا سجلات).
4. **اتصالات تسويقية بدون موافقة موَقَّتة موثَّقة** (WhatsApp / SMS / Email).
5. **عدم الاستجابة لإشعار SDAIA خلال النافذة**.
6. **عدم التسجيل على المنصة الوطنية لحوكمة البيانات (NDGP)** عند الإلزام.

**نقطة بيع تجارية لـ Dealix:**
> «PDPL compliance لم تعد مجاملة قانونية — هي خط دفاع مالي. Dealix يُسلَّم مع Trust Pack يغلق 4 من أكثر 6 مخالفات شيوعاً.»

---

## 3) ما يغطّيه Dealix اليوم (operational reality, no overclaim)

| المخالفة الشائعة | تغطية Dealix | الدليل في الريبو |
|-------------------|---------------|-------------------|
| معالجة بلا أساس قانوني | مغطّاة جزئياً | [`FOUNDER_PDPL_COMPLIANCE_PASS_AR.md`](FOUNDER_PDPL_COMPLIANCE_PASS_AR.md) §2 |
| إفصاح غير مصرَّح | مغطّاة | sub-processors.html + DPA template |
| غياب الضمانات | مغطّاة جزئياً | `api/middleware/http_stack.py` (audit log) |
| تسويق بلا موافقة | **مغطّاة بقوة** | قاعدة منتج: لا إرسال خارجي بدون approval per-action |
| عدم الاستجابة لإشعار | **غير مغطّاة** — تتطلب retainer محامٍ | [`FOUNDER_PDPL_COMPLIANCE_PASS_AR.md`](FOUNDER_PDPL_COMPLIANCE_PASS_AR.md) §5 |
| عدم التسجيل NDGP | **قرار مؤسس** — لم يُتخذ بعد | [`FOUNDER_PDPL_COMPLIANCE_PASS_AR.md`](FOUNDER_PDPL_COMPLIANCE_PASS_AR.md) §4 |

**مفتاح القراءة:** «مغطّاة» = موجود تقنياً + قابل للتدقيق. «مغطّاة جزئياً» = موجود تقنياً لكن يحتاج توثيق عميل. «غير مغطّاة» = يحتاج قرار مؤسس + ربما طرف ثالث (محامٍ).

---

## 4) قائمة إجراءات المؤسس (Founder action list — هذا الأسبوع)

1. **اقرأ** [`FOUNDER_PDPL_COMPLIANCE_PASS_AR.md`](FOUNDER_PDPL_COMPLIANCE_PASS_AR.md) §2–§6 وضَع `done: true` فقط بدليل في [`operations/founder_pdpl_compliance_pass.yaml`](operations/founder_pdpl_compliance_pass.yaml).
2. **احجز محامياً سعودياً على retainer** أو اتفاق توافر خلال 24 ساعة — هذا يفتح نافذة الـ 5 أيام عملياً.
3. **عيّن بريد + موبايل واحد** كنقطة استلام رسمية لإشعارات SDAIA. سجّلهما في `dealix/registers/sdaia_contact.yaml` (يُنشأ عند الحاجة).
4. **افحص نسخ المبيعات** بحثاً عن `PDPL certified|معتمد|100% سعودية|نضمن امتثال` واستبدلها بصيغ آمنة من [`MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md`](MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md) §2.
5. **قرار NDGP:** سجِّل أو وثِّق التأجيل بمبرر مكتوب قبل أول عميل قطاع منظَّم.
6. **حدّث Trust Pack** ليُذكر إنفاذ 2026 صراحة كـ «لماذا الآن» في كل proposal — انظر [`operations/TRUST_PACK_PROPOSAL_AR.md`](operations/TRUST_PACK_PROPOSAL_AR.md).

---

## 5) زاوية بيعية جديدة (sales angle — use carefully)

**القديم:** «Dealix يحترم خصوصية بياناتكم.»
**الجديد (مدعوم بواقع 2026):**
> «Dealix يحمي حسابكم من ست مخالفات PDPL أصدرت SDAIA قرارات إنفاذ بشأنها. كل عرض يأتي بـ Trust Pack وDPA وسجل موافقات قابل للاسترجاع — تُسلَّم الجاهزية، لا الوعود.»

**ما يبقى ممنوعاً قوله:** «نضمن عدم وقوع غرامة» / «معتمد من SDAIA» / «بدائل قانونية كاملة» — هذا تجاوز قانوني وتجاري.

**EN gloss:** Shift from "we respect privacy" to "we close 4 of the 6 most commonly enforced PDPL violations, with a Trust Pack delivered per engagement." Never promise zero fines.

---

## 6) ما لا يزال يتطلب المحامي البشري

- صياغة بنود DPA / MSA النهائية بلغة عقدية ملزمة.
- تأكيد المواد النظامية المحددة للأرقام (مدة احتفاظ سجل الموافقة، نطاق «حجم كبير»، تعريف «معالجة منتظمة»).
- مراجعة سياسة الخصوصية المنشورة قبل أي تحديث جوهري.
- تمثيل Dealix أمام SDAIA عند تلقي إشعار فعلي.
- قرار تسجيل NDGP حسب طبيعة العميل المحدد.
- DPIA للقطاعات المنظَّمة (صحة، مالية، تعليم أطفال).

**Evidence levels في هذه الوثيقة:**
- L1 (نص PDPL مباشر): سقف الغرامة، المضاعَفة، السجن للمخالفة الجزائية.
- L2 (مبدأ PDPL أو إرشاد SDAIA عام): نافذة 5 أيام، تعريف الموافقة، التزام DPO الجزئي.
- L3 (نمط إنفاذ SDAIA المُعلَن، لا أرقام قضايا): 48 قراراً، 6 مخالفات شائعة، إنفاذ WhatsApp.
- L4 (تفسير Dealix داخلي): تصنيف «مغطّاة / جزئياً / غير مغطّاة» للمنتج.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**

*مراجع داخلية:*
- [`FOUNDER_PDPL_COMPLIANCE_PASS_AR.md`](FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)
- [`MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md`](MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md)
- [`MARKET_INTELLIGENCE_OBJECTIONS_PDPL_AR.md`](MARKET_INTELLIGENCE_OBJECTIONS_PDPL_AR.md)
- [`operations/objection_engine_registry.yaml`](operations/objection_engine_registry.yaml) (5 اعتراضات PDPL جديدة)
- [`operations/TRUST_PACK_PROPOSAL_AR.md`](operations/TRUST_PACK_PROPOSAL_AR.md)
- [`operations/founder_pdpl_compliance_pass.yaml`](operations/founder_pdpl_compliance_pass.yaml)

*مراجع خارجية:*
- [SDAIA PDPL Knowledge Center](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPLCP/)
- [National Data Governance Platform — NDGP](https://dgp.sdaia.gov.sa)

*آخر تحديث: 2026-05-24*
