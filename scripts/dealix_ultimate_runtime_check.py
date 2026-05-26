from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports" / "readiness"


def run(name: str, cmd: list[str], timeout: int = 120) -> dict:
    try:
        p = subprocess.run(
            cmd,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            timeout=timeout,
        )
        return {
            "name": name,
            "cmd": " ".join(cmd),
            "ok": p.returncode == 0,
            "code": p.returncode,
            "stdout": p.stdout[-1600:],
            "stderr": p.stderr[-1600:],
        }
    except Exception as e:
        return {
            "name": name,
            "cmd": " ".join(cmd),
            "ok": False,
            "code": -1,
            "stdout": "",
            "stderr": f"{type(e).__name__}: {e}",
        }


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)

    tests = []

    tests.append(run("dealix_status", [sys.executable, "dealix.py", "status"], 60))

    if (ROOT / "scripts" / "verify_local_ai.py").exists():
        tests.append(run("verify_local_ai", [sys.executable, "scripts/verify_local_ai.py"], 180))

    if (ROOT / "scripts" / "ledger_guard.py").exists():
        tests.append(run("ledger_guard", [sys.executable, "scripts/ledger_guard.py"], 60))

    if (ROOT / "scripts" / "build_manual_send_queue.py").exists():
        tests.append(run("manual_send_queue", [sys.executable, "scripts/build_manual_send_queue.py"], 60))

    if (ROOT / "scripts" / "build_followup_queue.py").exists():
        tests.append(run("followup_queue", [sys.executable, "scripts/build_followup_queue.py"], 60))

    if (ROOT / "scripts" / "lead_status_report.py").exists():
        tests.append(run("lead_status_report", [sys.executable, "scripts/lead_status_report.py"], 60))

    if (ROOT / "scripts" / "revenue_ledger.py").exists():
        tests.append(run("revenue_report", [sys.executable, "scripts/revenue_ledger.py", "report"], 60))

    if (ROOT / "scripts" / "delivery_tracker.py").exists():
        tests.append(run("delivery_report", [sys.executable, "scripts/delivery_tracker.py", "report"], 60))

    if (ROOT / "scripts" / "hermes_safe_init.py").exists():
        tests.append(run("hermes_safe_init", [sys.executable, "scripts/hermes_safe_init.py"], 60))

    if (ROOT / "scripts" / "hermes_opportunity_radar.py").exists():
        tests.append(run("hermes_opportunity_radar", [sys.executable, "scripts/hermes_opportunity_radar.py"], 60))

    if (ROOT / "scripts" / "hermes_founder_brief.py").exists():
        tests.append(run("hermes_founder_brief", [sys.executable, "scripts/hermes_founder_brief.py"], 60))

    if (ROOT / "scripts" / "hermes_trust_pack.py").exists():
        tests.append(run("hermes_trust_pack", [sys.executable, "scripts/hermes_trust_pack.py"], 60))

    if (ROOT / "scripts" / "hermes_partner_init.py").exists():
        tests.append(run("hermes_partner_init", [sys.executable, "scripts/hermes_partner_init.py"], 60))

    if (ROOT / "scripts" / "hermes_partner_os.py").exists():
        tests.append(run("hermes_partner_report", [sys.executable, "scripts/hermes_partner_os.py", "report"], 60))

    passed = sum(1 for t in tests if t["ok"])
    failed = len(tests) - passed
    verdict = "PASS" if failed == 0 else "REVIEW_REQUIRED"

    lines = [
        "# Dealix/Hermes Ultimate Runtime Check",
        "",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        f"- Verdict: {verdict}",
        "",
        "| Test | OK | Code | Command |",
        "|---|---|---:|---|",
    ]

    for t in tests:
        lines.append(f"| {t['name']} | {t['ok']} | {t['code']} | `{t['cmd']}` |")

    lines += ["", "## Details", ""]

    for t in tests:
        lines += [
            f"### {t['name']}",
            "",
            f"- OK: {t['ok']}",
            f"- Code: {t['code']}",
            "",
            "STDOUT:",
            "```text",
            t["stdout"],
            "```",
            "",
            "STDERR:",
            "```text",
            t["stderr"],
            "```",
            "",
        ]

    out = REPORTS / f"ultimate-runtime-check-{time.strftime('%Y%m%d-%H%M%S')}.md"
    out.write_text("\n".join(lines), encoding="utf-8")

    print(f"ULTIMATE_RUNTIME_CHECK_REPORT={out}")
    print(f"ULTIMATE_RUNTIME_CHECK_VERDICT={verdict}")

    if verdict != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
