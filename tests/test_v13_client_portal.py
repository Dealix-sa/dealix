"""Tests for V13 client portal + delivery workspace + proof rhythm."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

V13_FILES = [
    "business/_data/client_portal.demo.json",
    "business/_data/client_workspaces.json",
    "business/_schemas/client_workspace.schema.json",
    "apps/web/lib/client/portal.ts",
    "apps/web/components/client/ClientStatusCard.tsx",
    "apps/web/components/client/DeliverableList.tsx",
    "apps/web/components/client/ApprovalQueue.tsx",
    "apps/web/components/client/ProofTimeline.tsx",
    "apps/web/components/client/NextReviewPanel.tsx",
    "apps/web/components/client/ClientRiskBadge.tsx",
    "apps/web/app/client-portal/page.tsx",
    "apps/web/app/client-portal/demo/page.tsx",
    "apps/web/app/client-portal/[clientId]/page.tsx",
    "apps/web/app/delivery-workspace/page.tsx",
    "apps/web/app/proof-vault/page.tsx",
    "apps/web/app/client-success/page.tsx",
    "apps/web/app/retention/page.tsx",
    "business/delivery-workspace/DELIVERY_WORKSPACE_SYSTEM.md",
    "business/delivery-workspace/CLIENT_KICKOFF_SOP.md",
    "business/delivery-workspace/APPROVAL_GATE_POLICY.md",
    "business/delivery-workspace/DELIVERABLE_ACCEPTANCE_FLOW.md",
    "business/delivery-workspace/WEEKLY_CLIENT_REVIEW_RHYTHM.md",
    "business/delivery-workspace/DELIVERY_RISK_REGISTER.md",
    "business/proof/PROOF_REPORT_AR.md",
    "business/proof/PROOF_REPORT_EN.md",
    "business/proof/PROOF_ITEM_SCHEMA.md",
    "business/proof/CLIENT_SUCCESS_SIGNALS.md",
    "business/proof/RETAINER_EXPANSION_PLAYBOOK.md",
    "scripts/lib/workspace_store.py",
    "scripts/create_client_workspace.py",
    "scripts/add_deliverable.py",
    "scripts/mark_deliverable_done.py",
    "scripts/request_client_approval.py",
    "scripts/record_client_approval.py",
    "scripts/generate_client_status_report.py",
    "scripts/generate_retainer_expansion_plan.py",
    "scripts/generate_case_study_draft.py",
]


class TestV13(unittest.TestCase):
    def test_files_exist(self) -> None:
        missing = [p for p in V13_FILES if not (ROOT / p).exists()]
        self.assertEqual(missing, [], f"missing: {missing}")

    def test_workspace_create_flow(self) -> None:
        path = ROOT / "business/_data/client_workspaces.json"
        before = json.loads(path.read_text(encoding="utf-8"))
        try:
            out = subprocess.run(
                ["python3", str(ROOT / "scripts/create_client_workspace.py"),
                 "--account-id", "demo-acc-001",
                 "--client-name", "Demo Marketing Agency",
                 "--offer", "Revenue OS", "--demo"],
                cwd=ROOT, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(out.returncode, 0, msg=out.stderr)
            after = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(len(after["workspaces"]), len(before["workspaces"]) + 1)
            ws_id = after["workspaces"][-1]["clientId"]
            self.assertEqual(ws_id, "demo-acc-001")

            out2 = subprocess.run(
                ["python3", str(ROOT / "scripts/add_deliverable.py"),
                 "--client-id", "demo-acc-001",
                 "--title", "Workflow map"],
                cwd=ROOT, capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(out2.returncode, 0, msg=out2.stderr)
        finally:
            path.write_text(json.dumps(before, indent=2, ensure_ascii=False), encoding="utf-8")

    def test_demo_seed_marked_demo(self) -> None:
        data = json.loads((ROOT / "business/_data/client_portal.demo.json").read_text(encoding="utf-8"))
        self.assertTrue(data.get("demo"))


if __name__ == "__main__":
    unittest.main()
