from pathlib import Path
import json, datetime, hashlib, argparse, re
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


ap=argparse.ArgumentParser(); ap.add_argument('--company', default='شركة تدريب الرياض'); ap.add_argument('--sector', default='training'); ap.add_argument('--pain', default='فرص تضيع بعد أول تواصل'); ap.add_argument('--fit-score', default='86'); args=ap.parse_args()
t=(ROOT/'templates/outreach/call_prep_template_ar.md').read_text(encoding='utf-8')
md=t.replace('{{company}}', args.company).replace('{{sector}}', args.sector).replace('{{pain}}', args.pain).replace('{{source}}','manual').replace('{{fit_score}}',str(args.fit_score))
out=ROOT/'out/call_prep'; out.mkdir(parents=True, exist_ok=True)
path=out/(slug(args.company)+'_call_prep.md'); path.write_text(md, encoding='utf-8')
q=read_json('data/outreach/call_prep_queue.json', {'calls':[]}); q['calls'].append({'company':args.company,'sector':args.sector,'status':'ready','path':str(path.relative_to(ROOT)),'created_at':now()}); write_json('data/outreach/call_prep_queue.json', q)
print(f'Wrote {path.relative_to(ROOT)}')
