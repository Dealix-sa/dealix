"""Entry point for `python -m dealix_cli`."""

from __future__ import annotations

import argparse

from dealix_cli.commands import assurance


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dealix_cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    assurance_parser = subparsers.add_parser(
        "assurance",
        help="Generate execution assurance report from real evidence.",
    )
    assurance_parser.add_argument("--private-ops", required=True)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "assurance":
        assurance(args.private_ops)
    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
