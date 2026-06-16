# مكينة الليدز السعودية — تشغيل Dealix

هذا المسار يربط **بذرة بيانات آمنة**، **استقبال دفعي** مع مصدر Tier1 موثّق، **dedupe**، **Decision Passport**، و**اكتشاف محلي** (Google Places chain) دون تجاوز سياسات PDPL أو مصادر محظورة.

## حدود غير قابلة للنقض

- لا قوائم مشتراة، لا scraping إنتاجي، لا واتساب بارد، لا أتمتة LinkedIn — التفاصيل في `auto_client_acquisition/revenue_os/source_registry.py` وفي كتالوج المصادر أدناه.
- كل ليد دفعي يجب أن يحمل `tier1_source` من الـ enum المعرّف في السجل؛ المصادر ذات `allowed_use=blocked` أو `can_store=false` تُرفض قبل التشغيل.
- بيانات `data/seed/saudi_demo_leads.yaml` **وهمية للتجربة**؛ عناوين البريد بصيغة `+seedN@example.com` لتمرير `email-validator` إن استُخدمت لاحقاً عبر الـ API. أي PII حقيقي يقع تحت مسؤولية المشغّل قانونياً.

## المسار الموصى به

1. **بذرة YAML** — تعديل أو نسخ `data/seed/saudi_demo_leads.yaml` ثم التحقق:  
   `python scripts/import_seed_leads.py --dry-run`
2. **استيراد برمجي (بدون HTTP)** — تشغيل الـ pipeline محلياً مع خيار عدم الكتابة لقاعدة البيانات:  
   `python scripts/import_seed_leads.py --no-persist`  
   أو الكتابة الكاملة (يتطلب اتصال Postgres مطابق `DATABASE_URL`):  
   `python scripts/import_seed_leads.py`
3. **دفعة عبر API** — `POST /api/v1/leads/batch` بجسم يتضمن `tier1_source` واحداً لكل الطلب وقائمة `items` (حتى 50). النجاح الجزئي مسموح: عنصر فاشل لا يوقف البقية.
4. **Dedupe + جواز قرار** — يُحسب `dedupe_hint` عبر `suggest_dedupe_fingerprint` ويُخزَّن في `LeadRecord.meta_json` مع `tier1_source` و`targeting_profile` عند توفرها.
5. **اكتشاف محلي** — `POST /api/v1/leads/discover/local` مع `industry` + `city` أو مع `targeting_profile` (نموذج `SaudiTargetingProfile`) لدمج الاستعلام مع الحقول الصريحة دون كسر التوافق مع العملاء الحاليين.

## Endpoints ذات الصلة

| Endpoint | الغرض |
|----------|--------|
| `POST /api/v1/leads` | ليد واحد عبر الـ pipeline الكامل |
| `POST /api/v1/leads/batch` | دفعة مع Tier1 واحد + anti-waste على مستوى الطلب |
| `POST /api/v1/leads/discover/local` | اكتشاف محلي (Places chain + fallback) |
| `GET /api/v1/leads/discover/local-industries` | مفاتيح `INDUSTRY_QUERIES` و`SAUDI_CITIES` |
| `GET /api/v1/revenue-os/catalog` | كتالوج المصادر وترتيب الـ waterfall |

## متغيرات البيئة (اكتشاف محلي)

- `GOOGLE_MAPS_API_KEY` — تفعيل مزود Google Places في السلسلة.
- `SERPAPI_API_KEY`، `APIFY_TOKEN` — اختيارية؛ السلسلة تتراجع إلى `static_fallback` عند عدم التوفر.

## ربط Tier1 بـ LeadSource (الاستقبال)

الجسر الحتمي بين سجل Revenue OS وقناة الاستقبال موثّق في `map_tier1_to_intake_lead_source` داخل `auto_client_acquisition/revenue_os/saudi_targeting_profile.py` — يُفضَّل الرجوع إليه بدل افتراضات ضمنية في الواجهات.

## كتالوج مصادر إضافي

للمقارنة مع مصادر بيانات سوقية عامة (تصنيف أخضر/أصفر/أحمر)، راجع [SAUDI_DATA_SOURCE_CATALOG.md](./SAUDI_DATA_SOURCE_CATALOG.md). استخدام أي مصدر **أحمر** أو خارج `source_registry` للإنتاج يُرفض من المنتج.

## السلسلة الذهبية والتشغيل الاستراتيجي

المرجع الشامل للمنتج: `docs/strategic/DEALIX_MASTER_OPERATING_MODEL_AR.md`.

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
