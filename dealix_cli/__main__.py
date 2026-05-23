"""Argument parsing entry point for `python -m dealix_cli`."""

from __future__ import annotations

import argparse

from dealix_cli.commands import (
    close_day,
    daily,
    dashboard,
    sprint,
    verify,
    weekly,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dealix_cli",
        description="Dealix founder operating CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    sprint_parser = subparsers.add_parser(
        "sprint",
        help="Show and verify the current priority execution sprint.",
    )
    sprint_parser.add_argument("--private-ops", required=True)

    daily_parser = subparsers.add_parser(
        "daily",
        help="Run the daily founder loop.",
    )
    daily_parser.add_argument("--private-ops", required=True)

    close_day_parser = subparsers.add_parser(
        "close-day",
        help="Run end-of-day execution gate.",
    )
    close_day_parser.add_argument("--private-ops", required=True)

    weekly_parser = subparsers.add_parser(
        "weekly",
        help="Run the weekly learning review checklist.",
    )
    weekly_parser.add_argument("--private-ops", required=True)

    verify_parser = subparsers.add_parser(
        "verify",
        help="Run public + private verifiers.",
    )
    verify_parser.add_argument("--private-ops", required=True)

    dashboard_parser = subparsers.add_parser(
        "dashboard",
        help="Print dashboard pointers.",
    )
    dashboard_parser.add_argument("--private-ops", required=True)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "sprint":
        sprint(args.private_ops)
    elif args.command == "daily":
        daily(args.private_ops)
    elif args.command == "close-day":
        close_day(args.private_ops)
    elif args.command == "weekly":
        weekly(args.private_ops)
    elif args.command == "verify":
        verify(args.private_ops)
    elif args.command == "dashboard":
        dashboard(args.private_ops)
    else:
        parser.error(f"unknown command: {args.command}")


if __name__ == "__main__":
    main()
