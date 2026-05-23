from __future__ import annotations

import argparse

from dealix_cli.commands import daily, weekly, dashboard, verify


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dealix-cli",
        description="Dealix CEO Operating Intelligence command center.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    daily_parser = subparsers.add_parser(
        "daily",
        help="Generate daily CEO brief, decision queue, and dashboard data.",
    )
    daily_parser.add_argument("--private-ops", required=True)

    weekly_parser = subparsers.add_parser(
        "weekly",
        help="Generate weekly operating intelligence and verify private ops.",
    )
    weekly_parser.add_argument("--private-ops", required=True)

    dashboard_parser = subparsers.add_parser(
        "dashboard",
        help="Generate dashboard data from private ops.",
    )
    dashboard_parser.add_argument("--private-ops", required=True)

    verify_parser = subparsers.add_parser(
        "verify",
        help="Run public and optional private verification checks.",
    )
    verify_parser.add_argument("--private-ops", required=False)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "daily":
        daily(args.private_ops)
    elif args.command == "weekly":
        weekly(args.private_ops)
    elif args.command == "dashboard":
        dashboard(args.private_ops)
    elif args.command == "verify":
        verify(args.private_ops)
    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
