import json
from collections import Counter, defaultdict
from pathlib import Path

p=Path('data/billing/usage_events.jsonl')
if not p.exists(): raise SystemExit('no usage file')
counts=defaultdict(Counter)
for line in p.read_text(encoding='utf-8').splitlines():
    if not line.strip(): continue
    e=json.loads(line); counts[e['tenant_id']][e['event_type']]+=float(e.get('quantity',1))
print('# Usage Report')
for tenant,c in counts.items():
    print(f'\n## {tenant}')
    for k,v in c.items(): print(f'- {k}: {v}')
