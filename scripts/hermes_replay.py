"""Hermes Replay — re-dispatch a past run by ``run_id`` for debugging.

Reads the original intent + customer + channel from ``var/hermes-runs.jsonl``
and feeds them back through the orchestrator. The replayed run gets a new
``run_id`` (so the audit trail stays append-only).

Usage:
    python scripts/hermes_replay.py hermes_1779977174796_98ef7ddf
    python scripts/hermes_replay.py --json hermes_…
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.hermes import HermesOrchestrator, HermesTask  # noqa: E402
from dealix.hermes.agents import route_to_agent_executor  # noqa: E402
from dealix.hermes.audit import _path as _audit_path  # noqa: E402


def _find_run(run_id: str) -> dict | None:
    path = _audit_path()
    if not path.is_file():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("run_id") == run_id:
            return row
    return None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="hermes_replay")
    p.add_argument("run_id", help="Original run_id to replay.")
    p.add_argument("--json", action="store_true", help="Emit JSON.")
    args = p.parse_args(argv)

    row = _find_run(args.run_id)
    if not row:
        print(f"run_id not found in audit ledger: {args.run_id}", file=sys.stderr)
        return 2

    orch = HermesOrchestrator(executor=route_to_agent_executor)
    result = orch.dispatch(
        HermesTask(
            intent=row.get("intent_summary", ""),
            customer_id=row.get("customer_id", "dealix_internal"),
        )
    )
    payload = {
        "original_run_id": args.run_id,
        "replayed": result.to_dict(),
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"original:  {args.run_id}")
        print(f"replayed:  {result.run_id}")
        print(f"decision:  {result.decision.decision}")
        if result.route:
            print(f"routed:    {result.route.sub_agent}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
