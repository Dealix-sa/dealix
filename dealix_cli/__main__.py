"""Entry point for ``python -m dealix_cli``.

Subcommands:
    delivery   Show the canonical Delivery & Client Success files to touch.

Usage:
    python -m dealix_cli delivery --private-ops /path/to/dealix-ops-private
"""

from __future__ import annotations

import argparse
import sys

from dealix_cli import commands


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dealix_cli")
    sub = parser.add_subparsers(dest="command", required=True)

    delivery_p = sub.add_parser(
        "delivery",
        help="Show Delivery & Client Success files in the private workspace.",
    )
    delivery_p.add_argument(
        "--private-ops",
        required=True,
        help="Path to the private operations workspace (dealix-ops-private).",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "delivery":
        commands.delivery(args.private_ops)
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
