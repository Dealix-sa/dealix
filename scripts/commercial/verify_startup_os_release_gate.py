#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from scripts.commercial.run_startup_os_day import main as run_startup_os_day

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "startup_release_gate"

REQUIRED_PATHS = [
    "data/commercial/lead_pipeline.csv",
    "data/commercial/startup_os_product_matrix.json",
    "data/commercial/startup_os_operating_config.json",
    "scripts/commercial/run_startup_os_day.py",
    "scripts/commercial/generate_startup_command_center.py",
    "scripts/commercial/generate_founder_daily_brief.py",
    "scripts/commercial/generate_startup_proof_pack.py",
    "apps/web/lib/commercial-command-snapshot.ts",
    "apps/web/lib/startup-command-snapshot.ts",
    "apps/web/lib/founder-daily-brief-snapshot.ts",
    "apps/web/app/(saas)/app/command-room/page.tsx",
    "apps/web/app/(saas)/app/startup-command/page.tsx",
    "apps/web/app/(saas)/app/founder-brief/page.tsx",
    "docs/ops/STARTUP_OS_DAY_RUNBOOK.md",
]

GENERATED_PATHS = [
    "reports/commercial/sales_agent_company_brain/latest.json",
    "reports/commercial/review_actions/latest.json",
    "reports/startup_command_center/latest.json",
    "reports/founder_daily_brief/latest.json",
    "reports/startup_proof_pack/latest.json",
]

SAFE_STRINGS = [
    "no live outbound by default",
    "no fake ROI",
    "source_url required",
    "draft_only",
    "WHATSAPP_ALLOW_LIVE_SEND",
]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def check_json(path: str, failures: list[str]) -> dict:
    try:
        return json.loads(read_text(path))
    except Exception as exc:  # pragma: no cover - diagnostic message only
        failures.append(f"invalid json: {path}: {exc}")
        return {}


def markdown(payload: dict) -> str:
    lines = [
        "# Startup OS Release Gate",
        "",
        f"Generated at: {payload['generated_at']}",
        "",
        f"Verdict: `{payload['verdict']}`",
        "",
        "## Required paths",
        "",
    ]
    for item in payload["required_paths"]:
        lines.append(f"- {item['status']}: `{item['path']}`")
    lines += ["", "## Generated paths", ""]
    for item in payload["generated_paths"]:
        lines.append(f"- {item['status']}: `{item['path']}`")
    lines += ["", "## Safety checks", ""]
    for item in payload["safety_checks"]:
        lines.append(f"- {item['status']}: {item['check']}")
    if payload["failures"]:
        lines += ["", "## Failures", ""]
        for failure in payload["failures"]:
            lines.append(f"- {failure}")
    return "\n".join(lines) + "\n"


def main() -> int:
    failures: list[str] = []
    run_startup_os_day()

    required = []
    for rel in REQUIRED_PATHS:
        exists = (ROOT / rel).exists()
        required.append({"path": rel, "status": "PASS" if exists else "FAIL"})
        if not exists:
            failures.append(f"missing required path: {rel}")

    generated = []
    for rel in GENERATED_PATHS:
        exists = (ROOT / rel).exists()
        generated.append({"path": rel, "status": "PASS" if exists else "FAIL"})
        if not exists:
            failures.append(f"missing generated path: {rel}")
        else:
            check_json(rel, failures)

    combined = "\n".join(
        read_text(path)
        for path in [
            "data/commercial/startup_os_product_matrix.json",
            "data/commercial/startup_os_operating_config.json",
            "docs/ops/STARTUP_OS_DAY_RUNBOOK.md",
        ]
        if (ROOT / path).exists()
    )
    safety = []
    for phrase in SAFE_STRINGS:
        ok = phrase in combined
        safety.append({"check": phrase, "status": "PASS" if ok else "FAIL"})
        if not ok:
            failures.append(f"missing safety phrase: {phrase}")

    startup = check_json("reports/startup_command_center/latest.json", failures)
    if not startup.get("products"):
        failures.append("startup command center has no products")
    if startup.get("mode") not in {"founder_led_review_first", "draft_only"}:
        failures.append(f"unexpected startup mode: {startup.get('mode')}")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "verdict": "PASS" if not failures else "FAIL",
        "required_paths": required,
        "generated_paths": generated,
        "safety_checks": safety,
        "failures": failures,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "latest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "latest.md").write_text(markdown(payload), encoding="utf-8")
    print(f"STARTUP_OS_RELEASE_GATE={payload['verdict']}")
    print("STARTUP_OS_RELEASE_GATE_REPORT=reports/startup_release_gate/latest.md")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
