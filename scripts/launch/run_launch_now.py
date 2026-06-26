#!/usr/bin/env python3
# ruff: noqa: S603, S607
from __future__ import annotations

import argparse
import json
import os
import subprocess
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "reports" / "launch"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

SAFE_ENV = {
    "APP_ENV": "test",
    "ENVIRONMENT": "test",
    "PYTHONIOENCODING": "utf-8",
    "EXTERNAL_SEND_ENABLED": "false",
    "EMAIL_SEND_ENABLED": "false",
    "WHATSAPP_SEND_ENABLED": "false",
    "WHATSAPP_ALLOW_LIVE_SEND": "false",
    "SMS_SEND_ENABLED": "false",
    "OUTBOUND_MODE": "draft_only",
}


@dataclass
class StepResult:
    name: str
    command: list[str]
    required: bool
    returncode: int
    status: str


def command_exists(path: str) -> bool:
    return (ROOT / path).exists()


def run_step(name: str, command: list[str], *, required: bool) -> StepResult:
    print(f"\n▶ {name}")
    env = os.environ.copy()
    env.update(SAFE_ENV)
    # Commands are static launch gates declared in this module; no user input is interpolated.
    result = subprocess.run(command, cwd=ROOT, env=env, check=False)
    status = "pass" if result.returncode == 0 else "fail"
    print(f"{name}: {status}")
    return StepResult(name, command, required, result.returncode, status)


def write_report(results: list[StepResult], *, include_frontend: bool, include_docker: bool) -> int:
    generated_at = datetime.now(UTC).isoformat()
    required_failed = [item for item in results if item.required and item.returncode != 0]
    optional_failed = [item for item in results if not item.required and item.returncode != 0]
    verdict = "GO_INTERNAL_MANUAL" if not required_failed else "BLOCKED"

    payload = {
        "generated_at": generated_at,
        "system": "Dealix Launch Command Center",
        "verdict": verdict,
        "include_frontend": include_frontend,
        "include_docker": include_docker,
        "safe_env": SAFE_ENV,
        "required_failed": [asdict(item) for item in required_failed],
        "optional_failed": [asdict(item) for item in optional_failed],
        "results": [asdict(item) for item in results],
    }
    (REPORT_DIR / "latest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    lines = [
        "# Dealix Launch Command Center",
        "",
        f"Generated at: {generated_at}",
        f"Verdict: `{verdict}`",
        "",
        "## Safety posture",
        "- Action flags are disabled by environment defaults.",
        "- Outbound mode is `draft_only`.",
        "- Data Intelligence outputs remain founder-reviewed.",
        "",
        "## Results",
        "",
        "| Step | Required | Status | Return code |",
        "|---|---:|---|---:|",
    ]
    for item in results:
        lines.append(
            f"| {item.name} | {str(item.required).lower()} | {item.status} | {item.returncode} |"
        )
    if required_failed:
        lines.extend(["", "## Required blockers"])
        for item in required_failed:
            lines.append(f"- {item.name}: `{' '.join(item.command)}`")
    if optional_failed:
        lines.extend(["", "## Optional blockers"])
        for item in optional_failed:
            lines.append(f"- {item.name}: `{' '.join(item.command)}`")
    lines.extend(
        [
            "",
            "## Next action",
            "- If verdict is `GO_INTERNAL_MANUAL`, run the company day and review outputs manually.",
            "- If verdict is `BLOCKED`, fix required blockers before public launch.",
        ]
    )
    (REPORT_DIR / "latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nLAUNCH_COMMAND_CENTER_VERDICT={verdict}")
    print(f"Report: {REPORT_DIR / 'latest.md'}")
    return 0 if verdict == "GO_INTERNAL_MANUAL" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Dealix launch command center checks")
    parser.add_argument("--include-frontend", action="store_true")
    parser.add_argument("--include-docker", action="store_true")
    args = parser.parse_args()

    steps: list[tuple[str, list[str], bool]] = [
        (
            "Compile Python surfaces",
            ["python", "-m", "compileall", "-q", "api", "dealix", "scripts", "tests", "app"],
            True,
        ),
        (
            "Exa/Data Intelligence tests",
            [
                "python",
                "-m",
                "pytest",
                "-q",
                "tests/test_exa_data_intelligence_os.py",
                "tests/test_data_intelligence_no_live_outbound.py",
            ],
            True,
        ),
        (
            "Data Intelligence Day",
            ["python", "scripts/intelligence/run_data_intelligence_day.py"],
            True,
        ),
        ("Environment contract", ["python", "scripts/check_env_contract.py"], True),
        ("Company safety check", ["make", "company-check"], True),
        ("Revenue daily machine", ["make", "revenue-daily"], False),
        ("Command room build", ["make", "command-room"], False),
    ]

    if command_exists("scripts/verify_railway_surfaces.py"):
        steps.append(("Railway surface check", ["python", "scripts/verify_railway_surfaces.py"], True))
    if command_exists("scripts/verify_founder_operating_system.py"):
        steps.append(("Founder OS check", ["python", "scripts/verify_founder_operating_system.py"], False))

    if args.include_frontend:
        steps.extend(
            [
                ("Install web dependencies", ["npm", "--prefix", "apps/web", "ci"], True),
                ("Web typecheck", ["npm", "--prefix", "apps/web", "run", "typecheck"], True),
                ("Web build", ["npm", "--prefix", "apps/web", "run", "build"], True),
            ]
        )

    if args.include_docker:
        steps.extend(
            [
                ("API Docker build", ["docker", "build", "-t", "dealix-api-ci", "."], True),
                ("Web Docker build", ["docker", "build", "-t", "dealix-apps-web-ci", "apps/web"], True),
            ]
        )

    results = [run_step(name, command, required=required) for name, command, required in steps]
    return write_report(results, include_frontend=args.include_frontend, include_docker=args.include_docker)


if __name__ == "__main__":
    raise SystemExit(main())
