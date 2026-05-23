"""Entry point: ``python -m dealix_cli <command> --private-ops <path>``."""
from __future__ import annotations

import argparse

from dealix_cli.commands import ceo, monthly


def main() -> None:
    parser = argparse.ArgumentParser(prog="dealix_cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ceo_parser = subparsers.add_parser(
        "ceo",
        help="Generate CEO score and action queue.",
    )
    ceo_parser.add_argument("--private-ops", required=True)

    monthly_parser = subparsers.add_parser(
        "monthly",
        help="Generate monthly strategy and finance review.",
    )
    monthly_parser.add_argument("--private-ops", required=True)

    args = parser.parse_args()
    if args.command == "ceo":
        ceo(args.private_ops)
    elif args.command == "monthly":
        monthly(args.private_ops)


if __name__ == "__main__":
    main()
