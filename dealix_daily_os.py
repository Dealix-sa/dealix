from __future__ import annotations

import json
from pathlib import Path

import m6_runtime
import z7_router

REPORT = Path('reports/leadership/z8')

COMMERCIAL_OFFERS = [
    {'offer_id': 'sprint-7d', 'name': '7 day command sprint', 'price_range': '5000-12000 SAR', 'best_for': 'fast diagnosis and first operating proof'},
    {'offer_id': 'os-14d', 'name': '14 day growth operating system', 'price_range': '15000-35000 SAR', 'best_for': 'client wants repeatable sales and follow up workflow'},
    {'offer_id': 'managed-monthly', 'name': 'managed command room', 'price_range': '5000-25000 SAR monthly', 'best_for': 'ongoing operation and leadership reporting'},
]

SECTORS = [
    {'sector': 'clinics', 'pain': 'missed follow up and WhatsApp overload', 'entry_offer': 'sprint-7d'},
    {'sector': 'agencies', 'pain': 'client reporting and lead operations', 'entry_offer': 'managed-monthly'},
    {'sector': 'training', 'pain': 'lead conversion and cohort follow up', 'entry_offer': 'os-14d'},
    {'sector': 'logistics', 'pain': 'B2B pipeline visibility and partner motion', 'entry_offer': 'os-14d'},
]


def build_console():
    memory = m6_runtime.build_payload()
    routing = z7_router.build_payload()
    approvals_pending = routing['summary']['needs_review']
    route_counts = {channel: len([r for r in routing['routes'] if r['channel'] == channel]) for channel in routing['channels']}
    owner_workload = {}
    for route in routing['routes']:
        owner_workload[route['owner']] = owner_workload.get(route['owner'], 0) + 1
    summary = {
        'memory_decisions': memory['summary']['decisions'],
        'routes': routing['summary']['routes'],
        'channels': routing['summary']['channels'],
        'approvals_pending': approvals_pending,
        'offers': len(COMMERCIAL_OFFERS),
        'target_sectors': len(SECTORS),
        'live': routing['summary']['live'],
    }
    return {
        'summary': summary,
        'commercial_offers': COMMERCIAL_OFFERS,
        'target_sectors': SECTORS,
        'route_counts': route_counts,
        'owner_workload': owner_workload,
        'proof': memory['proof'],
        'next_sales_actions': [
            {'action': 'prepare 10 account list for top sector', 'owner': 'Growth Director'},
            {'action': 'review proposal push drafts', 'owner': 'Sales Director'},
            {'action': 'prepare partner brief for one agency', 'owner': 'Partnerships Director'},
            {'action': 'publish founder proof post draft', 'owner': 'Marketing Director'},
            {'action': 'review claims and pricing ranges', 'owner': 'Trust Owner'},
        ],
    }


def write_reports(payload):
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Dealix Z8 Daily Operating Console', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Commercial Offers')
    for offer in payload['commercial_offers']:
        lines.append(f"- **{offer['name']}** — {offer['price_range']} — {offer['best_for']}")
    lines.append('\n## Next Sales Actions')
    for action in payload['next_sales_actions']:
        lines.append(f"- **{action['owner']}** — {action['action']}")
    (REPORT / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload):
    errors = []
    if payload['summary']['live'] != 0:
        errors.append('live must be zero')
    if payload['summary']['offers'] < 3:
        errors.append('commercial offers missing')
    if payload['summary']['target_sectors'] < 4:
        errors.append('target sectors missing')
    if payload['summary']['approvals_pending'] <= 0:
        errors.append('approvals must be visible')
    return errors


def main():
    payload = build_console()
    write_reports(payload)
    errors = verify(payload)
    print('Z8_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
