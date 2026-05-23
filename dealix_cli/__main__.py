"""Dealix founder CLI entry point."""
from __future__ import annotations

import argparse

from dealix_cli.commands import control_tower


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dealix_cli", description="Dealix founder CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    control_tower_parser = subparsers.add_parser(
        "control-tower",
        help="Generate Dealix executive control tower brief.",
    )
    control_tower_parser.add_argument("--private-ops", required=True)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "control-tower":
        control_tower(args.private_ops)
    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
