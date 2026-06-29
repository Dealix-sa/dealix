from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import dealix_acquisition_pack
import dealix_gtm_launch_kit
import dealix_revenue_machine
import dealix_sales_materials_factory

REPORT_DIR = Path('reports/commercial/rcmax')

SERVICE_STAGES = [
    {'stage': 'intake', 'owner': 'Founder', 'output': 'client inputs collected'},
    {'stage': 'diagnosis', 'owner': 'Delivery', 'output': 'workflow and owner map'},
    {'stage': 'queue', 'owner': 'Ops', 'output': 'daily command queue'},
    {'stage': 'drafting', 'owner': 'Sales', 'output': 'reviewed draft routes'},
    {'stage': 'approval', 'owner': 'Client Owner', 'output': 'approved next actions'},
    {'stage': 'proof', 'owner': 'Dealix', 'output': 'proof report'},
    {'stage': 'expansion', 'owner': 'Founder', 'output': 'next plan or managed room offer'},
]

CLIENT_INPUTS = ['channels', 'sample opportunities', 'owners', 'approval rules', 'proof target', 'weekly review time']
CLIENT_OUTPUTS = ['workflow map', 'owner map', 'action queue', 'draft routes', 'proof report', 'next plan']
RISK_GATES = ['no live sending without review', 'no guaranteed revenue claim', 'no final legal terms', 'no final price without scope']


def _top_account(revenue: dict[str, Any]) -> dict[str, Any]:
    return revenue['top_accounts'][0]


def _service_blueprint(top: dict[str, Any]) -> dict[str, Any]:
    return {
        'service_name': 'Dealix Growth Command Sprint',
        'sector': top['account']['sector'],
        'client_problem': top['account']['pain'],
        'inputs_needed': CLIENT_INPUTS,
        'stages': SERVICE_STAGES,
        'client_outputs': CLIENT_OUTPUTS,
        'success_metrics': ['reviewed opportunities', 'owners assigned', 'draft routes prepared', 'proof items delivered'],
        'risk_gates': RISK_GATES,
    }


def _pricing_guidance(top: dict[str, Any]) -> dict[str, Any]:
    offer = top['offer']['name']
    if '7 day' in offer:
        price = '5000-12000 SAR'
    elif '14 day' in offer:
        price = '15000-35000 SAR'
    else:
        price = '5000-25000 SAR monthly'
    return {
        'offer': offer,
        'suggested_range': price,
        'pricing_rule': 'final price only after scope, channels, owners, and proof depth are reviewed',
        'do_not_commit': ['discount', 'guaranteed result', 'legal terms', 'live sending'],
    }


def _proposal_folder(top: dict[str, Any], acquisition: dict[str, Any]) -> dict[str, Any]:
    sector = top['account']['sector']
    pack = [item for item in acquisition['packs'] if item['sector'] == sector][0]
    return {
        'account': top['account']['name'],
        'sector': sector,
        'one_page_offer': pack['one_page_offer'],
        'proposal_template': pack['proposal_template'],
        'discovery_script': pack['discovery_script'],
        'drafts': pack['drafts'],
        'mode': 'draft_only',
    }


def build_payload() -> dict[str, Any]:
    gtm = dealix_gtm_launch_kit.build_payload()
    revenue = dealix_revenue_machine.build_payload()
    acquisition = dealix_acquisition_pack.build_payload()
    materials = dealix_sales_materials_factory.build_payload()
    top = _top_account(revenue)
    blueprint = _service_blueprint(top)
    proposal = _proposal_folder(top, acquisition)
    pricing = _pricing_guidance(top)
    command = {
        'account': top['account']['name'],
        'sector': top['account']['sector'],
        'score': top['score'],
        'offer': top['offer']['name'],
        'why_now': top['account']['pain'],
        'today_goal': 'prepare one reviewed proposal folder and book one operating review',
        'proof_target': 'first daily command report',
        'next_action': 'run discovery, confirm inputs, and prepare proof-first sprint proposal',
        'review_required': True,
        'live': 0,
    }
    operating_day = {
        'morning': ['review top account', 'review matched offer', 'confirm client problem'],
        'midday': ['prepare proposal folder', 'review draft outreach', 'prepare discovery questions'],
        'afternoon': ['book operating review', 'record outcome', 'update proof report'],
    }
    summary = {
        'target_companies': gtm['summary']['target_companies'],
        'first_10_companies': len(gtm['company_plan'][:10]),
        'materials_sectors': materials['summary']['sectors'],
        'top_account_score': top['score'],
        'service_stages': len(blueprint['stages']),
        'client_inputs': len(blueprint['inputs_needed']),
        'client_outputs': len(blueprint['client_outputs']),
        'risk_gates': len(RISK_GATES),
        'live': 0,
    }
    return {
        'summary': summary,
        'command': command,
        'operating_day': operating_day,
        'service_blueprint': blueprint,
        'proposal_folder': proposal,
        'pricing_guidance': pricing,
        'first_10_companies': gtm['company_plan'][:10],
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    lines = ['# RCMax Practical Revenue Command', '']
    for key, value in payload['summary'].items():
        lines.append(f'- {key}: `{value}`')
    lines += ['', '## Today', f"- Account: {payload['command']['account']}", f"- Offer: {payload['command']['offer']}", f"- Goal: {payload['command']['today_goal']}", '', '## Service Stages']
    for stage in payload['service_blueprint']['stages']:
        lines.append(f"- {stage['stage']} — {stage['owner']} — {stage['output']}")
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def verify(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload['summary']['live'] != 0 or payload['command']['live'] != 0:
        errors.append('live must be zero')
    if payload['summary']['target_companies'] != 30:
        errors.append('target companies must be 30')
    if payload['summary']['first_10_companies'] != 10:
        errors.append('first 10 companies missing')
    if payload['summary']['service_stages'] < 7:
        errors.append('service stages incomplete')
    if payload['proposal_folder']['mode'] != 'draft_only':
        errors.append('proposal folder must stay draft_only')
    if not payload['command']['account'] or not payload['command']['offer']:
        errors.append('command missing account or offer')
    return errors


def main() -> int:
    payload = build_payload()
    write_reports(payload)
    errors = verify(payload)
    print('RCMAX_READY=' + ('0' if errors else '1'))
    print(payload['summary'])
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
