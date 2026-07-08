#!/usr/bin/env python3
"""Verify the Dealix autonomous growth execution layer.

The verifier is repo-local and deterministic. It proves the daily loop can create
internal artifacts while keeping external actions disabled.
"""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path
from typing import Any

from dealix.strategy_execution.orchestrator import run_daily_strategy_execution
from dealix.strategy_execution.safety_gate import evaluate_action_safety
from dealix.strategy_execution.strategy_registry import load_strategy_registry

REQUIRED_OUTPUT_DIRS = ("actions", "approvals", "proof", "learning", "content", "daily")
BLOCKED_ACTION_PROBES = (
    "cold WhatsApp blast",
    "mass LinkedIn automation",
    "guaranteed revenue campaign",
    "public vLLM endpoint without auth",
)
APPROVAL_ACTION_PROBES = (
    "send email to prospect",
    "publish post to LinkedIn",
    "merge PR",
    "production deploy",
)


def _load_json_files(path: Path) -> list[Any]:
    return [json.loads(item.read_text(encoding="utf-8")) for item in sorted(path.glob("*.json"))]


def verify(output_root: Path | None = None) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = output_root or Path(tmp_dir) / "autonomous_growth"
        result = run_daily_strategy_execution(output_root=root, autonomy_level=3, limit=50)

        missing_dirs = [name for name in REQUIRED_OUTPUT_DIRS if not (root / name).is_dir()]
        strategies = load_strategy_registry()
        action_payloads = _load_json_files(root / "actions")
        approval_payloads = _load_json_files(root / "approvals")
        proof_payloads = _load_json_files(root / "proof")
        content_payloads = _load_json_files(root / "content")
        daily_reports = list((root / "daily").glob("*.md"))

        blocked_checks = [evaluate_action_safety(action) for action in BLOCKED_ACTION_PROBES]
        approval_checks = [evaluate_action_safety(action) for action in APPROVAL_ACTION_PROBES]

        problems: list[str] = []
        if missing_dirs:
            problems.append(f"missing output dirs: {', '.join(missing_dirs)}")
        if not strategies:
            problems.append("strategy registry is empty")
        if not action_payloads:
            problems.append("no action queue generated")
        if not proof_payloads:
            problems.append("no proof log generated")
        if not content_payloads:
            problems.append("no content queue generated")
        if not daily_reports:
            problems.append("no daily report generated")
        if any(decision.allowed for decision in blocked_checks):
            problems.append("blocked action probe was allowed")
        if any(not decision.approval_required for decision in approval_checks):
            problems.append("external approval probe did not require approval")

        for payload in proof_payloads:
            if payload.get("external_execution_enabled") is not False:
                problems.append("proof log does not explicitly disable external execution")
            safety = payload.get("safety_summary", {})
            if safety.get("draft_only") is not True:
                problems.append("proof log does not confirm draft-only mode")
            if safety.get("no_cold_whatsapp") is not True:
                problems.append("proof log does not confirm no cold WhatsApp")

        return {
            "ok": not problems,
            "problems": problems,
            "result": result,
            "strategies": len(strategies),
            "action_files": len(action_payloads),
            "approval_files": len(approval_payloads),
            "proof_files": len(proof_payloads),
            "content_files": len(content_payloads),
            "daily_reports": len(daily_reports),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Dealix autonomous growth loop")
    parser.add_argument("--output-root", default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root) if args.output_root else None
    report = verify(output_root=output_root)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    if report["ok"]:
        print("DEALIX_AUTONOMOUS_GROWTH_VERIFIED=1")
        return 0
    print("DEALIX_AUTONOMOUS_GROWTH_VERIFIED=0")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
