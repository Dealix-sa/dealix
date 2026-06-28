#!/usr/bin/env python3
"""Backend launch cleanliness checks for Dealix.

Dependency-free checks for launch-critical files, safe defaults, and repository
shape. This script does not call external services.
"""
from __future__ import annotations

import json
from datetime import UTC, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_PATHS = [
    "api/main.py",
    "db/session.py",
    "db/models.py",
    ".env.example",
    "scripts/commercial/commercial_readiness_check.py",
    "scripts/commercial/generate_commercial_go_live_pack.py",
]
SAFE_DEFAULTS = {
    "EXTERNAL_SEND_ENABLED": "false",
    "EMAIL_SEND_ENABLED": "false",
    "WHATSAPP_SEND_ENABLED": "false",
    "WHATSAPP_ALLOW_LIVE_SEND": "false",
    "SMS_SEND_ENABLED": "false",
    "OUTBOUND_MODE": "draft_only",
}


def parse_env_example() -> dict[str, str]:
    values: dict[str, str] = {}
    path = ROOT / ".env.example"
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.split("#", 1)[0].strip()
    return values


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).exists():
            failures.append(f"Missing launch-critical backend path: {rel}")

    env_values = parse_env_example()
    for key, expected in SAFE_DEFAULTS.items():
        actual = env_values.get(key)
        if actual is None:
            failures.append(f".env.example missing {key}")
        elif actual.lower() != expected:
            failures.append(f".env.example {key} must be {expected}, got {actual}")

    db_models = ROOT / "db" / "models.py"
    if db_models.exists():
        models_text = db_models.read_text(encoding="utf-8", errors="ignore")
        if "class " not in models_text:
            warnings.append("db/models.py does not appear to define model classes")

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "blocked" if failures else "ready_for_launch_review",
        "failures": failures,
        "warnings": warnings,
        "safe_defaults": SAFE_DEFAULTS,
    }
    out_dir = ROOT / "reports" / "go_live"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "backend_launch_cleanliness.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if failures:
        print("BACKEND_LAUNCH_CLEANLINESS=BLOCKED")
        for item in failures:
            print(f"FAIL: {item}")
        for item in warnings:
            print(f"WARN: {item}")
        return 1

    print("BACKEND_LAUNCH_CLEANLINESS=READY_FOR_LAUNCH_REVIEW")
    for item in warnings:
        print(f"WARN: {item}")
    print("Report: reports/go_live/backend_launch_cleanliness.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
