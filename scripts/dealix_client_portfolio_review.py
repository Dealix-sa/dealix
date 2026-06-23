import json
from pathlib import Path

clients = json.loads(Path('data/portfolio/client_health.json').read_text(encoding='utf-8'))
print('# Client Portfolio Review')
for c in clients:
    action = 'expand' if c['health']=='green' and c['revenue_sar']>0 else 'stabilize' if c['health']=='yellow' else 'rescue'
    print(f"- {c['client']} | {c['health']} | SAR {c['revenue_sar']} | decision={action} | next={c['next_action']}")
