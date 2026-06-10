# Transformation OS — خارطة الطريق (4 جبهات)

> هذه الوثيقة **توثيق فقط** — لا تُبنى الآن. كل جبهة = PR مستقل لاحق ببوابة قبول.
> الهدف: جعل Dealix قوية من كل الجهات بعد إطلاق طبقة Transformation OS.

---

## الجبهة 1 — تقوية الأمان (Security Hardening)

**النطاق:** معالجة نتائج OpenSSF Scorecard القائم
(`.github/workflows/scorecard.yml`): تثبيت hashes للتبعيات في الـ workflows،
تضييق صلاحيات `permissions` لأدنى حد، معالجة الثغرات، تفعيل branch protection.
**بوابة القبول:** ارتفاع درجة Scorecard + ترقية ادّعاءات `secret_hygiene` /
`ci_security` في `no_overclaim.yaml` مع أدلة.

## الجبهة 2 — حزمة الثقة المؤسسية (Enterprise Trust Pack)

**النطاق:** تحويل [trust_compliance_pack_template](enterprise_package/trust_compliance_pack_template.md)
و MSA/DPA إلى **حزمة قابلة للتسليم** (PDF مولّد عبر `trust_os/trust_pack.py`):
أدلة PDPL/NCA، SLA، إجابات استبيان الأمان. + إضافة حزمة `transformation` إلى
**مصفوفة الجاهزية** (توسعة ٣٢→٤٢) مع تحديث اختبارات العدد والتوزيع معًا.
**بوابة القبول:** حزمة ثقة مولّدة لكل عميل مؤسسي + مصفوفة جاهزية محدّثة CI-green.

## الجبهة 3 — تعميق محرك العروض/ROI (Proposal/ROI Engine)

**النطاق:** حفظ العروض في قاعدة البيانات (موديل جديد + migration برأس واحد)،
ربط ROI المُقاس بأحداث Proof (حلقة تحقق فعلية)، سرد LLM للأقسام مثل
`diagnostic_engine._llm_sections`. تصدير العرض كـ PDF.
**بوابة القبول:** سجل عروض قابل للاستعلام + ROI مُتحقَّق (لا تقديري) عند توفر Proof.

## الجبهة 4 — نظام الهوية (Brand/Identity OS)

**النطاق:** تشغيل دليل تسليم `brand_intelligence_os`: تموضع، نبرة، قوالب محتوى،
prompt library آمنة للعلامة، ومحاذاة landing/portal.
**بوابة القبول:** أصول هوية قابلة لإعادة الاستخدام + محاذاة الواجهات.

---

## الترتيب المقترح

1 (أمان) → 2 (ثقة) معًا لأنهما أساس بيع enterprise كبير، ثم 3 (عروض/ROI) ثم 4 (هوية).

## مرجع

[DEALIX_TRANSFORMATION_OS_MASTER_AR.md](DEALIX_TRANSFORMATION_OS_MASTER_AR.md)
