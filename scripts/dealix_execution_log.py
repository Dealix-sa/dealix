import argparse
import datetime
import json
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--task', required=True)
ap.add_argument('--status', default='done')
ap.add_argument('--note', default='')
args=ap.parse_args()
Path('data/founder').mkdir(parents=True, exist_ok=True)
row={'ts':datetime.datetime.now(datetime.UTC).isoformat(),'task':args.task,'status':args.status,'note':args.note}
with Path('data/founder/execution_log.jsonl').open('a', encoding='utf-8') as f:
    f.write(json.dumps(row, ensure_ascii=False)+'\n')
print(f"Logged execution: {args.task} / {args.status}")
