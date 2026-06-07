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


import subprocess, sys
cmds=[
 [sys.executable,'scripts/dealix_v16_readiness_check.py'],
 [sys.executable,'scripts/dealix_outreach_batch_builder.py','--vertical','training','--limit','10'],
 [sys.executable,'scripts/dealix_message_personalizer.py','--vertical','training'],
 [sys.executable,'scripts/dealix_human_review_queue.py'],
 [sys.executable,'scripts/dealix_call_prep_builder.py','--company','شركة تدريب الرياض','--sector','training'],
 [sys.executable,'scripts/dealix_outreach_execution_dashboard.py'],
]
for c in cmds:
    print('\n$ '+' '.join(c)); subprocess.run(c, check=True)
