"""Entry point for ``python -m dealix_cli``.

Subcommands:
    revenue-ops   Show revenue ops file map and refresh the CEO action queue.
"""
from __future__ import annotations

import argparse

from . import commands


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dealix",
        description="Dealix founder CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    revenue_ops_parser = subparsers.add_parser(
        "revenue-ops",
        help="Show revenue operations files and generate CEO action queue.",
    )
    revenue_ops_parser.add_argument("--private-ops", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "revenue-ops":
        commands.revenue_ops(args.private_ops)
        return 0
    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
