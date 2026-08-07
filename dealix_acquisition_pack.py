from __future__ import annotations

import json
from pathlib import Path

import dealix_revenue_machine

REPORT = Path('reports/commercial/t10')

SECTOR_OFFERS = {
    'clinics': {
        'title': 'Clinic Follow-up Command Sprint',
        'pain': 'missed inquiries, WhatsApp overload, and weak follow-up visibility',
        'promise': 'build a daily review system for inquiries, follow-ups, and proof',
        'entry_offer': '7 day command sprint',
        'proof': 'daily inquiry and follow-up command report',
    },
    'agencies': {
        'title': 'Agency Client Command Room',
        'pain': 'client reporting, campaign follow-up, and delivery visibility',
        'promise': 'turn client growth work into tracked actions and proof',
        'entry_offer': 'managed command room',
        'proof': 'weekly client operating proof pack',
    },
    'training': {
        'title': 'Training Lead Conversion OS',
        'pain': 'lead conversion, cohort follow-up, and sales discipline',
        'promise': 'organize leads, follow-ups, and enrollment actions',
        'entry_offer': '14 day growth operating system',
        'proof': 'lead movement and follow-up proof report',
    },
    'logistics': {
        'title': 'B2B Pipeline Command Room',
        'pain': 'pipeline visibility, partner motion, and scattered account follow-up',
        'promise': 'create a controlled command queue for deals and partners',
        'entry_offer': '14 day growth operating system',
        'proof': 'account and partner movement report',
    },
}


def build_one_page_offer(sector: str, offer: dict) -> dict:
    return {
        'sector': sector,
        'headline': offer['title'],
        'problem': offer['pain'],
        'solution': offer['promise'],
        'start_with': offer['entry_offer'],
        'proof_asset': offer['proof'],
        'cta': 'Book a short operating review',
        'review_required': True,
    }


def proposal_template(sector: str, offer: dict) -> dict:
    return {
        'title': offer['title'] + ' Proposal',
        'scope': ['map current flow', 'create command queue', 'prepare draft routes', 'produce proof report'],
        'not_in_scope': ['final legal terms', 'guaranteed revenue', 'unapproved live sending'],
        'inputs_needed': ['current channels', 'sample leads', 'owner list', 'approval rules'],
        'timeline': '7 to 14 days depending on package',
        'commercial_note': 'final price requires scope review',
        'sector': sector,
    }


def first_touch_drafts(sector: str, offer: dict) -> dict:
    return {
        'email_subject': f"Quick idea for {sector} follow-up operations",
        'email_body': f"I noticed many {sector} teams lose value after the first inquiry. Dealix can start with a small {offer['entry_offer']} to map follow-up, prepare a daily command queue, and produce a proof report before any larger rollout.",
        'whatsapp_body': f"Hi, quick idea: Dealix can help {sector} teams organize follow-ups and proof using a small {offer['entry_offer']} first. Happy to share a one-page view.",
        'linkedin_manual_note': f"Manual note only: ask if the team has a clear daily follow-up command report for {sector} operations.",
        'mode': 'draft_only',
    }


def discovery_script(sector: str, offer: dict) -> list[str]:
    return [
        f'What happens after a new inquiry reaches your {sector} team?',
        'Who owns the next follow-up and how is it tracked?',
        'Which channel creates the most missed opportunities?',
        'What should leadership see every day to trust the process?',
        f'Would a small {offer["entry_offer"]} be a reasonable first step?',
    ]


def build_payload() -> dict:
    revenue = dealix_revenue_machine.build_payload()
    packs = []
    for sector, offer in SECTOR_OFFERS.items():
        packs.append({
            'sector': sector,
            'one_page_offer': build_one_page_offer(sector, offer),
            'proposal_template': proposal_template(sector, offer),
            'drafts': first_touch_drafts(sector, offer),
            'discovery_script': discovery_script(sector, offer),
        })
    founder_command = {
        'today': 'Pick one sector, review top three accounts, prepare drafts, and approve only reviewed actions.',
        'top_sector': revenue['top_accounts'][0]['account']['sector'],
        'top_account': revenue['top_accounts'][0]['account']['name'],
        'top_offer': revenue['top_accounts'][0]['offer']['name'],
        'review_required': True,
        'live': 0,
    }
    summary = {
        'sector_packs': len(packs),
        'proposal_templates': len(packs),
        'email_drafts': len(packs),
        'whatsapp_drafts': len(packs),
        'discovery_scripts': len(packs),
        'revenue_accounts': revenue['summary']['accounts'],
        'live': 0,
    }
    return {'summary': summary, 'packs': packs, 'founder_command': founder_command}


def write_reports(payload: dict) -> None:
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Dealix T10 Client Acquisition Pack', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Sector Packs')
    for pack in payload['packs']:
        lines.append(f"- **{pack['sector']}** — {pack['one_page_offer']['headline']}")
    lines.append('\n## Founder Command')
    lines.append(payload['founder_command']['today'])
    (REPORT / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload: dict) -> list[str]:
    errors = []
    if payload['summary']['live'] != 0:
        errors.append('live must be zero')
    if payload['summary']['sector_packs'] != 4:
        errors.append('sector packs missing')
    for pack in payload['packs']:
        if not pack['one_page_offer'] or not pack['proposal_template'] or not pack['drafts']:
            errors.append('pack missing assets')
        if pack['drafts']['mode'] != 'draft_only':
            errors.append('drafts must stay draft_only')
    return errors


def main() -> int:
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('T10_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
