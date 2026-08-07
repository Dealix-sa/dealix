#!/usr/bin/env python3
"""Dealix commercial readiness gate.

This script is dependency-free and safe to run in CI/local environments. It does
not send anything externally and fails when unsafe outbound flags are enabled.
"""
from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAFE_FALSE_FLAGS = [
    "EXTERNAL_SEND_ENABLED",
    "EMAIL_SEND_ENABLED",
    "WHATSAPP_SEND_ENABLED",
    "WHATSAPP_ALLOW_LIVE_SEND",
    "SMS_SEND_ENABLED",
]
REQUIRED_FILES = [
    "Makefile",
    ".env.example",
    "docs/ops/COMMERCIAL_READINESS_CONTROL_CENTER_AR.md",
    "business/products/COMMERCIAL_PRODUCT_CATALOG.md",
    "sales/COMMERCIAL_FOUNDATION_PACK_AR.md",
]
RECOMMENDED_FILES = [
    "scripts/verify_no_auto_external_send.py",
    "scripts/verify_company_launch_ready.py",
    "scripts/run_company_launch_day.sh",
    "scripts/command_room/build_command_room.py",
]


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def read_env_example() -> dict[str, str]:
    env_path = ROOT / ".env.example"
    values: dict[str, str] = {}
    if not env_path.exists():
        return values
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.split("#", 1)[0].strip()
    return values


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []
    env_example = read_env_example()

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            failures.append(f"Missing required commercial file: {rel}")

    for rel in RECOMMENDED_FILES:
        if not (ROOT / rel).exists():
            warnings.append(f"Recommended launch file not found yet: {rel}")

    for key in SAFE_FALSE_FLAGS:
        runtime_value = os.getenv(key)
        example_value = env_example.get(key)
        if truthy(runtime_value):
            failures.append(f"Unsafe runtime flag enabled: {key}=true")
        if example_value is None:
            warnings.append(f".env.example missing safety flag: {key}")
        elif truthy(example_value):
            failures.append(f".env.example must not enable {key}")

    mode = os.getenv("OUTBOUND_MODE", env_example.get("OUTBOUND_MODE", "draft_only"))
    if mode != "draft_only":
        failures.append(f"OUTBOUND_MODE must be draft_only for this baseline, got {mode!r}")

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "status": "blocked" if failures else "ready_for_manual_commercial_execution",
        "failures": failures,
        "warnings": warnings,
        "safe_outbound_defaults": {key: env_example.get(key, "") for key in SAFE_FALSE_FLAGS},
        "outbound_mode": mode,
        "next_actions": [
            "Run make commercial-pack",
            "Review reports/commercial/latest.md",
            "Review drafts manually before any outreach",
            "Do not enable live outbound in this PR",
        ],
    }

    out_dir = ROOT / "reports" / "commercial"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "readiness.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if failures:
        print("COMMERCIAL_READINESS=BLOCKED")
        for item in failures:
            print(f"FAIL: {item}")
        for item in warnings:
            print(f"WARN: {item}")
        return 1

    print("COMMERCIAL_READINESS=READY_FOR_MANUAL_COMMERCIAL_EXECUTION")
    for item in warnings:
        print(f"WARN: {item}")
    print("Report: reports/commercial/readiness.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
