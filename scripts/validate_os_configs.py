#!/usr/bin/env python3
"""
validate_os_configs.py — Dealix OS Configuration Validator

Checks:
  - os/*.yml parseability and required fields
  - os/growth/*.yml parseability and required fields
  - os/schemas/*.json valid JSON
  - approval gates consistency
  - offers catalog validity
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
OS_DIR = REPO_ROOT / "os"
GROWTH_DIR = OS_DIR / "growth"
SCHEMAS_DIR = OS_DIR / "schemas"

ERRORS: list[str] = []
WARNINGS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)
    print(f"  ERROR: {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  WARN:  {msg}")


def ok(msg: str) -> None:
    print(f"  OK:    {msg}")


# ---------------------------------------------------------------------------
# YAML loaders
# ---------------------------------------------------------------------------


def load_yaml(path: Path) -> dict | None:
    try:
        with path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        if data is None:
            warn(f"{path.name} is empty or null YAML")
            return {}
        if not isinstance(data, dict):
            err(f"{path.name} top-level is not a mapping (got {type(data).__name__})")
            return None
        ok(f"Parsed {path.name}")
        return data
    except yaml.YAMLError as exc:
        err(f"{path.name} YAML parse error: {exc}")
        return None


def load_json(path: Path) -> dict | None:
    try:
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        ok(f"Parsed {path.name}")
        return data
    except json.JSONDecodeError as exc:
        err(f"{path.name} JSON parse error: {exc}")
        return None


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------


def check_offers(data: dict, path: Path) -> None:
    if "offers" not in data:
        err(f"{path.name}: missing top-level 'offers' key")
        return
    offers = data["offers"]
    if not isinstance(offers, dict):
        err(f"{path.name}: 'offers' must be a mapping")
        return
    required_offer_fields = {"id", "name", "category"}
    for offer_key, offer_val in offers.items():
        if not isinstance(offer_val, dict):
            err(f"{path.name}: offer '{offer_key}' is not a mapping")
            continue
        for field in required_offer_fields:
            if field not in offer_val:
                err(f"{path.name}: offer '{offer_key}' missing required field '{field}'")
    ok(f"{path.name}: {len(offers)} offers validated")


def check_markets(data: dict, path: Path) -> None:
    if "primary_markets" not in data:
        err(f"{path.name}: missing 'primary_markets' key")
        return
    markets = data["primary_markets"]
    required_fields = {"id", "name", "priority"}
    for key, val in markets.items():
        if not isinstance(val, dict):
            continue
        for field in required_fields:
            if field not in val:
                err(f"{path.name}: market '{key}' missing required field '{field}'")
    ok(f"{path.name}: {len(markets)} markets validated")


def check_scoring(data: dict, path: Path) -> None:
    required_top = {"version", "max_score", "scoring_dimensions", "decision_thresholds"}
    for field in required_top:
        if field not in data:
            err(f"{path.name}: missing required field '{field}'")
    dims = data.get("scoring_dimensions", {})
    total_weight = sum(
        v.get("weight", 0) for v in dims.values() if isinstance(v, dict)
    )
    if total_weight != 100:
        err(
            f"{path.name}: scoring_dimensions weights sum to {total_weight}, expected 100"
        )
    else:
        ok(f"{path.name}: dimension weights sum correctly to 100")


def check_approval_gates(data: dict, path: Path) -> None:
    required_top = {"version", "enforced_by", "gates"}
    for field in required_top:
        if field not in data:
            err(f"{path.name}: missing required field '{field}'")
    gates = data.get("gates", {})
    for gate_key, gate_val in gates.items():
        if not isinstance(gate_val, dict):
            continue
        if "id" not in gate_val:
            err(f"{path.name}: gate '{gate_key}' missing 'id'")
        if "requires_human_approval" not in gate_val:
            err(
                f"{path.name}: gate '{gate_key}' missing 'requires_human_approval'"
            )
    ok(f"{path.name}: {len(gates)} gates validated")


def check_channel_router(data: dict, path: Path) -> None:
    if "channels" not in data:
        err(f"{path.name}: missing 'channels' key")
        return
    required_channel_fields = {"priority", "approval_required"}
    channels = data["channels"]
    for ch_key, ch_val in channels.items():
        if not isinstance(ch_val, dict):
            continue
        for field in required_channel_fields:
            if field not in ch_val:
                err(f"{path.name}: channel '{ch_key}' missing '{field}'")
    ok(f"{path.name}: {len(channels)} channels validated")


def check_anti_ban(data: dict, path: Path) -> None:
    if "rules" not in data:
        err(f"{path.name}: missing 'rules' key")
        return
    required_rule_fields = {"daily_limit", "hourly_limit", "required_opt_in"}
    rules = data["rules"]
    for rule_key, rule_val in rules.items():
        if not isinstance(rule_val, dict):
            continue
        for field in required_rule_fields:
            if field not in rule_val:
                err(f"{path.name}: rule '{rule_key}' missing '{field}'")
    ok(f"{path.name}: {len(rules)} anti-ban rules validated")


def check_schema_json(data: dict, path: Path) -> None:
    if "$schema" not in data and "title" not in data:
        warn(f"{path.name}: missing '$schema' or 'title' (may not be a JSON Schema)")
    if "type" in data and "properties" in data:
        ok(f"{path.name}: JSON Schema structure confirmed")
    elif "type" in data:
        ok(f"{path.name}: JSON structure confirmed")


# ---------------------------------------------------------------------------
# Main dispatcher
# ---------------------------------------------------------------------------

OS_YAML_CHECKS: dict[str, callable] = {
    "03_OFFERS.yml": check_offers,
    "04_MARKETS.yml": check_markets,
    "05_SCORING.yml": check_scoring,
    "06_APPROVAL_GATES.yml": check_approval_gates,
}

GROWTH_YAML_CHECKS: dict[str, callable] = {
    "CHANNEL_ROUTER.yml": check_channel_router,
    "ANTI_BAN_GUARDIAN.yml": check_anti_ban,
    "GCC_SECTOR_OFFERS.yml": lambda d, p: ok(f"{p.name}: sector offers parsed"),
}


def run() -> int:
    print("\n=== Dealix OS Config Validator ===\n")

    # --- os/*.yml ---
    print("-- Core OS YAML files --")
    for filename, checker in OS_YAML_CHECKS.items():
        path = OS_DIR / filename
        if not path.exists():
            err(f"File not found: {path.relative_to(REPO_ROOT)}")
            continue
        data = load_yaml(path)
        if data is not None:
            checker(data, path)

    # --- os/*.yml (remaining, parse-only) ---
    print("\n-- All os/*.yml (parse check) --")
    known = set(OS_YAML_CHECKS.keys())
    for yml_path in sorted(OS_DIR.glob("*.yml")):
        if yml_path.name in known:
            continue
        load_yaml(yml_path)

    # --- os/growth/*.yml ---
    print("\n-- Growth OS YAML files --")
    if GROWTH_DIR.exists():
        for filename, checker in GROWTH_YAML_CHECKS.items():
            path = GROWTH_DIR / filename
            if not path.exists():
                err(f"File not found: {path.relative_to(REPO_ROOT)}")
                continue
            data = load_yaml(path)
            if data is not None:
                checker(data, path)
        for yml_path in sorted(GROWTH_DIR.glob("*.yml")):
            if yml_path.name not in GROWTH_YAML_CHECKS:
                load_yaml(yml_path)
    else:
        warn("os/growth/ directory does not exist — skipping growth YAML checks")

    # --- os/schemas/*.json ---
    print("\n-- JSON Schemas --")
    if SCHEMAS_DIR.exists():
        for json_path in sorted(SCHEMAS_DIR.glob("*.json")):
            data = load_json(json_path)
            if data is not None:
                check_schema_json(data, json_path)
    else:
        warn("os/schemas/ directory does not exist — skipping schema checks")

    # --- os/growth/*.json ---
    print("\n-- Growth JSON Schemas --")
    if GROWTH_DIR.exists():
        for json_path in sorted(GROWTH_DIR.glob("*.json")):
            data = load_json(json_path)
            if data is not None:
                check_schema_json(data, json_path)

    # --- Cross-checks ---
    print("\n-- Cross-validation --")
    _cross_validate_offer_channel_consistency()

    # --- Summary ---
    print(f"\n=== Summary ===")
    print(f"  Errors:   {len(ERRORS)}")
    print(f"  Warnings: {len(WARNINGS)}")

    if ERRORS:
        print("\nFailed checks:")
        for e in ERRORS:
            print(f"  - {e}")
        return 1

    print("\nAll checks passed.")
    return 0


def _cross_validate_offer_channel_consistency() -> None:
    """Warn if best_channel values in sector offers do not match channel router."""
    offers_path = GROWTH_DIR / "GCC_SECTOR_OFFERS.yml" if GROWTH_DIR.exists() else None
    router_path = GROWTH_DIR / "CHANNEL_ROUTER.yml" if GROWTH_DIR.exists() else None

    if not offers_path or not offers_path.exists():
        return
    if not router_path or not router_path.exists():
        return

    offers_data = load_yaml(offers_path)
    router_data = load_yaml(router_path)
    if not offers_data or not router_data:
        return

    valid_channels = set((router_data.get("channels") or {}).keys())
    sectors = offers_data.get("sectors", {}) or {}
    for sector_key, sector_val in sectors.items():
        if not isinstance(sector_val, dict):
            continue
        pref_ch = sector_val.get("preferred_channel")
        if pref_ch and pref_ch not in valid_channels:
            warn(
                f"GCC_SECTOR_OFFERS.yml sector '{sector_key}' preferred_channel "
                f"'{pref_ch}' not found in CHANNEL_ROUTER.yml"
            )
    ok("Cross-validation: channel consistency checked")


if __name__ == "__main__":
    sys.exit(run())
