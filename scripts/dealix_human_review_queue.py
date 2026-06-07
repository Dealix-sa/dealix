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


ap=argparse.ArgumentParser(); ap.add_argument('--approve-first', action='store_true'); args=ap.parse_args()
items=[]
for p in (ROOT/'out/outreach_personalized').glob('*_draft.json') if (ROOT/'out/outreach_personalized').exists() else []:
    item=json.loads(p.read_text(encoding='utf-8'))
    item['review_status']='approved' if args.approve_first and not items else 'pending_review'
    item['reviewed_at']=now() if item['review_status']=='approved' else None
    items.append(item)
write_json('out/outreach_review_queue/latest_review_queue.json', {'generated_at':now(),'items':items})
for item in items:
    append_jsonl('data/outreach/reviewed_messages.jsonl', {'message_id':item['message_id'], 'company':item['company'], 'review_status':item['review_status'], 'timestamp':now()})
print(f'Review queue items: {len(items)}')
print('Reminder: drafts only; no automated sending.')
