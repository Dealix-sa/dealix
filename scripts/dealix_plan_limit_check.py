import json
from pathlib import Path
plans=json.loads(Path('data/billing/plans.json').read_text(encoding='utf-8'))['plans']
print('# Plan Limits')
for plan in plans:
    print(f"- {plan['id']}: SAR {plan['monthly_sar']} / limits={plan['limits']}")
