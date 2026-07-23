# ⚠️ ARCHIVED EXTERNAL REFERENCE — NOT WIRED INTO LIVE SYSTEMS

هذا المجلد أرشيف **حرفي** لحزمة إطلاق خارجية (Dealix Launch Package V2،
مولّدة بأداة خارجية بتاريخ 2026-06-07). محفوظ كمرجع فقط.

**لا شيء هنا مُفعّل:**

- ملفات `.tsx` هنا **خارج** `frontend/` فلا يبنيها Next.js.
- مجلد `.github/workflows/` هنا **ليس** في جذر الريبو فلا يشغّله GitHub Actions.
- سكربتات `scripts/` هنا مرجعية فقط؛ النسخ المعتمدة المُواءمة في `scripts/launch_package/`.

## لماذا أُرشفت بدل دمجها مباشرة؟

الحزمة تكرّر ~90% مما هو موجود في الريبو **بصيغة أنضج ومحكومة**، وبعض تعليمات
الدمج الأصلية (`cp -R` + الكتابة فوق صفحات الفرونت + CI على كل PR) **تدميرية**:
تستبدل صفحات Next.js ثنائية اللغة بنسخ ناقصة، وتُدخل نموذج تسعير ثالث متعارضًا،
وتشغّل سكربتات تكتب ملفات على كل PR.

**التفاصيل والخريطة الكاملة (ملف بملف):**
[`../LAUNCH_PACKAGE_RECONCILIATION_AR.md`](../LAUNCH_PACKAGE_RECONCILIATION_AR.md)

## ما الذي رُقّي فعليًا من هذه الحزمة (مُواءَمًا للاصطلاحات)؟

- `compliance/OUTBOUND_AND_DATA_POLICY_AR.md` → `docs/compliance/OUTBOUND_AND_DATA_POLICY_AR.md`
- `scripts/dealix_daily_prospect_drafts.py`, `dealix_lead_scoring.py`, `dealix_daily_command_center.py`
  → `scripts/launch_package/` (مع بذرة أمثلة ومخطط)
