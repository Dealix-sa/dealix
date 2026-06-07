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


queue=read_json('out/outreach_review_queue/latest_review_queue.json', {'items':[]}).get('items',[])
replies=lines_jsonl('data/outreach/reply_tracker.jsonl')
reviewed=lines_jsonl('data/outreach/reviewed_messages.jsonl')
callq=read_json('data/outreach/call_prep_queue.json', {'calls':[]}).get('calls',[])
approved=sum(1 for x in queue if x.get('review_status')=='approved')
print('# Dealix Outreach Execution Dashboard')
print(f'Drafts in review queue: {len(queue)}')
print(f'Approved drafts: {approved}')
print(f'Review log entries: {len(reviewed)}')
print(f'Replies tracked: {len(replies)}')
print(f'Call prep ready: {len(callq)}')
print('Next action: approve only high-context drafts, send manually, then log replies.')
