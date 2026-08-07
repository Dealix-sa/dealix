"""Tests for V10 enterprise release baseline."""

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _exists(relpath: str) -> bool:
    return (ROOT / relpath).exists()


V10_FILES = [
    "business/enterprise/ENTERPRISE_READINESS_PACK.md",
    "business/enterprise/SECURITY_QUESTIONNAIRE_TEMPLATE.md",
    "business/enterprise/DATA_BOUNDARY_STATEMENT.md",
    "business/enterprise/AI_GOVERNANCE_STATEMENT.md",
    "business/enterprise/HUMAN_REVIEW_STATEMENT.md",
    "business/enterprise/SERVICE_LEVEL_BOUNDARIES.md",
    "business/enterprise/IMPLEMENTATION_ASSURANCE_PLAN.md",
    "business/enterprise/ENTERPRISE_BUYER_FAQ_AR.md",
    "business/enterprise/ENTERPRISE_BUYER_FAQ_EN.md",
    "apps/web/app/enterprise-readiness/page.tsx",
    "business/demo/DEALIX_DEMO_SCRIPT_AR.md",
    "business/demo/DEALIX_DEMO_SCRIPT_EN.md",
    "business/demo/FOUNDER_DEMO_FLOW.md",
    "business/demo/LIVE_WORKFLOW_REVIEW_SCRIPT.md",
    "business/demo/DEMO_QA_OBJECTIONS.md",
    "business/demo/DEMO_CLOSE.md",
    "scripts/generate_demo_pack.py",
    "scripts/generate_release_notes.py",
    "scripts/generate_health_snapshot.py",
    "scripts/check_required_env.py",
    "scripts/generate_env_report.py",
    "scripts/dealix_v10_run_all.sh",
]


class TestV10Baseline(unittest.TestCase):
    def test_all_v10_files_exist(self) -> None:
        missing = [p for p in V10_FILES if not _exists(p)]
        self.assertEqual(missing, [], f"missing V10 files: {missing}")

    def test_demo_pack_generates(self) -> None:
        out = subprocess.run(
            ["python3", str(ROOT / "scripts/generate_demo_pack.py"), "--lang", "both"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(out.returncode, 0, msg=out.stderr)
        for line in out.stdout.splitlines():
            if line.startswith("wrote "):
                p = Path(line.split(" ", 1)[1])
                self.assertTrue(p.exists(), f"missing output: {p}")

    def test_env_check_demo_passes(self) -> None:
        out = subprocess.run(
            ["python3", str(ROOT / "scripts/check_required_env.py"), "--mode", "demo"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(out.returncode, 0)

    def test_enterprise_readiness_page_no_unsupported_claims(self) -> None:
        text = (ROOT / "apps/web/app/enterprise-readiness/page.tsx").read_text(encoding="utf-8")
        banned = ["guaranteed", "نضمن", "SOC 2 certified", "ISO 27001 certified"]
        for b in banned:
            self.assertNotIn(b.lower(), text.lower(), f"banned claim found: {b}")


if __name__ == "__main__":
    unittest.main()
