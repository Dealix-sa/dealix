"""
Dealix OS Runtime — CLI Entry Point
====================================
Usage:
    python -m dealix.os_runtime validate
    python -m dealix.os_runtime score-company <file.json>
    python -m dealix.os_runtime route-offer <file.json>
    python -m dealix.os_runtime approval-check <action>
    python -m dealix.os_runtime channel-route <file.json>
    python -m dealix.os_runtime growth-dry-run [--limit N] [--dry-run]
    python -m dealix.os_runtime daily-brief
"""

import sys
import json
import argparse
from pathlib import Path

# Ensure repo root is on path
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def cmd_validate(args) -> int:
    """Validate all OS configs and schemas."""
    from dealix.os_runtime.config_loader import load_all_configs

    print("Validating OS configs...")
    results = load_all_configs()
    errors = {k: v for k, v in results.items() if v.get("status") == "error"}
    ok = {k: v for k, v in results.items() if v.get("status") == "ok"}

    for path, meta in ok.items():
        print(f"  [OK] {path} ({meta.get('type', '?')})")

    if errors:
        print("\nERRORS:")
        for path, meta in errors.items():
            print(f"  [FAIL] {path}: {meta.get('error', 'unknown error')}")
        print(f"\n{len(errors)} error(s) found. Fix before proceeding.")
        return 1

    print(f"\nAll {len(ok)} configs validated successfully.")
    return 0


def cmd_score_company(args) -> int:
    """Score a company from a JSON file."""
    from dealix.os_runtime.company_scorer import score_from_dict

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    with file_path.open("r", encoding="utf-8") as f:
        company_data = json.load(f)

    result = score_from_dict(company_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_route_offer(args) -> int:
    """Route a company to the best offer from a JSON file."""
    from dealix.os_runtime.offer_router import route_offer

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    with file_path.open("r", encoding="utf-8") as f:
        company_data = json.load(f)

    result = route_offer(company_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_approval_check(args) -> int:
    """Check if an action requires approval."""
    from dealix.os_runtime.approval_gate import check_approval

    action = args.action
    result = check_approval(action)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["allowed"]:
        return 2  # Blocked
    if result["requires_approval"]:
        return 1  # Needs approval
    return 0  # Free action


def cmd_channel_route(args) -> int:
    """Route channels for a company from a JSON file."""
    from dealix.os_runtime.channel_router import route_channels

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    with file_path.open("r", encoding="utf-8") as f:
        company_data = json.load(f)

    result = route_channels(company_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_growth_dry_run(args) -> int:
    """
    Simulate the growth outreach pipeline (dry run).
    No actual sends — shows what would be queued.
    """
    limit = getattr(args, "limit", 10)
    dry_run = getattr(args, "dry_run", True)

    print(f"Growth dry-run: limit={limit}, dry_run={dry_run}")
    print("Note: This is a simulation. No messages are sent.")
    print("\nDoctrine checks:")
    print("  [OK] cold_whatsapp: BLOCKED")
    print("  [OK] linkedin_automation: BLOCKED")
    print("  [OK] scraping: BLOCKED")
    print("  [OK] all sends require founder approval")
    print("\nDry-run complete. Implement warm_list input + real pipeline for full run.")
    return 0


def cmd_daily_brief(args) -> int:
    """Generate today's founder daily brief."""
    from dealix.os_runtime.daily_brief import generate_brief
    from datetime import date

    brief = generate_brief()
    print(json.dumps(brief, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m dealix.os_runtime",
        description="Dealix OS Runtime CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # validate
    subparsers.add_parser("validate", help="Validate all OS configs and schemas")

    # score-company
    p_score = subparsers.add_parser("score-company", help="Score a company from a JSON file")
    p_score.add_argument("file", help="Path to company JSON file")

    # route-offer
    p_route = subparsers.add_parser("route-offer", help="Route a company to the best offer")
    p_route.add_argument("file", help="Path to company JSON file")

    # approval-check
    p_approval = subparsers.add_parser("approval-check", help="Check if an action requires approval")
    p_approval.add_argument("action", help="Action name to check")

    # channel-route
    p_channel = subparsers.add_parser("channel-route", help="Route channels for a company")
    p_channel.add_argument("file", help="Path to company JSON file")

    # growth-dry-run
    p_growth = subparsers.add_parser("growth-dry-run", help="Simulate growth pipeline (dry run)")
    p_growth.add_argument("--limit", type=int, default=10, help="Max companies to simulate")
    p_growth.add_argument("--dry-run", action="store_true", default=True, help="Dry run mode (default: True)")

    # daily-brief
    subparsers.add_parser("daily-brief", help="Generate today's founder daily brief")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "validate": cmd_validate,
        "score-company": cmd_score_company,
        "route-offer": cmd_route_offer,
        "approval-check": cmd_approval_check,
        "channel-route": cmd_channel_route,
        "growth-dry-run": cmd_growth_dry_run,
        "daily-brief": cmd_daily_brief,
    }

    handler = commands.get(args.command)
    if handler is None:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1

    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
