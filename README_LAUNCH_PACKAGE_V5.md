# Dealix Launch Package V5 — Client Acquisition Automation & Real Market Data Pack

V5 يبني فوق V4 ويضيف طبقة اكتساب عملاء واقعية: قوائم إدخال منظمة، scoring متقدم، حملات حسب القطاع، قوالب بحث، صفحات solutions، نظام referral، dashboard يومي، ورسائل متابعة بشرية.

## القاعدة الذهبية
لا scraping مخالف، لا إرسال آلي، لا وعود نتائج مضمونة. كل المخرجات تكون drafts وnext actions للمراجعة البشرية.

## التشغيل السريع
```bash
python scripts/dealix_v5_readiness_check.py
python scripts/dealix_market_list_builder.py --vertical training --count 25
python scripts/dealix_prospect_importer.py --input data/market/training_seed_list.csv --output data/prospects/v5_imported_prospects.csv
python scripts/dealix_campaign_builder.py --vertical training --campaign-name training-riyadh-pilot
python scripts/dealix_outreach_batch_drafter.py --input data/prospects/v5_imported_prospects.csv --vertical training --limit 10
python scripts/dealix_acquisition_dashboard.py
```
