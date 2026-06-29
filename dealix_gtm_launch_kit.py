from __future__ import annotations

import json
from pathlib import Path

import dealix_sales_materials_factory

REPORT = Path('reports/commercial/v12')

LAUNCH_CHECKLIST = [
    'select one primary sector',
    'review sector offer and proposal',
    'prepare first 30 company list',
    'approve draft sequences',
    'prepare proof pack template',
    'run daily operating console',
    'record owner decisions',
    'review weekly close plan',
]

SECTORS = ['clinics', 'agencies', 'training', 'logistics']


def build_company_plan() -> list[dict]:
    companies = []
    for idx in range(1, 31):
        sector = SECTORS[(idx - 1) % len(SECTORS)]
        companies.append({
            'company_id': f'gtm-{idx:03d}',
            'name': f'{sector.title()} Prospect {idx:02d}',
            'sector': sector,
            'priority': 100 - idx,
            'status': 'research_needed',
            'owner': 'Growth Director' if idx <= 15 else 'Sales Director',
            'next_step': 'prepare_account_brief',
            'review_required': True,
        })
    return companies


def campaign_calendar() -> list[dict]:
    return [
        {'day': 1, 'theme': 'sector selection and offer review', 'output': 'approved primary sector'},
        {'day': 2, 'theme': 'account research', 'output': 'first 30 company list'},
        {'day': 3, 'theme': 'draft sequence review', 'output': 'approved draft set'},
        {'day': 4, 'theme': 'proposal preparation', 'output': 'proposal briefs'},
        {'day': 5, 'theme': 'follow up and proof', 'output': 'proof summary'},
        {'day': 6, 'theme': 'objection review', 'output': 'battlecard updates'},
        {'day': 7, 'theme': 'close plan', 'output': 'weekly close plan'},
    ]


def proposal_folder(company: dict) -> dict:
    return {
        'folder_id': 'proposal-' + company['company_id'],
        'company_id': company['company_id'],
        'files': ['one_page_offer.md', 'proposal.md', 'discovery_script.md', 'proof_template.md'],
        'status': 'prepared_draft',
        'review_required': True,
    }


def onboarding_checklist() -> list[str]:
    return [
        'confirm client owner',
        'collect active channels',
        'collect sample leads or opportunities',
        'define approval rules',
        'define first proof metric',
        'schedule kickoff review',
        'prepare first daily command report',
    ]


def kpi_dashboard(companies: list[dict], folders: list[dict]) -> dict:
    return {
        'target_companies': len(companies),
        'proposal_folders': len(folders),
        'research_needed': len([c for c in companies if c['status'] == 'research_needed']),
        'review_required': len([c for c in companies if c['review_required']]),
        'primary_metric': 'reviewed opportunities per week',
        'live': 0,
    }


def build_payload() -> dict:
    materials = dealix_sales_materials_factory.build_payload()
    companies = build_company_plan()
    calendar = campaign_calendar()
    folders = [proposal_folder(c) for c in companies[:10]]
    onboarding = onboarding_checklist()
    kpis = kpi_dashboard(companies, folders)
    close_plan = [
        {'week': 1, 'goal': 'book 3 operating reviews', 'metric': 'meetings booked'},
        {'week': 2, 'goal': 'close 1 command sprint', 'metric': 'paid sprint'},
        {'week': 3, 'goal': 'deliver proof and expand', 'metric': 'proof accepted'},
        {'week': 4, 'goal': 'convert to monthly command room', 'metric': 'monthly proposal sent'},
    ]
    summary = {
        'checklist_items': len(LAUNCH_CHECKLIST),
        'target_companies': len(companies),
        'calendar_days': len(calendar),
        'proposal_folders': len(folders),
        'onboarding_steps': len(onboarding),
        'close_plan_weeks': len(close_plan),
        'sales_material_sectors': materials['summary']['sectors'],
        'live': 0,
    }
    return {
        'summary': summary,
        'launch_checklist': LAUNCH_CHECKLIST,
        'company_plan': companies,
        'campaign_calendar': calendar,
        'proposal_folders': folders,
        'onboarding_checklist': onboarding,
        'kpi_dashboard': kpis,
        'weekly_close_plan': close_plan,
    }


def write_reports(payload: dict) -> None:
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# Dealix V12 Go-To-Market Launch Kit', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Launch Checklist')
    for item in payload['launch_checklist']:
        lines.append(f'- {item}')
    lines.append('\n## Weekly Close Plan')
    for item in payload['weekly_close_plan']:
        lines.append(f"- Week {item['week']}: {item['goal']} — {item['metric']}")
    (REPORT / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload: dict) -> list[str]:
    errors = []
    if payload['summary']['live'] != 0:
        errors.append('live must be zero')
    if payload['summary']['target_companies'] != 30:
        errors.append('must have 30 target companies')
    if payload['summary']['proposal_folders'] < 10:
        errors.append('proposal folders missing')
    if payload['summary']['calendar_days'] != 7:
        errors.append('calendar must cover 7 days')
    if payload['summary']['close_plan_weeks'] != 4:
        errors.append('close plan must cover 4 weeks')
    return errors


def main() -> int:
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('V12_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
