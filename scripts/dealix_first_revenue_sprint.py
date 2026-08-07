import json
from pathlib import Path

clients_path=Path('data/revenue/first_5_clients.json')
clients=json.loads(clients_path.read_text(encoding='utf-8')) if clients_path.exists() else []
print('# First Revenue Sprint')
print(f'Clients tracked: {len(clients)}')
for c in clients:
    print(f"- {c.get('client')} | {c.get('sector')} | {c.get('stage')} | SAR {c.get('amount_sar',0)} | {c.get('status')}")
print('Next action: move every active pilot to proof report + retainer conversion review')
