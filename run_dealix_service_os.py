from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import rcmax
import auto14
import client_ops_max
import deal_conversation_intelligence as dci
import deal_strategy_brain as dsb
import client_service_autopilot as csa

REPORT_DIR = Path('reports/commercial/service_os')


def run_all() -> dict[str, Any]:
    rcmax_payload = rcmax.build_payload()
    rcmax.write_reports(rcmax_payload)
    rcmax_errors = rcmax.verify(rcmax_payload)

    auto14_payload = auto14.build_payload()
    auto14.write_reports(auto14_payload)
    auto14_errors = auto14.verify(auto14_payload)

    ops_payload = client_ops_max.build_payload()
    client_ops_max.write_reports(ops_payload)
    ops_errors = client_ops_max.verify(ops_payload)

    dci_payload = dci.build_payload()
    dci.write_reports(dci_payload)
    dci_errors = dci.verify(dci_payload)

    dsb_payload = dsb.build_payload()
    dsb.write_reports(dsb_payload)
    dsb_errors = dsb.verify(dsb_payload)

    csa_payload = csa.build_payload()
    csa.write_reports(csa_payload)
    csa_errors = csa.verify(csa_payload)

    status = {
        'RCMAX_READY': 0 if rcmax_errors else 1,
        'AUTO14_READY': 0 if auto14_errors else 1,
        'CLIENT_OPS_MAX_READY': 0 if ops_errors else 1,
        'CONVERSATION_INTELLIGENCE_READY': 0 if dci_errors else 1,
        'DEAL_STRATEGY_READY': 0 if dsb_errors else 1,
        'CLIENT_AUTOPILOT_READY': 0 if csa_errors else 1,
        'LIVE_SENDS': 0,
        'FINAL_COMMITMENTS': 0,
    }
    all_ok = all(v == 1 or v == 0 and k in ('LIVE_SENDS', 'FINAL_COMMITMENTS') for k, v in status.items())
    ready_flags = {k: v for k, v in status.items() if k.endswith('_READY')}
    status['DEALIX_SERVICE_OS_READY'] = 1 if all(v == 1 for v in ready_flags.values()) else 0

    return {
        'status': status,
        'errors': {
            'rcmax': rcmax_errors,
            'auto14': auto14_errors,
            'client_ops_max': ops_errors,
            'conversation_intelligence': dci_errors,
            'deal_strategy': dsb_errors,
            'client_autopilot': csa_errors,
        },
        'rcmax_command': rcmax_payload['command'],
        'auto14_summary': auto14_payload['summary'],
        'ops_summary': ops_payload['summary'],
        'dci_summary': dci_payload['summary'],
        'dsb_summary': dsb_payload['summary'],
        'csa_summary': csa_payload['summary'],
    }


def write_reports(payload: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
    status = payload['status']
    lines = ['# Dealix Service OS — Status Report', '']
    for key, value in status.items():
        lines.append(f'- {key}: `{value}`')
    lines.append('\n## Errors')
    for module, errs in payload['errors'].items():
        if errs:
            lines.append(f'### {module}')
            for e in errs:
                lines.append(f'- {e}')
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main() -> int:
    payload = run_all()
    write_reports(payload)
    status = payload['status']
    for key, value in status.items():
        print(f'{key}={value}')
    all_errors = [e for errs in payload['errors'].values() for e in errs]
    return 1 if all_errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
