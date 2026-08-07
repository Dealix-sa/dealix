from __future__ import annotations

import json
from pathlib import Path

import dealix_daily_os

REPORT = Path('reports/leadership/s9')

ACCOUNTS = [
    {'id': 'clinic-001', 'name': 'Riyadh Clinic Group', 'sector': 'clinics', 'city': 'riyadh', 'channels': ['whatsapp', 'email'], 'pain': 'missed follow up', 'urgency': 9, 'fit': 9},
    {'id': 'agency-001', 'name': 'B2B Growth Agency', 'sector': 'agencies', 'city': 'riyadh', 'channels': ['email', 'linkedin'], 'pain': 'client reporting', 'urgency': 8, 'fit': 8},
    {'id': 'training-001', 'name': 'Training Academy', 'sector': 'training', 'city': 'jeddah', 'channels': ['email', 'phone'], 'pain': 'lead conversion', 'urgency': 7, 'fit': 8},
    {'id': 'logistics-001', 'name': 'Logistics Operator', 'sector': 'logistics', 'city': 'dammam', 'channels': ['email', 'phone'], 'pain': 'B2B pipeline visibility', 'urgency': 8, 'fit': 7},
    {'id': 'clinic-002', 'name': 'Specialty Clinic', 'sector': 'clinics', 'city': 'khobar', 'channels': ['whatsapp', 'email'], 'pain': 'appointment follow up', 'urgency': 8, 'fit': 9},
]

OFFERS = {
    'sprint': {'name': '7 day command sprint', 'range': '5000-12000 SAR', 'best_for': ['clinics', 'training']},
    'os': {'name': '14 day growth operating system', 'range': '15000-35000 SAR', 'best_for': ['logistics', 'training']},
    'managed': {'name': 'managed command room', 'range': '5000-25000 SAR monthly', 'best_for': ['agencies', 'clinics']},
}

OBJECTIONS = {
    'price': 'Start with a smaller sprint and prove the operating workflow first.',
    'timing': 'Use a low lift diagnostic with clear required inputs.',
    'details': 'Send a non binding brief with scope, outputs, and next steps.',
    'trust': 'Show the daily proof report and review gates before any rollout.',
}


def score_account(account):
    channel_bonus = 2 if 'whatsapp' in account['channels'] else 1
    city_bonus = 2 if account['city'] in ['riyadh', 'jeddah'] else 1
    return account['urgency'] * 5 + account['fit'] * 5 + channel_bonus + city_bonus


def match_offer(account):
    scored = []
    for offer_id, offer in OFFERS.items():
        score = 10 if account['sector'] in offer['best_for'] else 6
        scored.append((score, offer_id, offer))
    scored.sort(reverse=True)
    return {'offer_id': scored[0][1], **scored[0][2]}


def build_discovery_script(account, offer):
    return [
        f"What happens today after a lead contacts {account['name']}?",
        'Who owns follow up and reporting?',
        'Which channels create the most missed opportunities?',
        f"Would a {offer['name']} be useful as a first controlled sprint?",
        'What must be approved before any external action?',
    ]


def build_followups(account):
    return [
        {'day': 0, 'type': 'first_touch', 'draft': f"Share a short operating gap note for {account['name']}."},
        {'day': 2, 'type': 'proof_followup', 'draft': 'Share a sample daily command report and ask for a short review.'},
        {'day': 5, 'type': 'pilot_offer', 'draft': 'Suggest a small sprint with clear inputs and review gates.'},
    ]


def build_payload():
    daily = dealix_daily_os.build_console()
    rows = []
    for account in ACCOUNTS:
        score = score_account(account)
        offer = match_offer(account)
        rows.append({
            'account': account,
            'score': score,
            'offer': offer,
            'discovery_script': build_discovery_script(account, offer),
            'followups': build_followups(account),
            'objection_notes': OBJECTIONS,
            'review_required': True,
            'live': 0,
        })
    rows.sort(key=lambda row: row['score'], reverse=True)
    summary = {
        'accounts': len(rows),
        'top_accounts': len(rows[:3]),
        'offers': len(OFFERS),
        'followups': sum(len(row['followups']) for row in rows),
        'review_required': len([row for row in rows if row['review_required']]),
        'live': 0,
        'daily_routes': daily['summary']['routes'],
        'daily_approvals': daily['summary']['approvals_pending'],
    }
    return {'summary': summary, 'ranked_accounts': rows, 'top_accounts': rows[:3], 'offers': OFFERS, 'objections': OBJECTIONS}


def write_reports(payload):
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Dealix S9 Revenue Machine', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Top Accounts')
    for row in payload['top_accounts']:
        lines.append(f"- **{row['account']['name']}** — score `{row['score']}` — offer `{row['offer']['name']}`")
    (REPORT / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload):
    errors = []
    if payload['summary']['live'] != 0:
        errors.append('live must be zero')
    if payload['summary']['accounts'] < 5:
        errors.append('accounts missing')
    if payload['summary']['offers'] < 3:
        errors.append('offers missing')
    if payload['summary']['followups'] < 15:
        errors.append('followups missing')
    for row in payload['ranked_accounts']:
        if not row['discovery_script'] or not row['followups']:
            errors.append('missing sales assets')
    return errors


def main():
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('S9_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
