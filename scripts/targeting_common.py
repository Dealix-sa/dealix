#!/usr/bin/env python3
"""Shared helpers for the Dealix Intelligence-to-Revenue-to-Delivery OS.

This module is the single place that knows where the targeting config and data
files live, how to load them, and how to read/write the company master record.
Every `targeting_*.py` script imports from here so the pipeline stays consistent
and auditable.

Pure stdlib + PyYAML. No network, no LLM, no scraping. The whole targeting OS is
deterministic and offline so its output can be reviewed and reproduced.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml

# ─────────────────────────── paths ───────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data" / "targeting"
OUT_DIR = DATA_DIR / "out"
CUSTOMERS_DIR = REPO_ROOT / "customers"

SCORING_WEIGHTS = DATA_DIR / "scoring_weights.yml"
SECTORS_FILE = DATA_DIR / "sectors.yml"
CITIES_FILE = DATA_DIR / "cities.yml"
SIGNALS_FILE = DATA_DIR / "signals.yml"
BLOCKED_SOURCES = DATA_DIR / "blocked_sources.yml"
COMPANY_MASTER = DATA_DIR / "company_master.jsonl"
OUTCOMES_FILE = DATA_DIR / "outcomes.jsonl"


# ─────────────────────────── config loaders ───────────────────────────
def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML config file into a dict (empty dict if missing/empty)."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_weights() -> dict[str, Any]:
    return load_yaml(SCORING_WEIGHTS)


def load_sectors() -> dict[str, Any]:
    return load_yaml(SECTORS_FILE).get("sectors", {})


def load_cities() -> dict[str, Any]:
    return load_yaml(CITIES_FILE).get("cities", {})


def load_signals() -> dict[str, Any]:
    return load_yaml(SIGNALS_FILE)


def load_blocked() -> dict[str, Any]:
    return load_yaml(BLOCKED_SOURCES)


# ─────────────────────────── company records ───────────────────────────
def _coerce_bool(value: Any) -> Any:
    """CSV gives strings; normalise 'true'/'false'/'1'/'0' to bool."""
    if isinstance(value, str):
        low = value.strip().lower()
        if low in {"true", "1", "yes", "y"}:
            return True
        if low in {"false", "0", "no", "n", ""}:
            return False
    return value


# Fields that carry boolean signals (so CSV strings get coerced correctly).
_BOOL_FIELDS = {
    "b2b", "case_study_presence", "weak_cta", "many_services_no_focus",
    "no_case_studies", "unclear_followup", "fragmented_tools",
    "recurring_support", "delivery_no_visibility", "many_clients_no_memory",
    "ai_claims_no_governance", "hiring_signal", "growth_signal",
    "partnership_signal", "technology_signal", "recent_news",
    "serves_many_clients", "personal_phone", "personal_email_only",
    "no_robots_respect",
}


def normalize_record(raw: dict[str, Any]) -> dict[str, Any]:
    """Coerce a raw company dict (CSV row or JSON) into the canonical shape."""
    rec = dict(raw)
    for field in _BOOL_FIELDS:
        if field in rec:
            rec[field] = _coerce_bool(rec[field])
    # source_urls / services may arrive as ';' or ',' separated strings
    for field in ("source_urls", "services"):
        val = rec.get(field)
        if isinstance(val, str):
            sep = ";" if ";" in val else ","
            rec[field] = [s.strip() for s in val.split(sep) if s.strip()]
        elif val is None:
            rec[field] = []
    if "evidence_count" in rec and rec["evidence_count"] not in (None, ""):
        try:
            rec["evidence_count"] = int(rec["evidence_count"])
        except (TypeError, ValueError):
            rec["evidence_count"] = 0
    else:
        rec.setdefault("evidence_count", len(rec.get("source_urls", [])))
    return rec


def load_companies_jsonl(path: Path = COMPANY_MASTER) -> list[dict[str, Any]]:
    """Read the company master (one JSON object per line)."""
    companies: list[dict[str, Any]] = []
    if not path.exists():
        return companies
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            companies.append(normalize_record(json.loads(line)))
    return companies


def load_companies_csv(path: Path) -> list[dict[str, Any]]:
    """Read a seed CSV into normalized company dicts (skips REPLACE: rows)."""
    companies: list[dict[str, Any]] = []
    if not path.exists():
        return companies
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            name = (row.get("company_name") or "").strip()
            if not name or name.upper().startswith("REPLACE:"):
                continue
            companies.append(normalize_record(row))
    return companies


def load_companies(path: Path) -> list[dict[str, Any]]:
    """Load companies from .jsonl or .csv based on the extension."""
    if str(path).endswith(".csv"):
        return load_companies_csv(path)
    return load_companies_jsonl(path)


def load_outcomes(path: Path = OUTCOMES_FILE) -> list[dict[str, Any]]:
    """Read the outcomes ledger (one JSON object per line)."""
    outcomes: list[dict[str, Any]] = []
    if not path.exists():
        return outcomes
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                outcomes.append(json.loads(line))
    return outcomes


def slugify(name: str) -> str:
    """Filesystem-safe slug for a company name (used for customer folders)."""
    keep = []
    for ch in name.lower().strip():
        if ch.isalnum():
            keep.append(ch)
        elif ch in {" ", "-", "_", "."}:
            keep.append("-")
    slug = "".join(keep)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "company"


def ensure_out_dir() -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUT_DIR
