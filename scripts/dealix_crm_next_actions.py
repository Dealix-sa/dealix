#!/usr/bin/env python3
import json
from pathlib import Path
LEADS=Path('data/crm/leads.jsonl')
leads=[json.loads(x) for x in LEADS.read_text(encoding='utf-8').splitlines() if x.strip()] if LEADS.exists() else []
print('# Next Actions')
for l in sorted(leads, key=lambda x: x.get('score',0), reverse=True)[:20]:
    score=int(l.get('score',0))
    if score >= 75: action='Call / send direct founder message today'
    elif score >= 60: action='Prepare tailored diagnostic note'
    elif score >= 40: action='Research more before outreach'
    else: action='Park until stronger signal'
    print(f"- {l.get('company')} ({score}): {action}")
