"""Entry point for ``python -m dealix_cli``.

Dispatches founder commands such as ``mission-control`` to their underlying
implementations. Keep dispatch flat — one block per command.
"""

from __future__ import annotations

import argparse
import sys

from .commands import mission_control


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dealix_cli")
    sub = parser.add_subparsers(dest="command", required=True)

    mc = sub.add_parser(
        "mission-control",
        help="Generate the Dealix Mission Control snapshot for the founder.",
    )
    mc.add_argument("--private-ops", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "mission-control":
        mission_control(args.private_ops)
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
