# Dealix Launch Package V4 — Production Growth & Enterprise Readiness

هذه الحزمة تبني فوق V1/V2/V3 وتضيف طبقة الإنتاج الحقيقي: نشر، قاعدة بيانات، تتبع، API contracts، قطاعية، شراكات، FinOps، QA، Data Room، وفحوصات CI أكثر انضباطًا.

## الهدف
تحويل Dealix من Revenue Machine محلية إلى نظام جاهز للتشغيل مع عملاء حقيقيين:

1. الموقع يلتقط Leads.
2. الـ CRM ledger يربط lead/account/opportunity/interactions.
3. الـ Offer Builder يطلع عرض.
4. الـ Delivery OS يعرف ماذا يسلم.
5. V4 يضيف Production readiness: deploy, DB, observability, QA, partner channel, enterprise collateral.

## التشغيل السريع

```bash
python scripts/dealix_v4_readiness_check.py
python scripts/dealix_finance_forecast.py --pilots 5 --pilot-price 499 --retainers 2 --retainer-price 4500
python scripts/dealix_vertical_pack_builder.py --vertical training
python scripts/dealix_partner_referral_tracker.py --partner "مستشار مبيعات" --lead "شركة تدريب الرياض" --value 4500
python scripts/dealix_deployment_manifest_check.py
python scripts/dealix_sla_risk_register.py
```

## قاعدة الحزمة
لا يوجد إرسال آلي. لا يوجد scraping مخالف. لا يوجد وعد بنتائج مضمونة. كل التشغيل الخارجي review-first.
