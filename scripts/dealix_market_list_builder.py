import argparse,csv
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--vertical',required=True,choices=['training','agencies','real_estate','clinics','professional_services']); p.add_argument('--count',type=int,default=25); a=p.parse_args()
out=Path(f'data/market/{a.vertical}_working_list.csv'); out.parent.mkdir(parents=True,exist_ok=True)
header=['company_name','vertical','city','website_or_profile','source_url','suspected_pain','contact_channel','owner','status']
with out.open('w',encoding='utf-8',newline='') as f:
 w=csv.writer(f); w.writerow(header)
 for i in range(1,a.count+1): w.writerow([f'{a.vertical} prospect {i}',a.vertical,'Riyadh','','manual_research_needed','Need manual research before outreach','unknown','sami','research_needed'])
print(f'Wrote {out}')
