#!/usr/bin/env python3
import argparse, json
from pathlib import Path
from datetime import datetime, timezone
ap=argparse.ArgumentParser()
for name in ['new-leads','qualified-leads','drafts-created','messages-reviewed','replies','discovery-calls','proposals-sent','closed-won']:
    ap.add_argument('--'+name, type=int, default=0)
args=ap.parse_args()
row={'created_at': datetime.now(timezone.utc).isoformat(), **vars(args)}
Path('data/analytics').mkdir(parents=True, exist_ok=True)
with Path('data/analytics/daily_metrics.jsonl').open('a', encoding='utf-8') as f: f.write(json.dumps(row, ensure_ascii=False)+'\n')
print(json.dumps(row, ensure_ascii=False, indent=2))
