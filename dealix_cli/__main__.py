"""Entrypoint: `python -m dealix_cli <command> --private-ops <path>`."""

from __future__ import annotations

import argparse

from dealix_cli import commands


def _add_private_ops(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--private-ops",
        required=True,
        help="Path to the private ops repository (e.g. ../dealix-ops-private).",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dealix_cli", description="Dealix priority CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("verify", "daily", "dashboard", "weekly", "close-day"):
        sub = subparsers.add_parser(name, help=f"Run the {name} command.")
        _add_private_ops(sub)

    args = parser.parse_args(argv)

    dispatch = {
        "verify": commands.verify,
        "daily": commands.daily,
        "dashboard": commands.dashboard,
        "weekly": commands.weekly,
        "close-day": commands.close_day,
    }
    dispatch[args.command](args.private_ops)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
