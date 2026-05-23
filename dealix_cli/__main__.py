from __future__ import annotations

import argparse

from dealix_cli.commands import daily, weekly, dashboard, verify, sprint, stage, advance


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dealix_cli", description="Dealix operator CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, helptext in [
        ("daily", "Show today's stage criterion in focus."),
        ("weekly", "Show weekly stage decision summary."),
        ("dashboard", "Print full stage checklist with current status."),
        ("verify", "Verify stage evidence directly from private-ops ledgers."),
        ("sprint", "List pending criteria for the current sprint."),
        ("stage", "Show current stage decision and checklist."),
    ]:
        sp = subparsers.add_parser(name, help=helptext)
        sp.add_argument("--private-ops", required=True)

    advance_parser = subparsers.add_parser(
        "advance",
        help="Scan evidence, update stage checklist, and show stage advancement readiness.",
    )
    advance_parser.add_argument("--private-ops", required=True)

    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.command == "daily":
        daily(args.private_ops)
    elif args.command == "weekly":
        weekly(args.private_ops)
    elif args.command == "dashboard":
        dashboard(args.private_ops)
    elif args.command == "verify":
        verify(args.private_ops)
    elif args.command == "sprint":
        sprint(args.private_ops)
    elif args.command == "stage":
        stage(args.private_ops)
    elif args.command == "advance":
        advance(args.private_ops)


if __name__ == "__main__":
    main()
