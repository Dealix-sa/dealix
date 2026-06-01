#!/usr/bin/env python3
"""
validate_os_configs.py
======================
Validates all YAML and JSON config files in os/ directory.
Exits 0 on success, 1 on any error.

Usage:
    python scripts/validate_os_configs.py
"""

import sys
import json
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OS_DIR = REPO_ROOT / "os"

# Required YAML files (relative to os/)
REQUIRED_YAML = [
    "03_OFFERS.yml",
    "04_MARKETS.yml",
    "05_SCORING.yml",
    "06_APPROVAL_GATES.yml",
    "config/countries.yml",
    "config/sectors.yml",
    "config/channel-router.yml",
    "config/anti-ban-guardian.yml",
    "config/persuasion.yml",
    "config/scoring.yml",
    "config/offers.yml",
    "config/markets.yml",
    "config/buyer-personas.yml",
    "config/quotas.yml",
    "config/experiments.yml",
    "config/approval-gates.yml",
]

# Required JSON files (relative to os/)
REQUIRED_JSON = [
    "07_COMPANY_MEMORY_SCHEMA.json",
    "08_CLIENT_MEMORY_SCHEMA.json",
    "09_PROJECT_MEMORY_SCHEMA.json",
    "schemas/company.schema.json",
    "schemas/contact.schema.json",
    "schemas/opportunity.schema.json",
    "schemas/project.schema.json",
    "schemas/persuasion-dossier.schema.json",
    "schemas/draft-queue.schema.json",
    "schemas/channel-job.schema.json",
    "schemas/execution-log.schema.json",
    "schemas/reply.schema.json",
    "schemas/finance.schema.json",
]

# Semantic checks: key must exist in loaded YAML/JSON
SEMANTIC_CHECKS = {
    "03_OFFERS.yml": {"key": "offers", "type": "yaml"},
    "06_APPROVAL_GATES.yml": {"key": "gates", "type": "yaml"},
    "config/countries.yml": {"key": "countries", "type": "yaml"},
    "config/sectors.yml": {"key": "sectors", "type": "yaml"},
    "config/persuasion.yml": {"key": "min_score_to_execute", "type": "yaml"},
    "config/scoring.yml": {"key": "tier_thresholds", "type": "yaml"},
    "config/quotas.yml": {"key": "daily_limits", "type": "yaml"},
}


def validate_yaml(path: Path) -> tuple[bool, str]:
    """Validate a YAML file. Returns (ok, error_message)."""
    if not path.exists():
        return False, f"Missing: {path.relative_to(REPO_ROOT)}"
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data is None:
            return False, f"Empty file: {path.relative_to(REPO_ROOT)}"
        if not isinstance(data, dict):
            return False, f"Must be a YAML mapping: {path.relative_to(REPO_ROOT)}"
        return True, ""
    except yaml.YAMLError as e:
        return False, f"YAML parse error in {path.relative_to(REPO_ROOT)}: {e}"


def validate_json(path: Path) -> tuple[bool, str]:
    """Validate a JSON file. Returns (ok, error_message)."""
    if not path.exists():
        return False, f"Missing: {path.relative_to(REPO_ROOT)}"
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return False, f"Must be a JSON object: {path.relative_to(REPO_ROOT)}"
        return True, ""
    except json.JSONDecodeError as e:
        return False, f"JSON parse error in {path.relative_to(REPO_ROOT)}: {e}"


def semantic_check(relative_path: str, check: dict) -> tuple[bool, str]:
    """Check that a required top-level key exists in a config."""
    path = OS_DIR / relative_path
    if not path.exists():
        return False, f"File missing for semantic check: {relative_path}"

    try:
        if check["type"] == "yaml":
            with path.open() as f:
                data = yaml.safe_load(f)
        else:
            with path.open() as f:
                data = json.load(f)

        if check["key"] not in data:
            return False, f"Missing required key '{check['key']}' in {relative_path}"
        return True, ""
    except Exception as e:
        return False, f"Error checking {relative_path}: {e}"


def main() -> int:
    errors = []
    warnings = []
    ok_count = 0

    print("=" * 60)
    print("Dealix OS Config Validation")
    print("=" * 60)

    # Validate required YAML files
    print("\n[YAML Files]")
    for rel_path in REQUIRED_YAML:
        path = OS_DIR / rel_path
        ok, err = validate_yaml(path)
        if ok:
            print(f"  [OK]   {rel_path}")
            ok_count += 1
        else:
            print(f"  [FAIL] {err}")
            errors.append(err)

    # Validate required JSON files
    print("\n[JSON Files]")
    for rel_path in REQUIRED_JSON:
        path = OS_DIR / rel_path
        ok, err = validate_json(path)
        if ok:
            print(f"  [OK]   {rel_path}")
            ok_count += 1
        else:
            print(f"  [FAIL] {err}")
            errors.append(err)

    # Semantic checks
    print("\n[Semantic Checks]")
    for rel_path, check in SEMANTIC_CHECKS.items():
        ok, err = semantic_check(rel_path, check)
        if ok:
            print(f"  [OK]   {rel_path} has key '{check['key']}'")
        else:
            print(f"  [FAIL] {err}")
            errors.append(err)

    # Scan all YAML/JSON in os/ for additional files
    print("\n[Additional File Scan]")
    all_yaml = list(OS_DIR.rglob("*.yml"))
    all_json = list(OS_DIR.rglob("*.json"))

    for f in all_yaml:
        rel = str(f.relative_to(OS_DIR))
        if rel not in REQUIRED_YAML:
            ok, err = validate_yaml(f)
            if ok:
                print(f"  [OK]   {rel} (extra)")
                ok_count += 1
            else:
                print(f"  [WARN] {err}")
                warnings.append(err)

    for f in all_json:
        rel = str(f.relative_to(OS_DIR))
        if rel not in REQUIRED_JSON:
            ok, err = validate_json(f)
            if ok:
                print(f"  [OK]   {rel} (extra)")
                ok_count += 1
            else:
                print(f"  [WARN] {err}")
                warnings.append(err)

    # Summary
    print("\n" + "=" * 60)
    print(f"Results: {ok_count} OK, {len(errors)} errors, {len(warnings)} warnings")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  - {e}")
        print("\nFix all errors before proceeding.")
        return 1

    if warnings:
        print("\nWarnings (non-blocking):")
        for w in warnings:
            print(f"  - {w}")

    print("\nAll required OS configs validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
