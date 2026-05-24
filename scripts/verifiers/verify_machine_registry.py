#!/usr/bin/env python3
"""Verify Machine Registry: every machine has owner, schedule, entrypoint,
kpi, kill_switch, failure_mode."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO_ROOT, report  # noqa: E402

LAYER = "Machine Registry"
REQUIRED = ("id", "name", "owner", "purpose", "schedule", "entrypoint",
            "kpi", "kill_switch", "audit_required", "failure_mode")
MIN_MACHINES = 3


def main() -> None:
    reasons: list[str] = []
    path = REPO_ROOT / "registries" / "machine_registry.yaml"
    if not path.exists():
        report(LAYER, False, ["missing: registries/machine_registry.yaml"])

    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
    except ImportError:
        for f in REQUIRED:
            if f"{f}:" not in text:
                reasons.append(f"missing field token: {f}")
        report(LAYER, not reasons, reasons)

    machines = (data or {}).get("machines") or []
    if len(machines) < MIN_MACHINES:
        reasons.append(f"machines count {len(machines)} < {MIN_MACHINES}")
    for m in machines:
        for f in REQUIRED:
            if f not in m:
                reasons.append(f"machine {m.get('id', '?')!r} missing: {f}")

    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
