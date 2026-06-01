"""
YAML/JSON Parse Tests
=====================
Verifies all YAML and JSON files in os/ parse correctly.
Every config file must load as a dict without error.
"""

import pytest
import yaml
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OS_DIR = REPO_ROOT / "os"


def collect_yaml_files():
    """Collect all YAML files under os/ (recursively)."""
    return list(OS_DIR.rglob("*.yml"))


def collect_json_files():
    """Collect all JSON files under os/ (recursively, excluding examples for now)."""
    return list(OS_DIR.rglob("*.json"))


@pytest.mark.parametrize("yaml_file", collect_yaml_files(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_yaml_file_parses(yaml_file):
    """Each YAML file must parse without error and yield a dict."""
    with yaml_file.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data is not None, f"Empty YAML file: {yaml_file}"
    assert isinstance(data, dict), f"YAML must be a mapping: {yaml_file}"


@pytest.mark.parametrize("json_file", collect_json_files(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_json_file_parses(json_file):
    """Each JSON file must parse without error and yield a dict."""
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    assert data is not None, f"Empty JSON file: {json_file}"
    assert isinstance(data, dict), f"JSON must be a mapping: {json_file}"


class TestCoreYamlFiles:
    """Verify the canonical OS YAML files exist and have expected top-level keys."""

    def test_offers_yml_exists(self):
        path = OS_DIR / "03_OFFERS.yml"
        assert path.exists(), "03_OFFERS.yml must exist"
        with path.open() as f:
            data = yaml.safe_load(f)
        assert "offers" in data

    def test_markets_yml_exists(self):
        path = OS_DIR / "04_MARKETS.yml"
        assert path.exists(), "04_MARKETS.yml must exist"

    def test_scoring_yml_exists(self):
        path = OS_DIR / "05_SCORING.yml"
        assert path.exists(), "05_SCORING.yml must exist"
        with path.open() as f:
            data = yaml.safe_load(f)
        assert "scoring_dimensions" in data or "factor_weights" in data

    def test_approval_gates_yml_exists(self):
        path = OS_DIR / "06_APPROVAL_GATES.yml"
        assert path.exists(), "06_APPROVAL_GATES.yml must exist"
        with path.open() as f:
            data = yaml.safe_load(f)
        assert "gates" in data


class TestConfigYamlFiles:
    """Verify all os/config/ YAML files exist and have correct structure."""

    def _load(self, name: str) -> dict:
        path = OS_DIR / "config" / f"{name}.yml"
        assert path.exists(), f"Missing config: {name}.yml"
        with path.open() as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict)
        return data

    def test_countries_yml(self):
        data = self._load("countries")
        assert "countries" in data
        assert "ksa" in data["countries"]

    def test_sectors_yml(self):
        data = self._load("sectors")
        assert "sectors" in data
        assert "legal" in data["sectors"]
        assert "facilities_management" in data["sectors"]

    def test_channel_router_yml(self):
        data = self._load("channel-router")
        assert "sector_routes" in data
        assert "doctrine" in data

    def test_anti_ban_guardian_yml(self):
        data = self._load("anti-ban-guardian")
        assert "global" in data
        assert "email" in data

    def test_persuasion_yml(self):
        data = self._load("persuasion")
        assert "min_score_to_execute" in data
        assert data["min_score_to_execute"] == 82
        assert "scoring_rubric" in data

    def test_scoring_yml(self):
        data = self._load("scoring")
        assert "tier_thresholds" in data
        assert "A" in data["tier_thresholds"]

    def test_offers_config_yml(self):
        data = self._load("offers")
        assert "floor_prices_sar" in data
        assert data["floor_prices_sar"]["ai_workflow_audit"] == 5000

    def test_markets_config_yml(self):
        data = self._load("markets")
        assert "primary_markets" in data

    def test_buyer_personas_yml(self):
        data = self._load("buyer-personas")
        assert "personas" in data

    def test_quotas_yml(self):
        data = self._load("quotas")
        assert "daily_limits" in data
        assert "blocked_channels" in data

    def test_experiments_yml(self):
        data = self._load("experiments")
        assert "min_score_to_execute" in data or "experiment_types" in data


class TestSchemaJsonFiles:
    """Verify all os/schemas/ JSON files exist and have $schema field."""

    REQUIRED_SCHEMAS = [
        "company",
        "contact",
        "opportunity",
        "project",
        "persuasion-dossier",
        "draft-queue",
        "channel-job",
        "execution-log",
        "reply",
        "finance",
    ]

    @pytest.mark.parametrize("schema_name", REQUIRED_SCHEMAS)
    def test_schema_file_exists(self, schema_name):
        path = OS_DIR / "schemas" / f"{schema_name}.schema.json"
        assert path.exists(), f"Missing schema: {schema_name}.schema.json"
        with path.open() as f:
            data = json.load(f)
        assert "$schema" in data
        assert "title" in data
        assert "type" in data
