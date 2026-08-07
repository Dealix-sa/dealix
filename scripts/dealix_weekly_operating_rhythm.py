import json
from pathlib import Path

metrics_path = Path('data/scale/weekly_operating_metrics.json')
metrics = json.loads(metrics_path.read_text(encoding='utf-8')) if metrics_path.exists() else {}
score = 0
checks = []
def add(name, ok):
    global score
    checks.append((name, ok))
    score += int(ok)
add('lead_flow', metrics.get('qualified_prospects',0) >= 10)
add('sales_motion', metrics.get('discovery_calls',0) >= 2)
add('proposal_motion', metrics.get('proposals_sent',0) >= 1)
add('proof_shipping', metrics.get('proof_assets_shipped',0) >= 1)
add('delivery_load_control', metrics.get('delivery_hours',999) <= 25)
print('# Weekly Operating Rhythm')
for name, ok in checks:
    print(f'- {name}: {"OK" if ok else "WATCH"}')
print(f'Score: {score}/{len(checks)}')
if score < 3:
    print('Next action: reduce scope and fix one bottleneck before scaling.')
else:
    print('Next action: continue controlled scale with weekly review.')
