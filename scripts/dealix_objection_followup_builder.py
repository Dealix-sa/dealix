from pathlib import Path
import json, datetime, argparse, re
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
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


ap=argparse.ArgumentParser(); ap.add_argument('--company', default='شركة تدريب الرياض'); ap.add_argument('--objection', default='price'); args=ap.parse_args()
map_={'price':'templates/outreach/follow_up_price_ar.md','interested':'templates/outreach/follow_up_interested_ar.md'}
t=(ROOT/map_.get(args.objection,'templates/outreach/follow_up_interested_ar.md')).read_text(encoding='utf-8')
out=ROOT/'out/objection_followups'; out.mkdir(parents=True, exist_ok=True)
path=out/(slug(args.company)+'_'+args.objection+'_followup.md'); path.write_text(t, encoding='utf-8')
data=read_json('data/outreach/objection_followups.json', {'items':[]}); data['items'].append({'company':args.company,'objection':args.objection,'path':str(path.relative_to(ROOT)),'created_at':now(),'status':'draft_needs_review'}); write_json('data/outreach/objection_followups.json', data)
print(f'Wrote {path.relative_to(ROOT)}')
