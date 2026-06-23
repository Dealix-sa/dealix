from pathlib import Path

required=['acquisition/ACQUISITION_MASTER_SYSTEM_AR.md','acquisition/playbooks/DAILY_100_LEADS_PLAYBOOK_AR.md','data/market/training_seed_list.csv','scripts/dealix_market_list_builder.py','scripts/dealix_prospect_importer.py','scripts/dealix_campaign_builder.py','scripts/dealix_outreach_batch_drafter.py','scripts/dealix_acquisition_dashboard.py','frontend/src/app/[locale]/solutions/training/page.tsx','frontend/src/app/[locale]/tools/roi-calculator/page.tsx','.github/workflows/dealix-v5-acquisition-readiness.yml']
missing=[p for p in required if not Path(p).exists()]
if missing:
 print('Missing V5 files:'); [print('-',m) for m in missing]; raise SystemExit(1)
print('OK: Dealix V5 acquisition files are present')
