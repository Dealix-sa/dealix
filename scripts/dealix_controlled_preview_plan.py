import json
from pathlib import Path
clients=json.loads(Path('data/preview/preview_clients.json').read_text(encoding='utf-8'))
print('# Controlled Preview Plan')
print(f'Clients tracked: {len(clients)}')
for c in clients:
    print(f"- {c['client']} | {c['vertical']} | {c['stage']} | risk={c['risk']} | next={c['next_action']}")
print('Decision: keep managed controlled preview; do not open self-serve SaaS yet')
