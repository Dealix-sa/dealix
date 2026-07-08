#!/usr/bin/env python3
"""One-shot foundation check: Railway config sanity + Money Now + Autonomous Growth.

Runs the sub-verifiers and a few lightweight existence checks. Optional
sub-verifiers that are absent are reported but do not fail the run.

Exit 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COMMERCIAL = ROOT / "scripts" / "commercial"


def _run(script: Path) -> tuple[str, bool]:
    if not script.exists():
        return (f"SKIP (missing): {script.name}", True)
    proc = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    tail = (proc.stdout.strip().splitlines() or ["(no output)"])[-1]
    ok = proc.returncode == 0
    return (f"{'PASS' if ok else 'FAIL'}: {script.name} -> {tail}", ok)


def _railway_config_ok() -> tuple[str, bool]:
    """Lightweight railway.toml sanity: Docker builder + /healthz present."""

    toml_path = ROOT / "railway.toml"
    if not toml_path.exists():
        return ("FAIL: railway.toml missing", False)
    text = toml_path.read_text(encoding="utf-8")
    checks = {
        'builder = "DOCKERFILE"': "DOCKERFILE" in text,
        "healthcheckPath /healthz": "/healthz" in text,
        "healthcheckTimeout 300": "300" in text,
    }
    missing = [k for k, ok in checks.items() if not ok]
    if missing:
        return (f"FAIL: railway.toml missing {missing}", False)
    return ("PASS: railway.toml (DOCKERFILE + /healthz + timeout)", True)


def _docs_exist() -> tuple[str, bool]:
    required = [
        ROOT / "docs" / "commercial" / "MONEY_NOW_SPRINT.md",
        ROOT / "docs" / "commercial" / "AUTONOMOUS_GROWTH_EXECUTION_OS.md",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        return (f"FAIL: missing docs {missing}", False)
    return ("PASS: foundation docs present", True)


def main() -> int:
    results: list[tuple[str, bool]] = []
    results.append(_railway_config_ok())

    # Optional external verifier if present in the repo.
    railway_verify = ROOT / "scripts" / "verify_railway_production_config.py"
    if railway_verify.exists():
        results.append(_run(railway_verify))

    results.append(_run(COMMERCIAL / "verify_money_now_sprint.py"))
    results.append(_run(COMMERCIAL / "verify_autonomous_growth.py"))
    results.append(_docs_exist())

    all_ok = True
    for line, ok in results:
        print(line)
        all_ok = all_ok and ok

    print("LAUNCH_FOUNDATION_VERIFY=" + ("PASS" if all_ok else "FAIL"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
