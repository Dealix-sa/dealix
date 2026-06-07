import argparse,csv
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--vertical',required=True); p.add_argument('--limit',type=int,default=10); a=p.parse_args()
tpl=Path('templates/messages/first_touch_whatsapp_ar.md').read_text(encoding='utf-8'); outdir=Path('out/outreach_drafts'); outdir.mkdir(parents=True,exist_ok=True); written=0
with open(a.input,encoding='utf-8') as f:
 for row in csv.DictReader(f):
  if written>=a.limit: break
  try: sc=int(row.get('fit_score') or 0)
  except (ValueError, TypeError): sc=0
  if sc<70: continue
  company=row.get('company_name','prospect'); msg=tpl.replace('{{company}}',company).replace('{{vertical}}',a.vertical).replace('{{vertical_label}}',a.vertical)
  safe=''.join(c for c in company if c.isalnum() or c in (' ','_','-')).strip().replace(' ','_') or f'prospect_{written+1}'
  (outdir/f'{safe}_whatsapp_draft.md').write_text(msg,encoding='utf-8'); written+=1
print(f'Wrote {written} outreach drafts to {outdir}')
