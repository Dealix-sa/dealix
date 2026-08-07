#!/usr/bin/env python3
import argparse, csv
from pathlib import Path

SECTOR_SCORE = {
    'real estate': 15, 'training': 15, 'marketing agency': 15,
    'clinic': 12, 'ecommerce': 12, 'b2b services': 14
}

def score(row):
    text = ' '.join(str(v).lower() for v in row.values())
    s = 0
    if any(k in text for k in ['whatsapp','واتساب','leads','استفسارات','sales','مبيعات']): s += 25
    if any(k in text for k in ['b2b','عقار','real estate','training','تدريب','agency','وكالة']): s += 25
    if row.get('website','').strip(): s += 10
    if row.get('public_contact_source','').strip() or row.get('phone','').strip() or row.get('email','').strip(): s += 10
    sector = row.get('sector','').lower().strip()
    s += SECTOR_SCORE.get(sector, 8)
    if any(k in text for k in ['hiring','new branch','campaign','growth','expansion','توسع','حملة']): s += 15
    return min(s, 100)

parser = argparse.ArgumentParser()
parser.add_argument('--input', default='data/prospects/icp_seed_accounts_saudi.csv')
parser.add_argument('--output', default='data/prospects/scored_prospects.csv')
args = parser.parse_args()

inp, out = Path(args.input), Path(args.output)
out.parent.mkdir(parents=True, exist_ok=True)
with inp.open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))
if not rows:
    raise SystemExit('No prospects found')
fieldnames = list(rows[0].keys())
if 'lead_score' not in fieldnames: fieldnames.append('lead_score')
if 'next_action' not in fieldnames: fieldnames.append('next_action')
for r in rows:
    sc = score(r); r['lead_score'] = sc
    r['next_action'] = 'Call today' if sc >= 90 else 'Personalized outreach' if sc >= 70 else 'Nurture' if sc >= 50 else 'Ignore'
rows.sort(key=lambda r: int(r['lead_score']), reverse=True)
with out.open('w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader(); w.writerows(rows)
print(f'Wrote {len(rows)} scored prospects to {out}')
