#!/usr/bin/env python3
"""Dealix Lead Graph adapter — feed the curated Saudi Lead Graph into daily prep.

Maps the founder-curated Saudi Lead Graph CSV
(``docs/ops/lead_machine/SAUDI_LEAD_GRAPH_MASTER.csv``) — a list of *public,
company-level* Saudi B2B prospects (no contact PII) — into the
``LeadCandidate`` shape consumed by ``dealix_daily_lead_prep.run_daily_prep``.

Why this exists
---------------
The master file's columns (``company``, ``website``, ``suggested_channel``,
``first_message_angle`` …) do not match the ``LeadCandidate`` schema (``name``,
``domain``, ``source`` …). This adapter bridges them WITHOUT mutating either
side (Article 11 — compose, don't mutate). It also carries the rich outreach
columns (channel, first-message angle, recommended offer, predicted objection)
forward so the activation runner can build a per-lead call sheet.

Doctrine (Articles 4 & 8 — IMMUTABLE)
-------------------------------------
- The CSV is founder-supplied static data; this module only READS it. No
  scraping, no fetching, no sending — ever.
- ``relationship_strength`` is kept HONEST: every row is public-sourced, so it
  maps only to ``manual_linkedin_research`` (0.40) or
  ``public_business_info_allowed`` (0.65) — NEVER ``warm_intro`` /
  ``partner_referral`` (no fabricated warmth).
- Governance-heavy / high-risk / ``HOLD_FOR_APPROVAL`` rows are dropped by
  default so they are never surfaced for outreach.
- ``contact_name`` is always empty — no personal data leaves the CSV.

Usage:
    from dealix_lead_graph_adapter import load_lead_graph_candidates
    candidates, rich = load_lead_graph_candidates(path)

    # CLI (debug):
    python3 scripts/dealix_lead_graph_adapter.py --limit 5
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
# Make sibling scripts + the repo package tree importable when run standalone.
for _p in (str(Path(__file__).resolve().parent), str(REPO_ROOT)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from dealix_daily_lead_prep import LeadCandidate  # noqa: E402

DEFAULT_LEAD_GRAPH = REPO_ROOT / "docs" / "ops" / "lead_machine" / "SAUDI_LEAD_GRAPH_MASTER.csv"

# Honest, doctrine-safe source buckets only (see saudi_dimensions.score_relationship_strength).
SOURCE_MANUAL_RESEARCH = "manual_linkedin_research"  # 0.40 — cold-ish manual research
SOURCE_PUBLIC_BUSINESS = "public_business_info_allowed"  # 0.65 — public, company-level info
_SAFE_SOURCES = frozenset({SOURCE_MANUAL_RESEARCH, SOURCE_PUBLIC_BUSINESS})

# Rich columns carried forward for the call sheet (keyed by company name).
_RICH_COLUMNS = (
    "suggested_channel",
    "first_message_angle",
    "offer_recommended",
    "objection_prediction",
    "opportunity_type",
    "priority",
    "sector",
    "website",
    "fit_score",
    "intent_score",
)


def _norm(value: Any) -> str:
    return str(value or "").strip()


def _safe_source(suggested_channel: str) -> str:
    """Map intended channel → an honest relationship-strength source.

    Every Lead Graph row is public-sourced, so we never claim warmth. LinkedIn
    manual research is the most honest "still cold-ish" bucket; everything else
    is public business info (allowed, company-level).
    """
    if "LINKEDIN" in suggested_channel.upper():
        return SOURCE_MANUAL_RESEARCH
    return SOURCE_PUBLIC_BUSINESS


def _risk_score(row: dict[str, str]) -> int:
    raw = _norm(row.get("risk_score"))
    return int(raw) if raw.isdigit() else 0


def is_held(row: dict[str, str], *, risk_threshold: int = 70) -> bool:
    """True if a row is governance-held / high-risk and must NOT be surfaced."""
    flags = (
        _norm(row.get("suggested_channel")) + " " + _norm(row.get("recommended_action"))
    ).upper()
    if "HOLD" in flags:
        return True
    return _risk_score(row) >= risk_threshold


def load_lead_graph_candidates(
    path: str | Path = DEFAULT_LEAD_GRAPH,
    *,
    exclude_held: bool = True,
) -> tuple[list[LeadCandidate], dict[str, dict[str, str]]]:
    """Load the Saudi Lead Graph into (candidates, rich_map).

    Args:
        path: CSV path (defaults to the curated master graph).
        exclude_held: Drop HOLD_FOR_APPROVAL / high-risk rows (default True).

    Returns:
        candidates: list[LeadCandidate] ready for ``run_daily_prep``.
        rich_map: {company_name: {rich columns}} for the call sheet.
    """
    path = Path(path)
    candidates: list[LeadCandidate] = []
    rich_map: dict[str, dict[str, str]] = {}

    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            name = _norm(row.get("company"))
            if not name:
                continue
            if exclude_held and is_held(row):
                continue

            channel = _norm(row.get("suggested_channel"))
            candidates.append(
                LeadCandidate(
                    name=name,
                    sector=_norm(row.get("sector")),
                    city="",  # not in the graph; left blank (no fabrication)
                    country=_norm(row.get("country")) or "SA",
                    domain=_norm(row.get("website")),
                    contact_name="",  # no PII ever
                    contact_title=_norm(row.get("decision_roles")),
                    source=_safe_source(channel),
                    locale="ar",
                    annual_turnover_sar=None,
                    notes=(
                        f"{_norm(row.get('opportunity_type'))} · "
                        f"offer={_norm(row.get('offer_recommended'))}"
                    )[:200],
                )
            )
            rich_map[name] = {col: _norm(row.get(col)) for col in _RICH_COLUMNS}

    return candidates, rich_map


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect the Saudi Lead Graph adapter (read-only)."
    )
    parser.add_argument("--path", type=Path, default=DEFAULT_LEAD_GRAPH)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--include-held", action="store_true", help="Include HOLD/high-risk rows")
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"ERROR: lead graph not found: {args.path}", file=sys.stderr)
        return 2

    candidates, rich = load_lead_graph_candidates(args.path, exclude_held=not args.include_held)
    print(f"Loaded {len(candidates)} candidates from {args.path}")
    sources = {c.source for c in candidates}
    print(f"Sources used (must be safe): {sorted(sources)}")
    assert sources <= _SAFE_SOURCES, f"UNSAFE source leaked: {sources - _SAFE_SOURCES}"
    for c in candidates[: max(0, args.limit)]:
        r = rich.get(c.name, {})
        print(
            f"  • {c.name} [{c.source}] title={c.contact_title or '—'} "
            f"channel={r.get('suggested_channel') or '—'} offer={r.get('offer_recommended') or '—'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
