import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read_json(path, default):
    p=ROOT/path
    if not p.exists(): return default
    return json.loads(p.read_text(encoding='utf-8') or '{}')
def write_json(path, obj):
    p=ROOT/path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
def append_jsonl(path, obj):
    p=ROOT/path; p.parent.mkdir(parents=True, exist_ok=True); p.open('a', encoding='utf-8').write(json.dumps(obj, ensure_ascii=False)+"\n")
def lines_jsonl(path):
    p=ROOT/path
    if not p.exists(): return []
    return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
def slug(s):
    return re.sub(r'[^\w\u0600-\u06FF-]+','_',s).strip('_')[:80]
def now():
    return datetime.datetime.now(datetime.UTC).isoformat()


ap=argparse.ArgumentParser(); ap.add_argument('--input', default='out/outreach_batches/latest_batch.json'); ap.add_argument('--vertical', default='training'); args=ap.parse_args()
batch=read_json(args.input, {'prospects':[], 'vertical':args.vertical})
vertical=batch.get('vertical') or args.vertical
template_path='templates/outreach/first_touch_training_whatsapp_ar.md' if vertical=='training' else 'templates/outreach/first_touch_agency_email_ar.md'
template=(ROOT/template_path).read_text(encoding='utf-8')
outdir=ROOT/'out/outreach_personalized'; outdir.mkdir(parents=True, exist_ok=True)
count=0
for p in batch.get('prospects',[]):
    company=p.get('company') or p.get('name') or 'Prospect'
    msg=template.replace('{{company}}', company).replace('{{sector}}', p.get('sector', vertical)).replace('{{pain}}', p.get('pain','فوضى المتابعة')).replace('{{source}}', p.get('contact_source','manual')).replace('{{fit_score}}', str(p.get('fit_score','')))
    item={'message_id':'msg_'+hashlib.sha1((company+now()).encode()).hexdigest()[:10], 'prospect_id':p.get('prospect_id') or slug(company), 'company':company, 'vertical':vertical, 'channel':p.get('channel','whatsapp'), 'status':'draft_needs_human_review', 'draft':msg, 'created_at':now()}
    (outdir/(slug(company)+'_draft.json')).write_text(json.dumps(item, ensure_ascii=False, indent=2), encoding='utf-8')
    count+=1
print(f'Wrote {count} personalized drafts to out/outreach_personalized')
