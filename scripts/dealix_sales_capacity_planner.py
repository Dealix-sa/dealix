import argparse, json
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('--weeks', type=int, default=4)
p.add_argument('--close-rate', type=float, default=0.2)
p.add_argument('--pilot-price', type=float, default=499)
args = p.parse_args()
cap = json.loads(Path('data/capacity/sales_capacity.json').read_text(encoding='utf-8'))
weekly_proposals = cap['founder']['proposals_per_week']
expected_pilots = weekly_proposals * args.close_rate * args.weeks
revenue = expected_pilots * args.pilot_price
print('# Sales Capacity Plan')
print(f'Weeks: {args.weeks}')
print(f'Founder proposals/week: {weekly_proposals}')
print(f'Expected pilots: {expected_pilots:.1f}')
print(f'Expected pilot revenue SAR: {revenue:.2f}')
print('Constraint: founder closing capacity; delegate research before closing.')
