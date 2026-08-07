#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

LEADS = Path('data/crm/leads.jsonl')

def read_jsonl(path):
    if not path.exists(): return []
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]

leads = read_jsonl(LEADS)
stages = Counter(l.get('status','Unknown') for l in leads)
qualified = [l for l in leads if int(l.get('score',0)) >= 60]
print('# Dealix CRM Pipeline Report')
print(f'Total leads: {len(leads)}')
print(f'Qualified leads: {len(qualified)}')
print('\n## Stages')
for stage, n in stages.most_common(): print(f'- {stage}: {n}')
print('\n## Top leads')
for l in sorted(leads, key=lambda x: x.get('score',0), reverse=True)[:10]:
    print(f"- {l.get('company')} | score={l.get('score')} | next={l.get('next_action')}")
