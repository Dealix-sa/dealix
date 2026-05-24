#!/usr/bin/env python3
"""First revenue playbook checklist — tracks founder actions (read-only scan)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CHECKS = [
    {
        "id": "warm_messages_doc",
        "path": "docs/FIRST_10_WARM_MESSAGES_AR_EN.md",
        "label_ar": "قوالب 10 رسائل دافئة",
    },
    {
        "id": "playbook_doc",
        "path": "docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md",
        "label_ar": "دليل أول إيراد 14 يوم",
    },
    {
        "id": "first_3_board",
        "path": "docs/FIRST_3_CUSTOMER_LOOP_BOARD.md",
        "label_ar": "لوحة أول 3 عملاء",
    },
    {
        "id": "daily_sales_pack_api",
        "path": "auto_client_acquisition/founder/daily_sales_pack.py",
        "label_ar": "حزمة مبيعات يومية API",
    },
    {
        "id": "lead_intake_ui",
        "path": "frontend/src/components/leads/LeadIntakeForm.tsx",
        "label_ar": "نموذج استقبال ليد في الواجهة",
    },
]


def build_status() -> dict:
    items = []
    for c in CHECKS:
        p = ROOT / c["path"]
        items.append({
            **c,
            "present": p.is_file(),
            "status": "ready" if p.is_file() else "missing",
        })
    ready = sum(1 for i in items if i["present"])
    return {
        "schema_version": 1,
        "checks": items,
        "ready_count": ready,
        "total": len(items),
        "verdict": "READY" if ready == len(items) else "PARTIAL",
        "founder_actions_ar": [
            "اعتمد 10 رسائل دافئة من docs/FIRST_10_WARM_MESSAGES_AR_EN.md عبر مركز الموافقات",
            "نفّذ 3 تشخيصات مدفوعة عبر commercial/engagements",
            "سلّم Proof Pack لكل عميل قبل أي upsell",
        ],
    }


def main() -> int:
    report = build_status()
    print(f"FIRST_REVENUE_PLAYBOOK_VERDICT={report['verdict']}")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
