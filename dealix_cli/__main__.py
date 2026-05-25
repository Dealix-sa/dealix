"""Dealix CEO operating CLI entry point.

Usage:
    python -m dealix_cli data-quality --private-ops /path/to/private-ops
    python -m dealix_cli snapshot      --private-ops /path/to/private-ops
    python -m dealix_cli business-score --private-ops ...
    python -m dealix_cli assurance      --private-ops ...
    python -m dealix_cli control-tower  --private-ops ...
"""

from __future__ import annotations

import argparse

from dealix_cli.commands import (
    assurance,
    business_score,
    control_tower,
    data_quality,
    snapshot,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dealix_cli", description="Dealix CEO operating CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    data_quality_parser = subparsers.add_parser(
        "data-quality",
        help="Audit private ops CSV data quality against schemas.",
    )
    data_quality_parser.add_argument("--private-ops", required=True)

    snapshot_parser = subparsers.add_parser(
        "snapshot",
        help="Write a company snapshot JSON for the dashboard.",
    )
    snapshot_parser.add_argument("--private-ops", required=True)

    business_parser = subparsers.add_parser(
        "business-score",
        help="Compute the daily CEO business score.",
    )
    business_parser.add_argument("--private-ops", required=True)

    assurance_parser = subparsers.add_parser(
        "assurance",
        help="Compute execution assurance from the evidence ledger.",
    )
    assurance_parser.add_argument("--private-ops", required=True)

    control_tower_parser = subparsers.add_parser(
        "control-tower",
        help="Render the CEO control tower brief.",
    )
    control_tower_parser.add_argument("--private-ops", required=True)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "data-quality":
        data_quality(args.private_ops)
    elif args.command == "snapshot":
        snapshot(args.private_ops)
    elif args.command == "business-score":
        business_score(args.private_ops)
    elif args.command == "assurance":
        assurance(args.private_ops)
    elif args.command == "control-tower":
        control_tower(args.private_ops)


if __name__ == "__main__":
    main()
