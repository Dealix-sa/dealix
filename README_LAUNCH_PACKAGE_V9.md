# Dealix Launch Package V9 — Real Productization & Multi-Tenant SaaS Layer

V9 يحول Dealix إلى منتج SaaS/Managed SaaS: tenants, workspaces, roles, usage, billing, audit logs, admin console, API contracts.

## تشغيل سريع
```bash
python scripts/dealix_v9_readiness_check.py
python scripts/dealix_tenant_bootstrap.py --tenant "شركة تدريب الرياض" --plan starter_managed
python scripts/dealix_usage_meter.py --tenant-id tenant_example --event-type agent_run --quantity 5
python scripts/dealix_audit_log.py --tenant-id tenant_example --action create_offer --resource-type offer
python scripts/dealix_usage_report.py
python scripts/dealix_saas_maturity_score.py
```

## القاعدة
لا تطلق self-serve كامل قبل أن يثبت: usage + retention + billing + support process.
