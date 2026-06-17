from pathlib import Path
required = [
 'scale/SCALE_MASTER_PLAN_AR.md','cadence/WEEKLY_OPERATING_RHYTHM_AR.md','cadence/MONTHLY_SCALE_REVIEW_AR.md','portfolio/CLIENT_PORTFOLIO_REVIEW_AR.md','scale/SALES_CAPACITY_AND_QUOTAS_AR.md','scale/SERVICE_MARGIN_SYSTEM_AR.md','automation-backlog/AUTOMATION_BACKLOG_SYSTEM_AR.md','scale/HIRING_AND_DELEGATION_CADENCE_AR.md','partners/PARTNER_QUOTA_AND_SCORECARD_AR.md','ops/SCALE_OPERATING_SCORECARD_AR.md','data/scale/weekly_operating_metrics.json','data/portfolio/client_health.json','data/automation/automation_backlog.json','scripts/dealix_weekly_operating_rhythm.py','scripts/dealix_scale_dashboard.py','.github/workflows/dealix-v12-scale-cadence.yml'
]
missing = [p for p in required if not Path(p).exists()]
if missing:
    print('Missing V12 files:')
    [print('-', m) for m in missing]
    raise SystemExit(1)
print('OK: Dealix V12 scale and operating cadence files are present')
