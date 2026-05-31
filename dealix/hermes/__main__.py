"""Hermes CLI — `python -m dealix.hermes "<intent>"`.

A founder-friendly command-line entry point that dispatches an intent
through the full Hermes pipeline (gate → router → executor → audit) and
prints the result as either human-readable text or JSON.

Examples:

    # Get a routed envelope for the engineer sub-agent.
    python -m dealix.hermes "refactor the FastAPI router for /leads"

    # JSON mode (pipeable into jq, n8n, Decision Bot, …).
    python -m dealix.hermes --json "produce today's founder brief"

    # Doctrine-blocked request — exits non-zero with a clear refusal.
    python -m dealix.hermes "send cold whatsapp blast to warm list"

    # Customer-scoped dispatch (writes to friction_log on refusal).
    python -m dealix.hermes --customer cust_001 "run sprint day 3 for ACME"

Exit codes:
  0 — approved + executor returned ok
  1 — approved but executor reported failure
  2 — needs_approval (queued in approval_center placeholder)
  3 — rejected by governance gate
  4 — kill switch active
  5 — usage error
"""

from __future__ import annotations

import argparse
import json
import sys

from . import HermesOrchestrator, HermesTask
from .agents import route_to_agent_executor
from .governance_gate import Decision


_EXIT_MAP: dict[str, int] = {
    Decision.NEEDS_APPROVAL.value: 2,
    Decision.REJECTED.value: 3,
    Decision.KILL_SWITCHED.value: 4,
}


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m dealix.hermes",
        description="Dispatch an intent through the Hermes orchestrator.",
    )
    p.add_argument("intent", help="The user intent to dispatch.")
    p.add_argument(
        "--customer",
        default="dealix_internal",
        help="Customer id for friction_log scoping (default: dealix_internal).",
    )
    p.add_argument(
        "--channel",
        default="",
        help="External channel hint (email | whatsapp | linkedin_dm | sms | portal).",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="Emit the full result as JSON instead of human-readable text.",
    )
    return p


def _render_text(result_dict: dict) -> str:
    lines: list[str] = []
    gd = result_dict["governance_decision"]
    route = result_dict.get("route") or {}
    output = result_dict.get("output") or {}
    lines.append(f"run_id:    {result_dict['run_id']}")
    lines.append(f"decision:  {gd['decision']}")
    lines.append(f"reason:    {gd['reason']}")
    if gd.get("matched_rules"):
        lines.append(f"matched:   {', '.join(gd['matched_rules'])}")
    if gd.get("safe_alternative"):
        lines.append(f"safe_alt:  {gd['safe_alternative']}")
    if route:
        lines.append(
            f"routed:    {route['sub_agent']} | gear={route['gear']} "
            f"| provider={route['provider']} | model={route['model_id']}"
        )
    if output.get("kind"):
        lines.append(f"output:    kind={output['kind']} ok={output.get('ok')}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    orch = HermesOrchestrator(executor=route_to_agent_executor)
    task = HermesTask(
        intent=args.intent,
        customer_id=args.customer,
        channel=args.channel,
    )
    result = orch.dispatch(task)
    payload = result.to_dict()

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(_render_text(payload))

    decision = result.decision.decision
    if decision in _EXIT_MAP:
        return _EXIT_MAP[decision]
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
