#!/usr/bin/env python3
"""Verify the Documentation Governance OS (V9). Static, read-only.

Checks:
  * the governance docs exist and are substantive,
  * the Master Index exists and references the key V9 systems,
  * README references the most important systems,
  * V9 docs carry no stale legacy brand references (e.g. 'VoXc2', 'AI-CV'),
  * key V9 reports exist.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/docs-governance-os/00_DOCS_GOVERNANCE_OS.md",
    "docs/docs-governance-os/01_SOURCE_OF_TRUTH_RULES.md",
    "docs/docs-governance-os/02_DOC_OWNERSHIP.md",
    "docs/docs-governance-os/03_VERSIONING_POLICY.md",
    "docs/docs-governance-os/04_DEPRECATION_POLICY.md",
    "docs/docs-governance-os/05_LINK_CHECK_POLICY.md",
    "docs/docs-governance-os/99_DOCS_GOVERNANCE_REPORT.md",
    "docs/00_MASTER_INDEX.md",
    "docs/01_ALL_SYSTEMS_MAP.md",
]

KEY_REPORTS = [
    "docs/strategic-moat-os/99_STRATEGIC_MOAT_REPORT.md",
    "docs/enterprise-readiness-os/99_ENTERPRISE_READINESS_REPORT.md",
    "docs/trust-center-os/99_TRUST_CENTER_REPORT.md",
    "docs/qms-os/99_QMS_REPORT.md",
]

STALE_BRAND_TOKENS = ("VoXc2", "AI-CV")

V9_DOC_DIRS = [
    "docs/strategic-moat-os", "docs/enterprise-readiness-os", "docs/trust-center-os",
    "docs/demo-os", "docs/customer-lifecycle-os", "docs/delegation-os",
    "docs/agent-governance-os", "docs/cost-control-os", "docs/data-room-os",
    "docs/procurement-os", "docs/qms-os", "docs/docs-governance-os",
    "docs/deployment-verification-os",
]

MASTER_INDEX_MUST_MENTION = [
    "Strategic Moat OS", "Enterprise Readiness OS", "Trust Center OS",
    "Agent Governance OS", "Cost Control OS",
]


def _extra_checks() -> list[str]:
    problems: list[str] = []

    # Master index references key systems
    mi = v9_lib.REPO / "docs/00_MASTER_INDEX.md"
    if mi.is_file():
        text = mi.read_text(encoding="utf-8")
        for token in MASTER_INDEX_MUST_MENTION:
            if token not in text:
                problems.append(f"master index missing reference: {token}")

    # README mentions the most important systems
    readme = v9_lib.REPO / "README.md"
    if readme.is_file():
        rtext = readme.read_text(encoding="utf-8")
        for token in ("Strategic Moat OS", "Enterprise Readiness OS", "Master Index"):
            if token not in rtext:
                problems.append(f"README missing reference: {token}")
    else:
        problems.append("README.md missing")

    # Key reports exist
    for rep in KEY_REPORTS:
        if not (v9_lib.REPO / rep).is_file():
            problems.append(f"missing key report: {rep}")

    # No stale brand tokens in V9 docs
    for d in V9_DOC_DIRS:
        for path in (v9_lib.REPO / d).glob("*.md"):
            text = path.read_text(encoding="utf-8")
            for token in STALE_BRAND_TOKENS:
                if token in text:
                    problems.append(f"stale brand token '{token}' in {path.relative_to(v9_lib.REPO)}")
    return problems


def verify() -> dict:
    report = v9_lib.run_system_check("docs_governance", REQUIRED_FILES)
    extra = _extra_checks()
    report["governance_checks"] = extra
    if extra and report["verdict"] == "PASS":
        report["verdict"] = "FAIL"
        report["summary"]["violations"].append({"path": "docs", "violations": extra})
    # always persist with the extra checks attached
    (v9_lib.OUTPUT_DIR / "docs_governance.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
