import argparse,csv
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--output',required=True); a=p.parse_args(); Path(a.output).parent.mkdir(parents=True,exist_ok=True)
def score(r):
 s=0; pain=(r.get('suspected_pain') or '').lower()
 if r.get('website_or_profile'): s+=15
 if r.get('source_url'): s+=15
 if any(k in pain for k in ['واتساب','follow','متابعة','pipeline','عروض','تسجيلات','حجوزات']): s+=35
 if r.get('contact_channel') and r.get('contact_channel')!='unknown': s+=15
 if r.get('city') in ['Riyadh','Jeddah','Dammam','Khobar']: s+=10
 if r.get('vertical'): s+=10
 return min(s,100)
with open(a.input,encoding='utf-8') as f, open(a.output,'w',encoding='utf-8',newline='') as o:
 r=csv.DictReader(f); fields=list(r.fieldnames or [])+['fit_score','next_action']; w=csv.DictWriter(o,fieldnames=fields); w.writeheader(); c=0
 for row in r:
  row['fit_score']=score(row); row['next_action']='draft_outreach' if int(row['fit_score'])>=70 else 'research_more'; w.writerow(row); c+=1
print(f'Imported {c} prospects into {a.output}')
