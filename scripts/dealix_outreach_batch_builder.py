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


ap=argparse.ArgumentParser(); ap.add_argument('--vertical', default='training'); ap.add_argument('--limit', type=int, default=10); args=ap.parse_args()
# Prefer imported prospects, fallback to seed batch.
prospects=[]
for f in ['data/prospects/v5_imported_prospects.csv']:
    p=ROOT/f
    if p.exists():
        import csv
        for row in csv.DictReader(p.open(encoding='utf-8')):
            if args.vertical.lower() in (row.get('vertical') or row.get('sector') or '').lower(): prospects.append(row)
if not prospects:
    data=read_json('data/outreach/prospect_batches.json', {'batches':[]})
    for b in data.get('batches',[]):
        if b.get('vertical')==args.vertical: prospects += b.get('prospects',[])
prospects=sorted(prospects, key=lambda x: int(float(x.get('fit_score') or x.get('score') or 0)), reverse=True)[:args.limit]
out={'batch_id':'batch_'+args.vertical+'_'+hashlib.sha1(now().encode()).hexdigest()[:6], 'vertical':args.vertical, 'created_at':now(), 'status':'ready_for_personalization', 'prospects':prospects}
write_json('out/outreach_batches/latest_batch.json', out)
print(f"Wrote out/outreach_batches/latest_batch.json with {len(prospects)} prospects")
