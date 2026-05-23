"""Dealix CLI commands.

Each command resolves a private-ops working directory and prints the
canonical files an operator should review. No I/O against external
systems; no writes. Safe to run from any environment.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def ensure_private_ops(private_ops: str | None) -> Path:
    """Resolve and return the private-ops directory.

    The directory must exist. We never create it implicitly so callers
    cannot accidentally write public scaffolding into a wrong location.
    """
    if not private_ops:
        raise SystemExit(
            "Missing --private-ops <path>. Set PRIVATE_OPS to the local "
            "checkout of dealix-ops-private."
        )
    path = Path(private_ops).expanduser().resolve()
    if not path.exists():
        raise SystemExit(f"Private ops path does not exist: {path}")
    if not path.is_dir():
        raise SystemExit(f"Private ops path is not a directory: {path}")
    return path


def content(private_ops: str) -> None:
    private_ops_path = ensure_private_ops(private_ops)
    print("\nDealix Brand, Proof & Content")
    print("=" * 40)
    print("Review these files:")
    print(f"- {private_ops_path / 'content/proof_library.md'}")
    print(f"- {private_ops_path / 'content/content_calendar.csv'}")
    print(f"- {private_ops_path / 'content/published_log.csv'}")
    print(f"- {private_ops_path / 'content/approved_claims.md'}")
    print(f"- {private_ops_path / 'trust/claim_review_log.csv'}")
    print("\nContent Rule:")
    print("No proof without approval. No claim without evidence.")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="dealix_cli")
    sub = parser.add_subparsers(dest="command", required=True)

    content_parser = sub.add_parser(
        "content",
        help="Show Brand, Proof & Content OS review files.",
    )
    content_parser.add_argument(
        "--private-ops",
        required=True,
        help="Path to the dealix-ops-private checkout.",
    )

    args = parser.parse_args(argv)
    if args.command == "content":
        content(args.private_ops)
    else:  # pragma: no cover - argparse enforces required subcommand
        parser.print_help()


if __name__ == "__main__":
    main()
