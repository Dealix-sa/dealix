import json
from pathlib import Path
clients=json.loads(Path('data/revenue/first_5_clients.json').read_text(encoding='utf-8')) if Path('data/revenue/first_5_clients.json').exists() else []
inv=[]
p=Path('data/revenue/invoices.jsonl')
if p.exists():
    inv=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()]
paid=sum(i.get('amount',0) for i in inv if i.get('status')=='paid')
sent=sum(i.get('amount',0) for i in inv if i.get('status') in ('sent','overdue'))
print('# Dealix Revenue Dashboard')
print(f'Clients in sprint: {len(clients)}')
print(f'Invoices: {len(inv)}')
print(f'Paid SAR: {paid}')
print(f'Open invoice SAR: {sent}')
print('Next action: collect open invoices, deliver proof reports, convert accepted pilots to retainers')
