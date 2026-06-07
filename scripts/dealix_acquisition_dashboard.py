from pathlib import Path
import csv
leads=high=0
for p in Path('data/prospects').glob('*.csv'):
 with p.open(encoding='utf-8') as f:
  for r in csv.DictReader(f):
   leads+=1
   try: high += int(r.get('fit_score') or 0)>=70
   except (ValueError, TypeError): pass  # non-numeric fit_score treated as 0
drafts=len(list(Path('out/outreach_drafts').glob('*.md'))) if Path('out/outreach_drafts').exists() else 0
campaigns=len(list(Path('data/campaigns').glob('*.json'))) if Path('data/campaigns').exists() else 0
print('Dealix Acquisition Dashboard'); print('Prospects:',leads); print('High-fit prospects:',high); print('Campaigns:',campaigns); print('Outreach drafts:',drafts); print('Next action: Review top drafts manually and log interactions in CRM')
