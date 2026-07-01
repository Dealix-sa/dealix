#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.commercial.negotiation_operator import demo_negotiation_day, verify_negotiation_payload

REPORT_DIR = Path('reports/commercial/negotiation_operator')


def main() -> int:
    payload = demo_negotiation_day()
    failures = verify_negotiation_payload(payload)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / 'latest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = [
        '# Dealix Negotiation Operator Day',
        '',
        f"- generated_at: `{payload['generated_at']}`",
        f"- plans: `{payload['summary']['plans']}`",
        f"- approval_required: `{payload['summary']['approval_required']}`",
        f"- live_commitments: `{payload['summary']['live_commitments']}`",
        f"- can_send_without_review: `{payload['summary']['can_send_without_review']}`",
        '',
        '## Plans',
    ]
    for plan in payload['plans']:
        lines.extend([
            '',
            f"### {plan['company_name']}",
            f"- reply_type: `{plan['reply_type']}`",
            f"- next_action: `{plan['recommended_next_action']}`",
            f"- risk_level: `{plan['risk_level']}`",
            f"- approval_required: `{plan['approval_required']}`",
            f"- draft: {plan['draft_response_ar']}",
        ])
    (REPORT_DIR / 'latest.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('NEGOTIATION_OPERATOR_READY=' + ('0' if failures else '1'))
    print(f"PLANS={payload['summary']['plans']}")
    print(f"APPROVAL_REQUIRED={payload['summary']['approval_required']}")
    print(f"LIVE_COMMITMENTS={payload['summary']['live_commitments']}")
    print(f"CAN_SEND_WITHOUT_REVIEW={payload['summary']['can_send_without_review']}")
    print('REPORT_JSON=reports/commercial/negotiation_operator/latest.json')
    print('REPORT_MD=reports/commercial/negotiation_operator/latest.md')
    if failures:
        for failure in failures:
            print('FAIL: ' + failure)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
