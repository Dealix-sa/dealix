import json, datetime
from pathlib import Path
# Ensure top tasks exist
try:
    top=Path('out/founder/top10_tasks.md').read_text(encoding='utf-8')
except FileNotFoundError:
    import subprocess, sys
    subprocess.run([sys.executable,'scripts/dealix_top10_task_ranker.py'], check=True)
    top=Path('out/founder/top10_tasks.md').read_text(encoding='utf-8')
clients=[]
for p in ['data/preview/preview_clients.json','data/revenue/first_5_clients.json']:
    if Path(p).exists():
        try:
            obj=json.loads(Path(p).read_text(encoding='utf-8'))
            if isinstance(obj, list): clients.extend(obj)
            elif isinstance(obj, dict): clients.extend(obj.get('clients',[]))
        except Exception:  # malformed JSON or missing keys — skip file
open_invoice='Review open invoices and collect before expanding scope'
if Path('data/revenue/invoices.jsonl').exists():
    rows=[r for r in Path('data/revenue/invoices.jsonl').read_text(encoding='utf-8').splitlines() if r.strip()]
    if rows: open_invoice=f'{len(rows)} invoice records require review'
decision='Close / Deliver / Prove: focus on one revenue action before building anything new.'
brief=f"""# Dealix Daily Command Brief

Date: {datetime.date.today().isoformat()}
Mode: Controlled Preview / Founder-led

## Today’s decision
{decision}

## Most important number
Active preview/client records: {len(clients)}

## Highest revenue action
{open_invoice}

## Top risks
- Too many open build threads without client action.
- Sending external messages without human review.
- Expanding SaaS self-serve before first 5 managed clients prove repeatability.

## Top 10 tasks
{top}

## Review queue
- Outreach drafts
- Invoices
- Proof reports
- Retainer conversion plans

## End-of-day requirement
Log execution, replies, invoice movement, proof delivered, and tomorrow’s single priority.
"""
out=Path('out/founder'); out.mkdir(parents=True, exist_ok=True)
Path('out/founder/daily_command_brief.md').write_text(brief, encoding='utf-8')
print(brief)
