"""Dealix CLI entrypoint: `python -m dealix_cli <command>`."""

from __future__ import annotations

import argparse

from dealix_cli.commands import audit, business_score


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dealix_cli", description="Dealix founder CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    business_score_parser = subparsers.add_parser(
        "business-score",
        help="Generate CEO business score from private ops evidence.",
    )
    business_score_parser.add_argument("--private-ops", required=True)

    audit_parser = subparsers.add_parser(
        "audit",
        help="Run CEO business systems audit and refresh the score.",
    )
    audit_parser.add_argument("--private-ops", required=True)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "business-score":
        business_score(args.private_ops)
    elif args.command == "audit":
        audit(args.private_ops)


if __name__ == "__main__":
    main()
