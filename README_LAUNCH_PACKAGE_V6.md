# Dealix Launch Package V6 — Enterprise Revenue & Service Factory

V6 يبني فوق V1/V2/V3/V4/V5 ويضيف طبقة تحويل Dealix إلى شركة قابلة للبيع للشركات الأكبر: enterprise account planning، business case، demo room، customer success، contracts، integrations، enablement، hiring، وCEO control tower.

## تشغيل سريع
```bash
python scripts/dealix_v6_readiness_check.py
python scripts/dealix_enterprise_account_planner.py --account "شركة تدريب الرياض" --vertical training --employees 80 --monthly_leads 250
python scripts/dealix_business_case_builder.py --account "شركة تدريب الرياض" --monthly_leads 250 --avg_deal_value 3500 --uplift 0.08
python scripts/dealix_demo_room_builder.py --vertical training --account "شركة تدريب الرياض"
python scripts/dealix_customer_success_health.py
python scripts/dealix_weekly_ceo_packet.py
```
