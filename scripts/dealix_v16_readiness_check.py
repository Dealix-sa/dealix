import datetime
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


required = [
 'outreach-execution/REAL_OUTREACH_EXECUTION_SYSTEM_AR.md',
 'outreach-execution/HUMAN_REVIEWED_OUTREACH_POLICY_AR.md',
 'data/outreach/prospect_batches.json',
 'templates/outreach/first_touch_training_whatsapp_ar.md',
 'scripts/dealix_outreach_batch_builder.py',
 'scripts/dealix_message_personalizer.py',
 'scripts/dealix_human_review_queue.py',
 'scripts/dealix_reply_tracker.py',
 'scripts/dealix_call_prep_builder.py',
 'frontend/src/app/[locale]/sales-execution/page.tsx',
 '.github/workflows/dealix-v16-real-outreach.yml'
]
missing=[p for p in required if not (ROOT/p).exists()]
if missing:
    print('MISSING:'); [print('-',m) for m in missing]; raise SystemExit(1)
print('OK: Dealix V16 real outreach execution files are present')
print(f'Checked: {len(required)} critical files')
