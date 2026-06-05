#!/usr/bin/env python3
"""
targeting_enrichment.py — normalize + enrich raw company candidates.

Takes raw rows (from the seed CSV or a discovery provider) and produces clean,
deduplicated company records ready for the compliance gate and scorecard. No
network calls: enrichment here is structural (domain normalization, evidence
counting, sector/phase tagging, dedupe). Firmographic *inference* from page
content is intentionally out of scope for this module — it only formalizes what
the founder/discovery already observed, so every field stays evidence-backed.

Usage:
    python scripts/targeting_enrichment.py --seed data/targeting/company_seed_template.csv \
        --out data/targeting/out/company_master.jsonl
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import yaml  # noqa: E402

DATA = _ROOT / "data" / "targeting"


def _active_sector_ids(phase: int | None) -> set[str]:
    path = DATA / "sectors.yml"
    if not path.exists():
        return set()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rows = data.get("sectors", []) or []
    if phase is not None:
        rows = [r for r in rows if int(r.get("phase", 1)) <= phase]
    return {str(r.get("id")) for r in rows if r.get("id")}


def _sensitive_sectors() -> set[str]:
    path = DATA / "blocked_sources.yml"
    if not path.exists():
        return set()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {str(s).lower() for s in data.get("sensitive_sectors", []) or []}


def normalize_domain(website: str) -> str:
    """Lowercase host without leading www and without scheme/path."""
    if not website:
        return ""
    url = website if "//" in website else f"https://{website}"
    host = (urlparse(url).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


def dedupe_key(record: dict[str, Any]) -> str:
    """Companies are the same if domain matches; fall back to normalized name."""
    dom = normalize_domain(record.get("website", ""))
    if dom:
        return f"domain:{dom}"
    name = " ".join(str(record.get("company_name", "")).lower().split())
    return f"name:{name}"


def enrich_company(
    raw: dict[str, Any],
    *,
    phase: int | None = 1,
    active_sectors: set[str] | None = None,
    sensitive: set[str] | None = None,
) -> dict[str, Any]:
    """Return a normalized company record with derived fields."""
    active_sectors = active_sectors if active_sectors is not None else _active_sector_ids(phase)
    sensitive = sensitive if sensitive is not None else _sensitive_sectors()

    domain = normalize_domain(raw.get("website", ""))
    sources = [s for s in (raw.get("source_urls") or []) if s]
    sector = str(raw.get("sector", "")).strip().lower()

    record: dict[str, Any] = {
        "company_name": str(raw.get("company_name", "")).strip(),
        "website": raw.get("website", ""),
        "domain": domain,
        "city": str(raw.get("city", "")).strip(),
        "country": str(raw.get("country", "Saudi Arabia")).strip() or "Saudi Arabia",
        "sector": sector,
        "subsector": str(raw.get("subsector", "")).strip(),
        "company_size_signal": raw.get("company_size_signal", ""),
        "decision_maker_role": raw.get("decision_maker_role", "Founder / GM / Sales Director"),
        "contact_channel": raw.get("contact_channel", "contact_page"),
        "source_urls": sources,
        "source_types": raw.get("source_types", []),
        "evidence_count": len(sources),
        "pain_signals": raw.get("pain_signals", []) or [],
        "intent_signals": raw.get("intent_signals", []) or [],
        "partnership_signal": bool(raw.get("partnership_signal", False)),
        "weakness_hypothesis": raw.get("weakness_hypothesis", ""),
        "recommended_offer": raw.get("recommended_offer", ""),
        "icp_in_phase": (sector in active_sectors) if active_sectors else True,
        "is_sensitive_sector": sector in sensitive,
        "targeting_score": 0,
        "grade": "",
        "risk_flags": list(raw.get("risk_flags", []) or []),
        "next_action": "Manual founder review",
        "draft_status": "needs_approval",
    }
    if record["is_sensitive_sector"] and "sensitive_sector" not in record["risk_flags"]:
        record["risk_flags"].append("sensitive_sector")
    return record


def normalize_and_dedupe(
    rows: list[dict[str, Any]],
    *,
    phase: int | None = 1,
) -> list[dict[str, Any]]:
    """Enrich all rows and drop duplicates (keeping the one with more evidence)."""
    active = _active_sector_ids(phase)
    sensitive = _sensitive_sectors()
    best: dict[str, dict[str, Any]] = {}
    for raw in rows:
        rec = enrich_company(raw, phase=phase, active_sectors=active, sensitive=sensitive)
        if not rec["company_name"]:
            continue
        key = dedupe_key(rec)
        if key in best:
            best[key]["is_duplicate"] = True
            # keep the record with more evidence
            if rec["evidence_count"] <= best[key]["evidence_count"]:
                continue
        best[key] = rec
    return list(best.values())


# --------------------------------------------------------------------------- #
# Seed CSV loading
# --------------------------------------------------------------------------- #
def load_seed_csv(path: Path) -> list[dict[str, Any]]:
    """Load the founder seed CSV. Collapses source_url_1/2/... into source_urls."""
    rows: list[dict[str, Any]] = []
    text = path.read_text(encoding="utf-8")
    # strip comment lines (csv module doesn't skip them)
    clean = "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))
    reader = csv.DictReader(clean.splitlines())
    for r in reader:
        sources = [v for k, v in r.items() if k and k.startswith("source_url") and v]
        rows.append(
            {
                "company_name": r.get("company_name", ""),
                "website": r.get("website", ""),
                "city": r.get("city", ""),
                "country": r.get("country", "Saudi Arabia"),
                "sector": r.get("sector", ""),
                "subsector": r.get("subsector", ""),
                "source_urls": sources,
                # Optional founder-observed columns (pipe-separated lists).
                "pain_signals": _split_list(r.get("pain_signals")),
                "intent_signals": _split_list(r.get("intent_signals")),
                "recommended_offer": (r.get("recommended_offer") or "").strip(),
                "company_size_signal": (r.get("company_size_signal") or "").strip(),
                "contact_channel": (r.get("contact_channel") or "contact_page").strip(),
                "partnership_signal": str(r.get("partnership_signal", "")).strip().lower()
                in {"1", "true", "yes", "y"},
            }
        )
    return rows


def _split_list(value: str | None) -> list[str]:
    """Parse a pipe-separated cell into a clean list (empty -> [])."""
    if not value:
        return []
    return [v.strip() for v in str(value).split("|") if v.strip()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix Targeting OS enrichment + dedupe")
    ap.add_argument("--seed", required=True, help="seed CSV path")
    ap.add_argument("--phase", type=int, default=1)
    ap.add_argument("--out", default=None, help="write enriched company_master.jsonl")
    args = ap.parse_args(argv)

    raw = load_seed_csv(Path(args.seed))
    records = normalize_and_dedupe(raw, phase=args.phase)
    lines = [json.dumps(r, ensure_ascii=False) for r in records]
    if args.out:
        outp = Path(args.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"wrote {len(records)} companies -> {outp}", file=sys.stderr)
    else:
        print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
