"""Loads and caches os/*.yml and os/*.json config files."""
from __future__ import annotations

from pathlib import Path
from functools import lru_cache
import yaml
import json

OS_DIR = Path(__file__).resolve().parents[1] / "os"


@lru_cache(maxsize=None)
def load_offers() -> dict:
    return yaml.safe_load((OS_DIR / "03_OFFERS.yml").read_text())["offers"]


@lru_cache(maxsize=None)
def load_markets() -> dict:
    return yaml.safe_load((OS_DIR / "04_MARKETS.yml").read_text())


@lru_cache(maxsize=None)
def load_scoring() -> dict:
    return yaml.safe_load((OS_DIR / "05_SCORING.yml").read_text())


@lru_cache(maxsize=None)
def load_approval_gates() -> dict:
    return yaml.safe_load((OS_DIR / "06_APPROVAL_GATES.yml").read_text())


@lru_cache(maxsize=None)
def load_company_schema() -> dict:
    return json.loads((OS_DIR / "07_COMPANY_MEMORY_SCHEMA.json").read_text())


@lru_cache(maxsize=None)
def load_client_schema() -> dict:
    return json.loads((OS_DIR / "08_CLIENT_MEMORY_SCHEMA.json").read_text())


@lru_cache(maxsize=None)
def load_project_schema() -> dict:
    return json.loads((OS_DIR / "09_PROJECT_MEMORY_SCHEMA.json").read_text())


class OSConfig:
    offers = staticmethod(load_offers)
    markets = staticmethod(load_markets)
    scoring = staticmethod(load_scoring)
    approval_gates = staticmethod(load_approval_gates)
    company_schema = staticmethod(load_company_schema)
    client_schema = staticmethod(load_client_schema)
    project_schema = staticmethod(load_project_schema)
