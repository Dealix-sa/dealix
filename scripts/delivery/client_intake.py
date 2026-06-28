#!/usr/bin/env python3
"""Client intake — populate the intake phase of a client workspace.

Usage:
    python scripts/delivery/client_intake.py --client-slug acme \\
        --sponsor "Jane Doe" --outcome "Cut lead time 40%" --baseline "10 days" --target "6 days"
"""
from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = REPO_ROOT / "clients"


def _workspace(slug: str) -> Path:
    ws = CLIENTS_DIR / slug
    if not ws.exists():
        raise FileNotFoundError(f"client workspace not found: {ws}")
    return ws


def fill_intake(
    slug: str,
    sponsor: str | None = None,
    outcome: str | None = None,
    baseline: str | None = None,
    target: str | None = None,
) -> Path:
    """Fill the intake form with the provided fields, preserving template structure."""
    ws = _workspace(slug)
    form = ws / "00_intake" / "intake_form.md"
    if not form.exists():
        raise FileNotFoundError(f"intake form missing: {form}")

    text = form.read_text(encoding="utf-8")
    replacements: list[tuple[str, str]] = []
    if sponsor:
        replacements.append(("**Sponsor (executive owner):**", f"**Sponsor (executive owner):** {sponsor}"))
    if outcome:
        replacements.append(
            ("**Target business outcome (one sentence):**", f"**Target business outcome (one sentence):** {outcome}")
        )
    if baseline:
        replacements.append(("**Baseline value today:**", f"**Baseline value today:** {baseline}"))
    if target:
        replacements.append(("**Target value + date:**", f"**Target value + date:** {target}"))

    for old, new in replacements:
        text = text.replace(old, new)

    text += f"\n\n_Intake completed: {_dt.date.today().isoformat()}_\n"
    form.write_text(text, encoding="utf-8")
    return form


def main() -> int:
    parser = argparse.ArgumentParser(description="Fill client intake form.")
    parser.add_argument("--client-slug", required=True)
    parser.add_argument("--sponsor", default=None)
    parser.add_argument("--outcome", default=None)
    parser.add_argument("--baseline", default=None)
    parser.add_argument("--target", default=None)
    args = parser.parse_args()

    try:
        path = fill_intake(args.client_slug, args.sponsor, args.outcome, args.baseline, args.target)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"intake filled: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
