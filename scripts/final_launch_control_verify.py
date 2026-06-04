#!/usr/bin/env python3
"""Final Launch Control Tower verification.

The single GO/NO-GO gate. Reads the artifacts produced by the launch pipeline
and verifies the whole OS is present and safe:

- 400+ review-only drafts generated (daily_metrics.target_met),
- safety audit passed (no external send capability),
- all mandatory draft safety flags correct,
- CRM schema valid, media OS present, site launch checks pass,
- API static check pass, secret + risk scan pass,
- the four launch workflows exist,
- the section OS docs and final reports exist,
- README references the launch OS.

Writes outputs/final_launch_control/final_verification.{json,md}. Exits 0 only
if every critical check passes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import (
    COMMERCIAL_OUTPUTS,
    CONTROL_OUTPUTS,
    MEDIA_OUTPUTS,
    OUTPUTS_DIR,
    ROOT,
    today_str,
    write_json,
    write_text,
)

WORKFLOWS = [
    ".github/workflows/commercial-draft-factory.yml",
    ".github/workflows/media-social-calendar.yml",
    ".github/workflows/site-commercial-verify.yml",
    ".github/workflows/final-launch-control.yml",
]

FINAL_REPORTS = [
    "docs/company-os/99_COMPANY_OS_REPORT.md",
    "docs/site-launch/99_SITE_LAUNCH_REPORT.md",
    "docs/commercial-launch/99_FINAL_COMMERCIAL_LAUNCH_REPORT.md",
    "docs/media-social-os/99_MEDIA_SOCIAL_READY_REPORT.md",
    "docs/delivery-os/99_DELIVERY_READINESS_REPORT.md",
    "docs/analytics-os/99_ANALYTICS_READY_REPORT.md",
    "docs/go-live/99_GO_LIVE_REPORT.md",
    "docs/launch-control/99_FINAL_CONTROL_TOWER_REPORT.md",
]

OS_DOCS = [
    "docs/company-os/00_DEALIX_COMPANY_OS.md",
    "docs/commercial-launch/00_COMMERCIAL_LAUNCH_OS.md",
    "docs/media-social-os/00_MEDIA_SOCIAL_OS.md",
    "docs/delivery-os/00_DELIVERY_OS.md",
    "docs/analytics-os/00_ANALYTICS_OS.md",
    "docs/go-live/00_EXTERNAL_GO_LIVE_REQUIREMENTS.md",
    "docs/launch-control/00_FINAL_LAUNCH_CONTROL_TOWER.md",
]


def _read_json(path: Path) -> dict[str, Any]:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def run(day: str) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, critical: bool = True, detail: str = "") -> None:
        checks.append({"check": name, "passed": bool(ok), "critical": critical, "detail": detail})

    daily = _read_json(COMMERCIAL_OUTPUTS / day / "daily_metrics.json")
    add(
        "drafts_generated>=400",
        daily.get("drafts_generated", 0) >= 400,
        detail=str(daily.get("drafts_generated")),
    )
    add("draft_target_met", bool(daily.get("target_met")))

    safety = _read_json(COMMERCIAL_OUTPUTS / day / "safety_audit.json")
    add(
        "safety_audit_pass",
        bool(safety.get("passed")),
        detail=f"code_violations={len(safety.get('code_violations', []))}, "
        f"flag_violations={len(safety.get('flag_violations', []))}",
    )

    # Re-verify the draft safety flags directly from the queue.
    from _commercial_common import read_jsonl  # local import to keep top clean

    drafts = read_jsonl(COMMERCIAL_OUTPUTS / day / "draft_queue.jsonl")
    flags_ok = bool(drafts) and all(
        d.get("send_allowed") is False
        and d.get("external_send_blocked") is True
        and d.get("no_auto_send") is True
        and d.get("requires_founder_approval") is True
        for d in drafts
    )
    add("draft_safety_flags", flags_ok, detail=f"{len(drafts)} drafts")

    # CRM schema.
    from commercial_crm_schema_verify import verify as crm_verify

    crm_errors = crm_verify()
    add("crm_schema_valid", not crm_errors, detail=f"{len(crm_errors)} errors")

    # Media OS.
    media_cal = MEDIA_OUTPUTS / day / "content_calendar.json"
    add("media_calendar_generated", media_cal.exists(), critical=False)
    add("media_os_docs", (ROOT / "docs/media-social-os/03_30_DAY_CONTENT_CALENDAR.md").exists())

    # Site launch.
    site_report = _read_json(OUTPUTS_DIR / "site_launch" / day / "site_launch_report.json")
    add(
        "site_launch_pass",
        bool(site_report.get("passed")) or site_report.get("skipped", False),
        detail=f"errors={len(site_report.get('errors', []))}",
    )

    # API static check.
    api_report = _read_json(OUTPUTS_DIR / "api" / day / "api_commercial_qa.json")
    add(
        "api_commercial_pass",
        bool(api_report.get("passed")) or api_report.get("skipped", False),
        detail=f"errors={len(api_report.get('errors', []))}",
    )

    # Secret + risk scan.
    secret_report = _read_json(CONTROL_OUTPUTS / "secret_risk_scan.json")
    add(
        "secret_risk_scan_pass",
        bool(secret_report.get("passed")),
        detail=f"secrets={len(secret_report.get('secrets', []))}, "
        f"claims={len(secret_report.get('forbidden_claims', []))}",
    )

    # Delivery OS docs.
    add("delivery_os_docs", (ROOT / "docs/delivery-os/00_DELIVERY_OS.md").exists())

    # Workflows.
    for wf in WORKFLOWS:
        add(f"workflow:{Path(wf).name}", (ROOT / wf).exists())

    # OS section docs.
    for doc in OS_DOCS:
        add(f"doc:{Path(doc).name}", (ROOT / doc).exists())

    # Final reports.
    for rep in FINAL_REPORTS:
        add(f"report:{Path(rep).name}", (ROOT / rep).exists())

    # README references.
    readme = ROOT / "README.md"
    readme_ok = readme.exists() and "Launch Company OS" in readme.read_text(
        encoding="utf-8", errors="ignore"
    )
    add("readme_updated", readme_ok)

    critical_failed = [c for c in checks if c["critical"] and not c["passed"]]
    return {
        "date": day,
        "passed": not critical_failed,
        "decision": "GO" if not critical_failed else "NO-GO",
        "total_checks": len(checks),
        "passed_checks": sum(1 for c in checks if c["passed"]),
        "failed_critical": len(critical_failed),
        "checks": checks,
        "go_scope": [
            "public website launch",
            "commercial positioning",
            "400 review-only drafts",
            "founder manual review",
            "media/social planning",
            "manual social posting",
            "paid diagnostics",
            "discovery calls",
            "proposals",
            "pilot planning",
            "analytics schema",
            "delivery preparation",
        ],
        "no_go_scope": [
            "automated email sending",
            "WhatsApp cold outreach",
            "LinkedIn automation",
            "website form auto-submit",
            "bulk sending",
            "paid ads live launch without tracking/compliance",
            "processing sensitive data before agreement",
            "external sending from GitHub Actions",
        ],
    }


def _write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        f"# Final Launch Control — Verification ({report['date']})",
        "",
        f"## Decision: **{report['decision']}**",
        "",
        f"- Checks passed: {report['passed_checks']} / {report['total_checks']}",
        f"- Critical failures: {report['failed_critical']}",
        "",
        "| Check | Critical | Result | Detail |",
        "|-------|----------|--------|--------|",
    ]
    for c in report["checks"]:
        lines.append(
            f"| {c['check']} | {'yes' if c['critical'] else 'no'} | "
            f"{'PASS' if c['passed'] else 'FAIL'} | {c['detail']} |"
        )
    lines += [
        "",
        "## GO scope (allowed)",
        *[f"- {x}" for x in report["go_scope"]],
        "",
        "## NO-GO scope (blocked)",
        *[f"- {x}" for x in report["no_go_scope"]],
        "",
        "> AI drafts, ranks, and recommends. Founder reviews, approves, and sends manually. "
        "The system never sends externally.",
    ]
    write_text(path, "\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Final launch control verification.")
    parser.add_argument("--date", default=today_str())
    args = parser.parse_args()

    report = run(args.date)
    write_json(CONTROL_OUTPUTS / "final_verification.json", report)
    _write_markdown(report, CONTROL_OUTPUTS / "final_verification.md")

    print(
        f"FINAL LAUNCH CONTROL: {report['decision']} — "
        f"{report['passed_checks']}/{report['total_checks']} checks passed."
    )
    if not report["passed"]:
        for c in report["checks"]:
            if c["critical"] and not c["passed"]:
                print(f"  - FAIL: {c['check']} {c['detail']}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
