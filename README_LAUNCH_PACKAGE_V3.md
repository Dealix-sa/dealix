# Dealix Launch Package V3 — Revenue Machine

هذه الحزمة تبني فوق V1 و V2 وتحوّل Dealix من موقع + أصول مبيعات إلى ماكينة تشغيل إيراد قابلة للقياس.

## ماذا يضيف V3؟

1. Lead Capture API + صفحات Diagnostic و Booking.
2. CRM Ledger محلي بصيغة JSON/JSONL.
3. Offer Builder يولّد عروض Diagnostic / Pilot / Executive OS / Custom AI.
4. Case Study Engine لتحويل كل نجاح إلى أصل تسويقي.
5. KPI logging + dashboard يومي.
6. Client Delivery OS لتسليم الخدمات بعد البيع.
7. Security Smoke Checks تمنع تسريب أسرار أو نشر بيانات حساسة.
8. GitHub Actions بصلاحيات read فقط قدر الإمكان.

## أوامر التشغيل السريعة

```bash
python scripts/dealix_v3_readiness_check.py
python scripts/dealix_crm_append_lead.py --company "شركة تدريب الرياض" --sector "Training" --pain "متابعة واتساب ضعيفة" --source "manual" --email "ops@example.com"
python scripts/dealix_crm_pipeline_report.py
python scripts/dealix_crm_next_actions.py
python scripts/dealix_offer_builder.py --company "شركة تدريب الرياض" --package pilot --sector training --pain "فرص تضيع بعد أول تواصل"
python scripts/dealix_kpi_log.py --new-leads 5 --qualified-leads 2 --drafts-created 12 --messages-reviewed 8 --replies 1 --discovery-calls 1 --proposals-sent 0 --closed-won 0
python scripts/dealix_kpi_dashboard.py
python scripts/dealix_secret_smoke_check.py
python scripts/dealix_public_exposure_check.py
```

## قاعدة التشغيل

- لا إرسال تلقائي للعملاء.
- لا scraping مخالف.
- كل رسالة تخرج بمراجعة بشرية.
- كل lead له مصدر واضح.
- كل عرض مرتبط بمشكلة تجارية قابلة للقياس.
- كل workflow بصلاحيات محدودة.
