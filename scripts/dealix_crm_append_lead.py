#!/usr/bin/env python3
import argparse
import hashlib
import json
from datetime import UTC, datetime, timezone
from pathlib import Path

CRM = Path('data/crm')
CRM.mkdir(parents=True, exist_ok=True)
LEADS = CRM / 'leads.jsonl'

def score(args):
    s = 0
    if args.company: s += 15
    if args.email or args.phone: s += 15
    if args.sector: s += 10
    if args.pain and len(args.pain) >= 20: s += 35
    if args.source: s += 10
    if any(x in (args.pain or '') for x in ['مبيعات','واتساب','متابعة','إيراد','leads','sales','revenue']): s += 15
    return min(s, 100)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--company', required=True)
    ap.add_argument('--sector', default='')
    ap.add_argument('--pain', required=True)
    ap.add_argument('--source', default='manual')
    ap.add_argument('--email', default='')
    ap.add_argument('--phone', default='')
    args = ap.parse_args()
    raw = f"{args.company}|{args.email}|{args.phone}|{datetime.now(UTC).date()}"
    lead = {
        'id': 'lead_' + hashlib.sha1(raw.encode()).hexdigest()[:12],
        'created_at': datetime.now(UTC).isoformat(),
        'company': args.company,
        'sector': args.sector,
        'pain': args.pain,
        'source': args.source,
        'email': args.email,
        'phone': args.phone,
        'score': score(args),
        'status': 'New',
        'next_action': 'Research company and draft first outreach message'
    }
    with LEADS.open('a', encoding='utf-8') as f:
        f.write(json.dumps(lead, ensure_ascii=False) + '\n')
    print(json.dumps(lead, ensure_ascii=False, indent=2))

if __name__ == '__main__': main()
