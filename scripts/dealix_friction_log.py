#!/usr/bin/env python3
"""Dealix Friction Log CLI — log and review friction events from a terminal.

Wraps the existing, already-tested friction log store and aggregator
(``auto_client_acquisition.friction_log.store`` and
``auto_client_acquisition.friction_log.aggregator``) so the founder can
record friction (manual overrides, governance blocks, approval delays,
support tickets, etc) without writing a Python one-liner or standing up
the FastAPI server. Pure local JSONL file I/O — NO LLM call, NO live
send, NO network calls. This script only ever appends to / reads a
local JSONL file and prints to stdout.

Usage:
    python scripts/dealix_friction_log.py log \\
        --kind manual_override \\
        --severity med \\
        --notes "Had to manually re-send the Sprint proof pack email after Gmail OAuth token expired" \\
        --cost-minutes 20 \\
        --customer-id dealix_internal \\
        --workflow-id founder_manual

    python scripts/dealix_friction_log.py report --customer-id dealix_internal --window-days 14

This is a local append-only log entry — no external action, no
notification is ever sent to anyone by this script.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.friction_log.aggregator import aggregate
from auto_client_acquisition.friction_log.schemas import FrictionKind, FrictionSeverity
from auto_client_acquisition.friction_log.store import emit, list_events

# Default identifier for founder/company-level friction not tied to one
# customer engagement — used consistently across the codebase, e.g.
# api/routers/agent_os.py, api/routers/founder_dashboard.py,
# api/routers/founder_launch_status.py.
DEFAULT_CUSTOMER_ID = "dealix_internal"

# CRITICAL: this default is what keeps manually-logged entries clearly
# distinguishable from automated ones (e.g. delivery_sprint.py tags every
# automated entry with workflow_id="delivery_sprint"). Never change this
# default to "" or to a value that could collide with an automated tag.
DEFAULT_WORKFLOW_ID = "founder_manual_cli"

_NOTES_TRUNCATE_LEN = 80


def _truncate(text: str, limit: int = _NOTES_TRUNCATE_LEN) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def _cmd_log(args: argparse.Namespace) -> int:
    event = emit(
        customer_id=args.customer_id,
        kind=args.kind,
        severity=args.severity,
        workflow_id=args.workflow_id,
        evidence_ref=args.evidence_ref,
        cost_minutes=args.cost_minutes,
        notes=args.notes,
    )

    lines = [
        "Friction event logged.",
        "",
        f"event_id: {event.event_id}",
        f"customer_id: {event.customer_id}",
        f"kind: {event.kind}",
        f"severity: {event.severity}",
        f"workflow_id: {event.workflow_id}",
        f"cost_minutes: {event.cost_minutes}",
        f"occurred_at: {event.occurred_at}",
        "",
        "This is a local append-only log entry — no external action, no "
        "notification sent to anyone.",
    ]
    print("\n".join(lines))
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    agg = aggregate(customer_id=args.customer_id, window_days=args.window_days)

    if args.json:
        print(json.dumps(agg.to_dict(), indent=2, ensure_ascii=False, default=str))
        return 0

    lines: list[str] = []
    lines.append(
        f"Friction report — customer_id: {args.customer_id}, "
        f"window_days: {args.window_days}"
    )
    lines.append("")

    if agg.total == 0:
        lines.append("No friction events found in this window.")
        print("\n".join(lines))
        return 0

    high_count = agg.by_severity.get("high", 0)
    if high_count > 0:
        lines.append(
            f"HIGH SEVERITY: Resolve {high_count} high-severity friction "
            "event(s) — review before proceeding."
        )
        lines.append("")

    lines.append(f"total: {agg.total}")
    lines.append(f"by_kind: {json.dumps(agg.by_kind, ensure_ascii=False)}")
    lines.append(f"by_severity: {json.dumps(agg.by_severity, ensure_ascii=False)}")
    lines.append(f"top_3_kinds: {agg.top_3_kinds}")
    lines.append(f"total_cost_minutes: {agg.total_cost_minutes}")
    lines.append(f"week_over_week_delta: {agg.week_over_week_delta}")

    if args.kind:
        events = list_events(
            customer_id=args.customer_id,
            since_days=args.window_days,
            kind=args.kind,
        )
        lines.append("")
        lines.append(f"Events matching kind={args.kind!r} ({len(events)}):")
        if not events:
            lines.append("  (none)")
        for ev in events:
            notes_display = _truncate(ev.notes) if ev.notes else ""
            lines.append(
                f"  - {ev.event_id} | {ev.occurred_at} | severity={ev.severity} "
                f"| workflow_id={ev.workflow_id} | cost_minutes={ev.cost_minutes} "
                f"| notes={notes_display!r}"
            )

    print("\n".join(lines))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Log and review Dealix friction events locally. Pure local "
            "JSONL file I/O — no external send of any kind."
        ),
    )
    sub = p.add_subparsers(dest="command", required=True)

    log_p = sub.add_parser("log", help="record a new friction event")
    log_p.add_argument(
        "--kind",
        required=True,
        choices=[k.value for k in FrictionKind],
        help="type of friction encountered",
    )
    log_p.add_argument(
        "--severity",
        default=FrictionSeverity.LOW.value,
        choices=[s.value for s in FrictionSeverity],
        help="severity of the friction event (default: %(default)s)",
    )
    log_p.add_argument(
        "--notes",
        default="",
        help=(
            "free text describing the friction (PII is automatically "
            "redacted and text capped at 500 chars by the store)"
        ),
    )
    log_p.add_argument(
        "--cost-minutes",
        type=int,
        default=0,
        help="minutes lost to this friction event (default: 0)",
    )
    log_p.add_argument(
        "--customer-id",
        default=DEFAULT_CUSTOMER_ID,
        help=(
            "tenant/engagement this friction belongs to. Use a real "
            "customer_id (e.g. an engagement_id from dealix_sprint_run.py) "
            "when logging friction tied to a specific paid engagement, or "
            f"{DEFAULT_CUSTOMER_ID!r} (default) for general founder/company-"
            "level friction not tied to one customer."
        ),
    )
    log_p.add_argument(
        "--workflow-id",
        default=DEFAULT_WORKFLOW_ID,
        help=(
            "workflow step this friction is tagged to. Defaults to "
            f"{DEFAULT_WORKFLOW_ID!r}, which signals this event was typed "
            "by a human at a terminal (not detected by automated code). "
            "Override with a specific engagement's workflow step, e.g. "
            "sprint_acme_001_kickoff_call, if desired."
        ),
    )
    log_p.add_argument(
        "--evidence-ref",
        default="",
        help="optional pointer to supporting evidence (file path, ticket ID, etc)",
    )
    log_p.set_defaults(func=_cmd_log)

    report_p = sub.add_parser("report", help="aggregate + list recent friction events")
    report_p.add_argument("--customer-id", default=DEFAULT_CUSTOMER_ID)
    report_p.add_argument("--window-days", type=int, default=14)
    report_p.add_argument(
        "--kind",
        default=None,
        choices=[k.value for k in FrictionKind],
        help="if given, also print the filtered event list for this kind",
    )
    report_p.add_argument(
        "--json",
        action="store_true",
        help="print the aggregate as JSON instead of a human-readable summary",
    )
    report_p.set_defaults(func=_cmd_report)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
