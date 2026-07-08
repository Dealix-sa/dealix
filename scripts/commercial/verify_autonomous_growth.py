#!/usr/bin/env python3
"""Verify the Autonomous Growth & Strategy Execution OS is safe and complete.

Checks:
  - strategy folder exists and all 13 required strategies are present
  - a draft-only run produces action, approval, proof, and content queues
  - no live-send function is enabled; level 5 is blocked by default
  - no cold WhatsApp automation / guaranteed claims in generated content
  - no hardcoded secrets or public model endpoint configs in the engine

Exit 0 = PASS, 1 = FAIL.
"""

from __future__ import annotations

import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.strategy_execution import growth_engine, orchestrator, strategy_registry
from dealix.strategy_execution.safety_gate import (
    assert_no_live_send_enabled,
    clamp_autonomy,
)
from dealix.strategy_execution.schemas import AutonomyLevel, MAX_ENABLED_AUTONOMY_LEVEL

ENGINE_DIR = ROOT / "dealix" / "strategy_execution"

FORBIDDEN_CLAIMS = (
    "guaranteed revenue",
    "guaranteed clients",
    "guaranteed government access",
    "cold whatsapp blast",
    "auto send whatsapp",
    "fake proof",
)

# Patterns that would indicate a public model endpoint or committed provider key.
UNSAFE_PATTERNS = (
    re.compile(r"https?://[^\s\"']*:11434"),  # exposed ollama port
    re.compile(r"sk-[A-Za-z0-9]{20,}"),  # provider key shape
)


def verify() -> list[str]:
    failures: list[str] = []

    # 1. Strategy folder + required files.
    missing = strategy_registry.missing_required()
    if missing:
        failures.append(f"Missing required strategies: {', '.join(missing)}")
    strategies = strategy_registry.load_strategies()
    if len(strategies) < len(strategy_registry.REQUIRED_STRATEGIES):
        failures.append("Fewer strategies loaded than required.")

    # 2. Level 5 is blocked by default.
    if int(MAX_ENABLED_AUTONOMY_LEVEL) >= int(AutonomyLevel.EXTERNAL_EXECUTION):
        failures.append("External execution (level 5) is not blocked.")
    if clamp_autonomy(5) >= int(AutonomyLevel.EXTERNAL_EXECUTION):
        failures.append("clamp_autonomy allows level 5.")

    # 3. Draft-only run produces all queues.
    result = orchestrator.run_day(
        autonomy_level=3, limit=50, mode="draft-only", run_date=date.today(), write=True
    )
    if not result.outputs.get("actions"):
        failures.append("Action queue not generated.")
    if not result.outputs.get("approvals"):
        failures.append("Approval queue not generated.")
    if not result.outputs.get("proof"):
        failures.append("Proof log not generated.")
    if not result.outputs.get("content"):
        failures.append("Content queue not generated.")
    if result.blocked_count and not result.approvals:
        failures.append("Blocked actions were not surfaced for approval.")

    # 4. mode must be draft-only.
    try:
        orchestrator.run_day(mode="live", write=False)
        failures.append("Engine accepted a non-draft-only mode.")
    except ValueError:
        pass

    # 5. No live-send flags enabled.
    failures.extend(assert_no_live_send_enabled(dict(os.environ)))

    # 6. Generated content has no forbidden claims.
    content = growth_engine.build_content_queue(date.today())
    low = content.lower()
    for claim in FORBIDDEN_CLAIMS:
        if claim in low:
            failures.append(f"Forbidden claim in content: {claim}")

    # 7. No unsafe endpoint/secret patterns in engine source.
    for path in ENGINE_DIR.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for pattern in UNSAFE_PATTERNS:
            if pattern.search(text):
                failures.append(f"Unsafe pattern in {path.name}: {pattern.pattern}")

    return failures


def main() -> int:
    failures = verify()
    if failures:
        print("AUTONOMOUS_GROWTH_VERIFY=FAIL")
        for f in failures:
            print(f"FAIL: {f}")
        return 1
    print("AUTONOMOUS_GROWTH_VERIFY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
