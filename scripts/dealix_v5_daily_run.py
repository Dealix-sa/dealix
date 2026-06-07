import subprocess,sys
steps=[['python','scripts/dealix_v5_readiness_check.py'],['python','scripts/dealix_market_list_builder.py','--vertical','training','--count','25'],['python','scripts/dealix_prospect_importer.py','--input','data/market/training_seed_list.csv','--output','data/prospects/v5_imported_prospects.csv'],['python','scripts/dealix_campaign_builder.py','--vertical','training','--campaign-name','training-riyadh-pilot'],['python','scripts/dealix_outreach_batch_drafter.py','--input','data/prospects/v5_imported_prospects.csv','--vertical','training','--limit','10'],['python','scripts/dealix_acquisition_dashboard.py']]
for s in steps:
 print('RUN:',' '.join(s)); r=subprocess.run(s)
 if r.returncode: sys.exit(r.returncode)
