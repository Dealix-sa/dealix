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


ap=argparse.ArgumentParser(); ap.add_argument('--company', default='شركة تدريب الرياض'); ap.add_argument('--reply', default='interested'); ap.add_argument('--note', default='طلب تفاصيل'); args=ap.parse_args()
entry={'reply_id':'reply_'+hashlib.sha1((args.company+now()).encode()).hexdigest()[:10], 'company':args.company, 'reply_type':args.reply, 'note':args.note, 'next_action':'build_call_prep' if args.reply in ['interested','send_info'] else 'follow_up_later', 'timestamp':now()}
append_jsonl('data/outreach/reply_tracker.jsonl', entry)
print(f"Logged reply: {args.company} / {args.reply} / next={entry['next_action']}")
