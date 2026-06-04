#!/usr/bin/env python3
"""Master verifier for the Dealix Startup Operating System.

Verifies every OS area's docs, the vertical playbooks, required scripts, tests,
workflows, configs, the README section, and the daily output spine all exist.
Writes outputs/startup_os/startup_os_verification.{json,md}.

Exit 0 only if all CRITICAL checks pass. Read-only.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from startup_os_common import ROOT, now_iso, write_json  # noqa: E402
from startup_os_manifest import (  # noqa: E402
    OS_AREAS,
    REQUIRED_CONFIGS,
    REQUIRED_SCRIPTS,
    REQUIRED_TESTS,
    REQUIRED_WORKFLOWS,
    VERTICAL_DOCS,
)


def _exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def verify() -> dict:
    checks: list[dict] = []

    def add(name: str, missing: list[str], critical: bool = True) -> None:
        checks.append({
            "check": name,
            "ok": not missing,
            "missing": missing,
            "critical": critical,
        })

    # OS doc trees
    for area_key, area in OS_AREAS.items():
        missing = [f"{area['dir']}/{d}" for d in area["docs"] if not _exists(f"{area['dir']}/{d}")]
        add(f"os:{area_key}", missing)

    # Vertical playbooks
    add("verticals", [f"docs/commercial-launch/verticals/{v}" for v in VERTICAL_DOCS if not _exists(f"docs/commercial-launch/verticals/{v}")])

    # Scripts / tests / workflows / configs
    add("scripts", [s for s in REQUIRED_SCRIPTS if not _exists(s)])
    add("tests", [t for t in REQUIRED_TESTS if not _exists(t)])
    add("workflows", [w for w in REQUIRED_WORKFLOWS if not _exists(w)])
    add("configs", [c for c in REQUIRED_CONFIGS if not _exists(c)])

    # API QA doc
    add("api_qa_doc", [] if _exists("docs/ops/API_COMMERCIAL_LAUNCH_QA.md") else ["docs/ops/API_COMMERCIAL_LAUNCH_QA.md"])

    # 99 reports present across areas
    missing_reports = []
    for area in OS_AREAS.values():
        rep = next((d for d in area["docs"] if d.startswith("99_")), None)
        if rep and not _exists(f"{area['dir']}/{rep}"):
            missing_reports.append(f"{area['dir']}/{rep}")
    add("reports", missing_reports)

    # README mentions the Startup OS
    readme = ROOT / "README.md"
    readme_ok = readme.exists() and "Startup Operating System" in readme.read_text(encoding="utf-8")
    add("readme", [] if readme_ok else ["README.md missing 'Startup Operating System' section"])

    critical_failures = [c for c in checks if c["critical"] and not c["ok"]]
    passed = not critical_failures

    total_docs = sum(len(a["docs"]) for a in OS_AREAS.values()) + len(VERTICAL_DOCS)
    report = {
        "generated_at": now_iso(),
        "passed": passed,
        "os_areas": len(OS_AREAS),
        "total_docs_expected": total_docs,
        "checks": checks,
        "critical_failures": [c["check"] for c in critical_failures],
        "decision": "PASS" if passed else "FAIL",
    }

    out_dir = ROOT / "outputs" / "startup_os"
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / "startup_os_verification.json", report)

    md = [
        "# Startup OS Verification",
        "",
        f"- Generated: {report['generated_at']}",
        f"- Decision: **{report['decision']}**",
        f"- OS areas: {report['os_areas']}",
        f"- Docs expected: {report['total_docs_expected']}",
        "",
        "| Check | OK | Missing |",
        "|---|---|---|",
    ]
    for c in checks:
        md.append(f"| {c['check']} | {'✅' if c['ok'] else '❌'} | {len(c['missing'])} |")
    (out_dir / "startup_os_verification.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return report


def main() -> int:
    r = verify()
    print(f"Startup OS verification: {r['decision']} ({r['os_areas']} areas, {r['total_docs_expected']} docs expected)")
    if not r["passed"]:
        for c in r["checks"]:
            if not c["ok"]:
                print(f"  FAIL {c['check']}: {c['missing'][:5]}")
    return 0 if r["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
