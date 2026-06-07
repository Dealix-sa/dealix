"""Seed loader for the Dealix Now engine.

Reads the committed demo dataset (`data/demo/saudi_b2b_demo.csv`), skips
data-quality-flagged rows (blank company_name), and deduplicates by
normalized company name keeping the latest `last_interaction`.

Deterministic and offline: no network, no API keys, no LLM.
"""

from __future__ import annotations

import csv
import logging
import unicodedata
from pathlib import Path

log = logging.getLogger(__name__)

# data/demo/saudi_b2b_demo.csv relative to the repo root (two parents up:
# dealix/now/seed.py -> dealix/now -> dealix -> <repo root>).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_CSV = _REPO_ROOT / "data" / "demo" / "saudi_b2b_demo.csv"

# Arabic tatweel + diacritics get stripped so dedupe matches the same
# company written with cosmetic differences.
_ARABIC_DIACRITICS = (
    "".join(chr(c) for c in range(0x0610, 0x061B))
    + "".join(chr(c) for c in range(0x064B, 0x0660))
    + "ـ"
)


def _normalize_name(name: str) -> str:
    """Return a stable, case/diacritic-insensitive key for a company name."""
    text = unicodedata.normalize("NFKC", name or "").strip().lower()
    text = "".join(ch for ch in text if ch not in _ARABIC_DIACRITICS)
    # Collapse internal whitespace runs to a single space.
    return " ".join(text.split())


def _slugify(name: str, sector: str) -> str:
    """Deterministic lead id slug.

    Latin names slugify directly; Arabic-only names fall back to a stable
    sector + ordinal scheme handled by the caller. Here we produce the
    latin-token slug and let the caller disambiguate empties.
    """
    text = unicodedata.normalize("NFKD", name or "")
    ascii_text = text.encode("ascii", "ignore").decode("ascii").lower()
    tokens = [t for t in "".join(ch if ch.isalnum() else " " for ch in ascii_text).split() if t]
    return "_".join(tokens)


def load_targets(csv_path: str | Path | None = None) -> list[dict]:
    """Load and normalize demo targets.

    - Skips rows with a blank ``company_name`` (data-quality flag).
    - Dedupes by normalized company name, keeping the row with the latest
      ``last_interaction`` (ISO date string compare is lexicographic-safe).
    - Returns dicts with the seven canonical columns plus ``id`` and
      ``name_key``.

    The result is deterministic: stable order (first appearance of each
    company) regardless of input dedupe churn.
    """
    path = Path(csv_path) if csv_path is not None else _DEFAULT_CSV
    if not path.exists():
        log.warning("seed_csv_missing path=%s", path)
        return []

    # name_key -> (order_index, row dict)
    chosen: dict[str, tuple[int, dict]] = {}
    order = 0

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            company_name = (raw.get("company_name") or "").strip()
            if not company_name:
                # Data-quality flag: never let a nameless row through.
                continue
            key = _normalize_name(company_name)
            if not key:
                continue

            last_interaction = (raw.get("last_interaction") or "").strip()
            row = {
                "company_name": company_name,
                "sector": (raw.get("sector") or "").strip(),
                "city": (raw.get("city") or "").strip(),
                "relationship_status": (raw.get("relationship_status") or "").strip().lower(),
                "source": (raw.get("source") or "").strip(),
                "last_interaction": last_interaction,
                "notes": (raw.get("notes") or "").strip(),
                "name_key": key,
            }

            existing = chosen.get(key)
            if existing is None:
                chosen[key] = (order, row)
                order += 1
            else:
                prev_order, prev_row = existing
                # Keep the latest last_interaction; preserve first-seen order.
                if last_interaction >= (prev_row.get("last_interaction") or ""):
                    chosen[key] = (prev_order, row)

    ordered = sorted(chosen.values(), key=lambda item: item[0])

    targets: list[dict] = []
    seen_ids: dict[str, int] = {}
    for _idx, row in ordered:
        slug = _slugify(row["company_name"], row["sector"])
        if not slug:
            # Arabic-only name: stable id from sector + ordinal.
            slug = f"{row['sector'] or 'company'}"
        # Disambiguate collisions deterministically.
        if slug in seen_ids:
            seen_ids[slug] += 1
            lead_id = f"lead_{slug}_{seen_ids[slug]}"
        else:
            seen_ids[slug] = 0
            lead_id = f"lead_{slug}"
        row = dict(row)
        row["id"] = lead_id
        targets.append(row)

    return targets


__all__ = ["load_targets"]
