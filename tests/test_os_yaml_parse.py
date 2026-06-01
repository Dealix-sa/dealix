"""Verify all OS YAML and JSON config files parse without error."""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

OS_DIR = Path(__file__).resolve().parents[1] / "os"

YAML_FILES = [
    "03_OFFERS.yml",
    "04_MARKETS.yml",
    "05_SCORING.yml",
    "06_APPROVAL_GATES.yml",
]

JSON_FILES = [
    "07_COMPANY_MEMORY_SCHEMA.json",
    "08_CLIENT_MEMORY_SCHEMA.json",
    "09_PROJECT_MEMORY_SCHEMA.json",
]


@pytest.mark.parametrize("filename", YAML_FILES)
def test_yaml_file_exists_and_parses(filename: str) -> None:
    path = OS_DIR / filename
    assert path.exists(), f"Missing file: {path}"
    data = yaml.safe_load(path.read_text())
    assert data is not None, f"Empty or null YAML: {filename}"


@pytest.mark.parametrize("filename", JSON_FILES)
def test_json_file_exists_and_parses(filename: str) -> None:
    path = OS_DIR / filename
    assert path.exists(), f"Missing file: {path}"
    data = json.loads(path.read_text())
    assert isinstance(data, dict), f"Expected dict at top level in {filename}"


def test_offers_yaml_has_offers_key() -> None:
    data = yaml.safe_load((OS_DIR / "03_OFFERS.yml").read_text())
    assert "offers" in data, "03_OFFERS.yml must have top-level 'offers' key"


def test_scoring_yaml_has_dimensions() -> None:
    data = yaml.safe_load((OS_DIR / "05_SCORING.yml").read_text())
    assert "scoring_dimensions" in data
    assert "decision_thresholds" in data


def test_approval_gates_has_gates_key() -> None:
    data = yaml.safe_load((OS_DIR / "06_APPROVAL_GATES.yml").read_text())
    assert "gates" in data, "06_APPROVAL_GATES.yml must have 'gates' key"
