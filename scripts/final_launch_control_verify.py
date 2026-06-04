#!/usr/bin/env python3
"""Master verification for the Dealix Final Launch Control Tower.

Proves the whole launch surface is present, review-only, and safe. Aggregates:
required files, required scripts, run outputs, draft guard-flag counts, safety
pass, README markers, and workflow safety (read-only perms, no send-secrets,
no SMTP/WhatsApp/LinkedIn automation terms in new commercial-launch code).

Writes:
- outputs/final_launch_control/final_verification.json
- outputs/final_launch_control/final_verification.md

Exit 0 iff all critical checks pass; 1 otherwise.

Usage:
    python scripts/final_launch_control_verify.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from launch_os import paths  # noqa: E402
from launch_os.compliance import find_external_send  # noqa: E402
from launch_os.verify import Check, summarize, print_checks  # noqa: E402

REQUIRED_REPORTS = (
    "docs/commercial-launch/99_FINAL_COMMERCIAL_LAUNCH_READINESS_REPORT.md",
    "docs/media-social-os/99_MEDIA_SOCIAL_READY_REPORT.md",
    "docs/site-launch/99_SITE_LAUNCH_REPORT.md",
    "docs/launch-control/99_FINAL_CONTROL_TOWER_REPORT.md",
    "README.md",
)

REQUIRED_WORKFLOWS = (
    ".github/workflows/commercial-draft-factory.yml",
    ".github/workflows/media-social-calendar.yml",
    ".github/workflows/site-commercial-verify.yml",
    ".github/workflows/final-launch-control.yml",
)

REQUIRED_SCRIPTS = (
    "scripts/commercial_generate_400_drafts.py",
    "scripts/commercial_safety_audit.py",
    "scripts/commercial_launch_readiness.py",
    "scripts/media_social_calendar_generate.py",
    "scripts/final_launch_control_verify.py",
    "scripts/site_launch_static_check.py",
    "scripts/media_social_verify.py",
    "scripts/commercial_crm_schema_verify.py",
    "scripts/api_commercial_static_check.py",
    "scripts/final_secret_and_risk_scan.py",
)

# New commercial-launch code surface that must be free of external-send patterns.
COMMERCIAL_CODE_GLOBS = ("launch_os/**/*.py", "scripts/commercial_*.py", "scripts/media_social_*.py")
# Modules that *define* the detection rules (and therefore legitimately name the
# forbidden patterns) are excluded from the self-scan to avoid false positives.
SCAN_EXCLUDE = {"compliance.py", "verify.py"}
TARGET = 400


def _exists(rel_path: str) -> Path:
    return paths.REPO_ROOT / rel_path


def run() -> dict:
    checks: list[Check] = []

    # 1) Required reports.
    for rp in REQUIRED_REPORTS:
        checks.append(Check(f"report::{rp}", _exists(rp).exists(), detail=rp))

    # 2) Required workflows.
    for wf in REQUIRED_WORKFLOWS:
        checks.append(Check(f"workflow::{wf.split('/')[-1]}", _exists(wf).exists(), detail=wf))

    # 3) Required scripts.
    for sc in REQUIRED_SCRIPTS:
        checks.append(Check(f"script::{sc.split('/')[-1]}", _exists(sc).exists(), critical=False, detail=sc))

    # 4) Run outputs.
    run_dir = paths.latest_dir()
    queue = run_dir / "draft_queue.jsonl"
    for name in ("draft_queue.jsonl", "founder_review.md", "top_50_priority.md", "safety_audit.json", "daily_metrics.json"):
        checks.append(Check(f"output::{name}", (run_dir / name).exists(), detail=paths.rel(run_dir / name)))

    # 5) Draft guard-flag counts.
    drafts: list[dict] = []
    if queue.exists():
        for line in queue.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                drafts.append(json.loads(line))
    n = len(drafts)
    checks.append(Check("draft_count_ge_400", n >= TARGET, detail=f"count={n}"))
    checks.append(Check("send_allowed_true_count_zero",
                        sum(1 for d in drafts if d.get("send_allowed") is True) == 0))
    checks.append(Check("external_send_blocked_false_count_zero",
                        sum(1 for d in drafts if d.get("external_send_blocked") is not True) == 0))
    checks.append(Check("no_auto_send_false_count_zero",
                        sum(1 for d in drafts if d.get("no_auto_send") is not True) == 0))

    # 6) Safety audit pass.
    safety_path = run_dir / "safety_audit.json"
    safety_pass = False
    if safety_path.exists():
        try:
            safety_pass = bool(json.loads(safety_path.read_text(encoding="utf-8")).get("pass"))
        except json.JSONDecodeError:
            safety_pass = False
    checks.append(Check("safety_audit_pass", safety_pass))

    # 7) README markers.
    readme = (paths.REPO_ROOT / "README.md").read_text(encoding="utf-8", errors="ignore")
    checks.append(Check("readme_has_commercial_launch_os", "Commercial Launch OS" in readme))
    checks.append(Check("readme_clone_url_dealix_sa",
                        "Dealix-sa/dealix.git" in readme or "dealix-sa/dealix.git" in readme.lower()))

    # 8) Workflow safety: permissions read-only/minimal, no send-secrets.
    wf_text_all = ""
    for wf in REQUIRED_WORKFLOWS:
        p = _exists(wf)
        if p.exists():
            wf_text_all += "\n" + p.read_text(encoding="utf-8", errors="ignore")
    # No write-all permissions in our workflows.
    no_write_all = "write-all" not in wf_text_all and "permissions: write-all" not in wf_text_all
    checks.append(Check("workflows_no_write_all", no_write_all))
    # Our launch workflows declare contents: read.
    final_wf = _exists(".github/workflows/final-launch-control.yml")
    final_txt = final_wf.read_text(encoding="utf-8", errors="ignore") if final_wf.exists() else ""
    checks.append(Check("final_workflow_contents_read", "contents: read" in final_txt))
    # No send-oriented secrets usage in our workflows.
    send_secret = re.search(r"secrets\.[A-Z_]*(SMTP|MAIL|TWILIO|WHATSAPP|LINKEDIN)[A-Z_]*", wf_text_all)
    checks.append(Check("workflows_no_send_secrets", send_secret is None,
                        detail=send_secret.group(0) if send_secret else ""))

    # 9) No external-send patterns in new commercial-launch code.
    code_offenders: list[str] = []
    seen: set[Path] = set()
    for g in COMMERCIAL_CODE_GLOBS:
        for p in paths.REPO_ROOT.glob(g):
            if p in seen or not p.is_file() or p.name in SCAN_EXCLUDE:
                continue
            seen.add(p)
            if find_external_send(p.read_text(encoding="utf-8", errors="ignore")):
                code_offenders.append(paths.rel(p))
    checks.append(Check("no_external_send_in_commercial_code", len(code_offenders) == 0,
                        detail=f"offenders={code_offenders[:5]}"))

    # 10) Site pages if apps/web exists.
    web = paths.REPO_ROOT / "apps" / "web" / "app"
    if web.exists():
        checks.append(Check("site_homepage_present", (web / "page.tsx").exists(), critical=False))

    return summarize(checks)


def _render_md(result: dict) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    verdict = "PASS ✅" if result["pass"] else "FAIL ❌"
    lines = [
        "# Final Launch Control — Master Verification",
        "",
        f"- Generated: {ts}",
        f"- Verdict: **{verdict}**",
        f"- Checks: {result['passed']}/{result['total']} passed "
        f"({result['critical_failed']} critical failed, {result['warnings']} warnings)",
        "",
        "| Status | Critical | Check | Detail |",
        "|---|---|---|---|",
    ]
    for c in result["checks"]:
        status = "✅" if c["passed"] else ("⚠️" if not c["critical"] else "❌")
        lines.append(f"| {status} | {'yes' if c['critical'] else 'no'} | `{c['name']}` | {c['detail']} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    paths.ensure_dirs()
    result = run()
    out_json = paths.FINAL_CONTROL_OUT / "final_verification.json"
    out_md = paths.FINAL_CONTROL_OUT / "final_verification.md"
    out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(_render_md(result), encoding="utf-8")

    print_checks("verify", [Check(**c) for c in result["checks"]])
    print(f"[verify] {result['passed']}/{result['total']} passed, "
          f"{result['critical_failed']} critical failed, {result['warnings']} warnings")
    print(f"[verify] wrote {paths.rel(out_json)} and {paths.rel(out_md)}")
    print("[verify] PASS" if result["pass"] else "[verify] FAIL")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
