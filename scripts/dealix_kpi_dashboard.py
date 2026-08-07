#!/usr/bin/env python3
import json
from pathlib import Path

p=Path('data/analytics/daily_metrics.jsonl')
rows=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()] if p.exists() else []
keys=['new_leads','qualified_leads','drafts_created','messages_reviewed','replies','discovery_calls','proposals_sent','closed_won']
print('# Dealix KPI Dashboard')
print(f'Days logged: {len(rows)}')
for k in keys:
    print(f'- {k}: {sum(int(r.get(k,0)) for r in rows)}')
if rows:
    latest=rows[-1]
    print('\n## Latest day')
    for k in keys: print(f'- {k}: {latest.get(k,0)}')
