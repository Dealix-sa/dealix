"""
OS Config Loader
================
Reads YAML and JSON config files from os/ directory.
Raises clear errors for missing or malformed files.
"""

from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[2]
OS_DIR = ROOT / "os"


def load_yaml(relative_path: str) -> dict:
    """Load a YAML file from OS_DIR. relative_path is relative to os/."""
    path = OS_DIR / relative_path
    if not path.exists():
        raise FileNotFoundError(f"Missing OS config: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        raise ValueError(f"OS config is empty: {path}")
    if not isinstance(data, dict):
        raise ValueError(f"OS config must be a mapping (dict), got {type(data).__name__}: {path}")
    return data


def load_json(relative_path: str) -> dict:
    """Load a JSON file from OS_DIR. relative_path is relative to os/."""
    path = OS_DIR / relative_path
    if not path.exists():
        raise FileNotFoundError(f"Missing OS schema: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"OS JSON must be a mapping (dict): {path}")
    return data


# ── Canonical loaders for each OS file ──────────────────────────────────────

def load_offers() -> dict:
    return load_yaml("03_OFFERS.yml")


def load_markets() -> dict:
    return load_yaml("04_MARKETS.yml")


def load_scoring() -> dict:
    return load_yaml("05_SCORING.yml")


def load_approval_gates() -> dict:
    return load_yaml("06_APPROVAL_GATES.yml")


def load_company_memory_schema() -> dict:
    return load_json("07_COMPANY_MEMORY_SCHEMA.json")


def load_client_memory_schema() -> dict:
    return load_json("08_CLIENT_MEMORY_SCHEMA.json")


def load_project_memory_schema() -> dict:
    return load_json("09_PROJECT_MEMORY_SCHEMA.json")


# ── Config subdir loaders ────────────────────────────────────────────────────

def load_config(name: str) -> dict:
    """Load from os/config/<name>.yml"""
    return load_yaml(f"config/{name}.yml")


def load_countries() -> dict:
    return load_config("countries")


def load_sectors() -> dict:
    return load_config("sectors")


def load_channel_router_config() -> dict:
    return load_config("channel-router")


def load_anti_ban_config() -> dict:
    return load_config("anti-ban-guardian")


def load_persuasion_config() -> dict:
    return load_config("persuasion")


def load_scoring_config() -> dict:
    return load_config("scoring")


def load_offers_config() -> dict:
    return load_config("offers")


def load_markets_config() -> dict:
    return load_config("markets")


def load_buyer_personas() -> dict:
    return load_config("buyer-personas")


def load_quotas() -> dict:
    return load_config("quotas")


def load_experiments() -> dict:
    return load_config("experiments")


# ── Schema loaders ───────────────────────────────────────────────────────────

def load_schema(name: str) -> dict:
    """Load from os/schemas/<name>.schema.json"""
    return load_json(f"schemas/{name}.schema.json")


def load_all_configs() -> dict:
    """Load all OS configs and return summary. Used by validate command."""
    results = {}
    yaml_files = list((OS_DIR).glob("*.yml")) + list((OS_DIR / "config").glob("*.yml"))
    json_files = list(OS_DIR.glob("*.json")) + list((OS_DIR / "schemas").glob("*.json"))
    growth_yamls = list((OS_DIR / "growth").glob("*.yml")) if (OS_DIR / "growth").exists() else []

    for f in yaml_files + growth_yamls:
        try:
            path = OS_DIR / f
            with path.open("r", encoding="utf-8") as fh:
                yaml.safe_load(fh)
            results[str(f.relative_to(ROOT))] = {"status": "ok", "type": "yaml"}
        except Exception as e:
            results[str(f)] = {"status": "error", "error": str(e)}

    for f in json_files:
        try:
            path = OS_DIR / f
            with path.open("r", encoding="utf-8") as fh:
                json.load(fh)
            results[str(f.relative_to(ROOT))] = {"status": "ok", "type": "json"}
        except Exception as e:
            results[str(f)] = {"status": "error", "error": str(e)}

    return results
