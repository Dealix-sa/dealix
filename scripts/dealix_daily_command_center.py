#!/usr/bin/env python3
from pathlib import Path
from datetime import date
import csv, json

prospects = Path('data/prospects/scored_prospects.csv')
report_dir = Path('reports/daily')
report_dir.mkdir(parents=True, exist_ok=True)
rows=[]
if prospects.exists():
    with prospects.open(encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
priority=[r for r in rows if int(r.get('lead_score') or 0)>=70]
report = {
    'date': str(date.today()),
    'total_scored_prospects': len(rows),
    'priority_prospects': len(priority),
    'top_10': priority[:10],
    'daily_targets': {
        'new_accounts': 25,
        'human_reviewed_messages': 10,
        'call_attempts': 3,
        'qualified_meetings_target': 1
    },
    'rules': ['no automated outbound', 'human approval before sending', 'use public/consented context only']
}
out=report_dir/f'dealix_command_center_{date.today()}.json'
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(out)
