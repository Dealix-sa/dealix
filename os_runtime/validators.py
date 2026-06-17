"""Validate that all OS config files exist and parse correctly."""
from __future__ import annotations

from pathlib import Path
import yaml
import json

OS_DIR = Path(__file__).resolve().parents[1] / "os"

_YAML_FILES: list[str] = [
    "03_OFFERS.yml",
    "04_MARKETS.yml",
    "05_SCORING.yml",
    "06_APPROVAL_GATES.yml",
]

_JSON_FILES: list[str] = [
    "07_COMPANY_MEMORY_SCHEMA.json",
    "08_CLIENT_MEMORY_SCHEMA.json",
    "09_PROJECT_MEMORY_SCHEMA.json",
]


def validate_configs() -> dict[str, str]:
    """Return ``{filename: "OK" | "ERROR: ..."}`` for every OS config file."""
    results: dict[str, str] = {}

    for filename in _YAML_FILES:
        path = OS_DIR / filename
        try:
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            yaml.safe_load(path.read_text())
            results[filename] = "OK"
        except Exception as exc:  # noqa: BLE001
            results[filename] = f"ERROR: {exc}"

    for filename in _JSON_FILES:
        path = OS_DIR / filename
        try:
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            json.loads(path.read_text())
            results[filename] = "OK"
        except Exception as exc:  # noqa: BLE001
            results[filename] = f"ERROR: {exc}"

    return results


def validate_all() -> bool:
    """Return True only if every OS config file validates without error."""
    return all(v == "OK" for v in validate_configs().values())
