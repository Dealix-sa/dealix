import json
from pathlib import Path

items=json.loads(Path('data/partners/partner_scorecard.json').read_text(encoding='utf-8'))
print('# Partner Quota Dashboard')
for p in items:
    conv = (p['pilots']/p['qualified']) if p['qualified'] else 0
    print(f"- {p['partner']} | referrals={p['referrals_month']} | qualified={p['qualified']} | pilots={p['pilots']} | conversion={conv:.0%} | decision={p['quality']}")
