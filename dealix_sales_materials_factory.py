from __future__ import annotations

import json
from pathlib import Path

import dealix_acquisition_pack

REPORT = Path('reports/commercial/u11')

OBJECTION_BATTLECARDS = {
    'price': {
        'concern': 'price feels high before proof',
        'response': 'start with a smaller sprint and prove the operating workflow first',
        'safe_offer': '7 day command sprint',
    },
    'timing': {
        'concern': 'not ready this month',
        'response': 'start with a light diagnostic that needs minimal inputs',
        'safe_offer': 'operating review',
    },
    'trust': {
        'concern': 'need confidence before changing process',
        'response': 'show proof reports and review gates before rollout',
        'safe_offer': 'proof first sprint',
    },
    'details': {
        'concern': 'needs more clarity',
        'response': 'send a clear one page scope, inputs, and next step brief',
        'safe_offer': 'non binding brief',
    },
}

PRICING_MENU = [
    {'name': '7 day command sprint', 'range': '5000-12000 SAR', 'use_when': 'client needs fast proof'},
    {'name': '14 day growth operating system', 'range': '15000-35000 SAR', 'use_when': 'client needs repeatable workflow'},
    {'name': 'managed command room', 'range': '5000-25000 SAR monthly', 'use_when': 'client needs ongoing operation'},
]


def one_page_offer(pack: dict) -> str:
    offer = pack['one_page_offer']
    return '\n'.join([
        f"# {offer['headline']}",
        '',
        f"Problem: {offer['problem']}",
        f"Solution: {offer['solution']}",
        f"Start with: {offer['start_with']}",
        f"Proof asset: {offer['proof_asset']}",
        f"CTA: {offer['cta']}",
        '',
        'Review required before use.',
    ])


def proposal_markdown(pack: dict) -> str:
    proposal = pack['proposal_template']
    lines = [f"# {proposal['title']}", '', '## Scope']
    lines.extend(f"- {item}" for item in proposal['scope'])
    lines.append('\n## Not in scope')
    lines.extend(f"- {item}" for item in proposal['not_in_scope'])
    lines.append('\n## Inputs needed')
    lines.extend(f"- {item}" for item in proposal['inputs_needed'])
    lines.append(f"\nTimeline: {proposal['timeline']}")
    lines.append(f"Commercial note: {proposal['commercial_note']}")
    return '\n'.join(lines) + '\n'


def email_sequence(pack: dict) -> list[dict]:
    sector = pack['sector']
    headline = pack['one_page_offer']['headline']
    return [
        {'day': 0, 'subject': f'Quick idea for {sector}', 'body': f'Share the {headline} one page view.', 'mode': 'draft_only'},
        {'day': 2, 'subject': f'Proof example for {sector}', 'body': 'Share a sample operating proof summary.', 'mode': 'draft_only'},
        {'day': 5, 'subject': 'Small sprint option', 'body': 'Suggest a small reviewed sprint before any rollout.', 'mode': 'draft_only'},
    ]


def whatsapp_sequence(pack: dict) -> list[dict]:
    sector = pack['sector']
    return [
        {'day': 0, 'body': f'Quick idea for {sector}: a small command sprint to organize follow up and proof.', 'mode': 'draft_only'},
        {'day': 2, 'body': 'Can I share a one page example of the daily command report?', 'mode': 'draft_only'},
        {'day': 5, 'body': 'A small reviewed sprint may be enough to prove the workflow first.', 'mode': 'draft_only'},
    ]


def linkedin_posts(pack: dict) -> list[str]:
    sector = pack['sector']
    return [
        f'Many {sector} teams do not lose opportunities because of demand. They lose them after the first inquiry because follow up is not visible.',
        f'A command room for {sector} should show owners, follow ups, approvals, and proof every day.',
    ]


def landing_copy(pack: dict) -> dict:
    offer = pack['one_page_offer']
    return {
        'hero': offer['headline'],
        'subhero': offer['solution'],
        'problem': offer['problem'],
        'cta': 'Book an operating review',
        'proof': offer['proof_asset'],
    }


def proof_pack_template(pack: dict) -> dict:
    return {
        'sector': pack['sector'],
        'sections': ['baseline', 'actions prepared', 'approvals reviewed', 'follow ups drafted', 'proof produced', 'next decisions'],
        'review_required': True,
    }


def build_payload() -> dict:
    acquisition = dealix_acquisition_pack.build_payload()
    materials = []
    for pack in acquisition['packs']:
        materials.append({
            'sector': pack['sector'],
            'one_page_offer': one_page_offer(pack),
            'proposal_markdown': proposal_markdown(pack),
            'email_sequence': email_sequence(pack),
            'whatsapp_sequence': whatsapp_sequence(pack),
            'linkedin_posts': linkedin_posts(pack),
            'landing_copy': landing_copy(pack),
            'proof_pack_template': proof_pack_template(pack),
            'mode': 'draft_only',
        })
    summary = {
        'sectors': len(materials),
        'one_page_offers': len(materials),
        'proposals': len(materials),
        'email_sequences': len(materials),
        'whatsapp_sequences': len(materials),
        'linkedin_post_sets': len(materials),
        'landing_pages': len(materials),
        'proof_templates': len(materials),
        'battlecards': len(OBJECTION_BATTLECARDS),
        'pricing_items': len(PRICING_MENU),
        'live': 0,
    }
    return {'summary': summary, 'materials': materials, 'battlecards': OBJECTION_BATTLECARDS, 'pricing_menu': PRICING_MENU}


def write_reports(payload: dict) -> None:
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Dealix U11 Sales Materials Factory', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Materials')
    for material in payload['materials']:
        lines.append(f"- **{material['sector']}** — one-page, proposal, sequences, landing, proof template")
    (REPORT / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload: dict) -> list[str]:
    errors = []
    if payload['summary']['live'] != 0:
        errors.append('live must be zero')
    if payload['summary']['sectors'] != 4:
        errors.append('sector material missing')
    if payload['summary']['battlecards'] < 4:
        errors.append('battlecards missing')
    if payload['summary']['pricing_items'] < 3:
        errors.append('pricing missing')
    for material in payload['materials']:
        if material['mode'] != 'draft_only':
            errors.append('materials must stay draft_only')
        if len(material['email_sequence']) != 3 or len(material['whatsapp_sequence']) != 3:
            errors.append('sequence missing')
    return errors


def main() -> int:
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('U11_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
