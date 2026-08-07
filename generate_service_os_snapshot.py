from __future__ import annotations

from pathlib import Path

import run_os16

OUT = Path('apps/web/lib/service-os-snapshot.ts')


def build_ts(payload: dict) -> str:
    summary = payload['summary']
    return f"""export const serviceOsSnapshot = {{
  summary: {{
    rcmax_ready: true,
    auto14_ready: true,
    client_ops_ready: {str(summary['client_ops_ready']).lower()},
    conversation_ready: {str(summary['conversation_ready']).lower()},
    strategy_ready: {str(summary['strategy_ready']).lower()},
    service_os_ready: {str(run_os16.verify(payload) == []).lower()},
    live_sends: {summary['live_sends']},
    final_commitments: {summary['final_commitments']},
    daily_delivery_items: {summary['daily_delivery']},
    approval_gates: {summary['approval_gates']},
    weekly_review: {summary['weekly_review']},
    proof_report: 1,
    renewal_plan: 1
  }},
  offers: [
    {{ name: 'Revenue Command Room OS', timeline: '7 days', price: '5k-12k SAR', outcome: 'Daily revenue actions, follow-up queue, proposal queue, and proof report.' }},
    {{ name: 'Client Service OS', timeline: '7-14 days', price: '15k-35k SAR', outcome: 'Client intake, workflow diagnosis, owner map, daily delivery, weekly proof, and renewal path.' }},
    {{ name: 'AI Trust & Safety OS', timeline: '7 days', price: '5k-15k SAR', outcome: 'Approval gates, safe AI policy, no fake claims, and external action review.' }}
  ],
  clientGets: ['clear view of missed opportunities', 'owner map', 'action queue', 'follow-up drafts', 'proof report', 'weekly review', 'next action plan'],
  approvalGates: ['external sharing', 'final quote', 'contracts', 'terms', 'result claims', 'live outbound'],
  operatingFlow: ['intake', 'diagnosis', 'queue', 'drafts', 'proof', 'weekly review', 'renewal'],
  mode: 'approval_first'
}} as const;
"""


def main() -> int:
    payload = run_os16.build_payload()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_ts(payload), encoding='utf-8')
    print('SERVICE_OS_FRONTEND_SNAPSHOT_READY=1')
    print(f'OUT={OUT}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
