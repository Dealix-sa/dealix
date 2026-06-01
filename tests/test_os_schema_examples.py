"""Verify each JSON schema has required meta keys: $schema, title, type."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

OS_DIR = Path(__file__).resolve().parents[1] / "os"

SCHEMA_FILES = [
    "07_COMPANY_MEMORY_SCHEMA.json",
    "08_CLIENT_MEMORY_SCHEMA.json",
    "09_PROJECT_MEMORY_SCHEMA.json",
]

REQUIRED_KEYS = ["$schema", "title", "type"]


@pytest.mark.parametrize("filename", SCHEMA_FILES)
def test_schema_has_required_meta_keys(filename: str) -> None:
    path = OS_DIR / filename
    assert path.exists(), f"Missing schema file: {path}"
    data = json.loads(path.read_text())
    for key in REQUIRED_KEYS:
        assert key in data, f"Schema {filename} is missing required key '{key}'"


@pytest.mark.parametrize("filename", SCHEMA_FILES)
def test_schema_type_is_object(filename: str) -> None:
    path = OS_DIR / filename
    data = json.loads(path.read_text())
    assert data["type"] == "object", f"{filename}: top-level type must be 'object'"


@pytest.mark.parametrize("filename", SCHEMA_FILES)
def test_schema_has_properties(filename: str) -> None:
    path = OS_DIR / filename
    data = json.loads(path.read_text())
    assert "properties" in data, f"{filename}: must have 'properties' key"
    assert len(data["properties"]) > 0, f"{filename}: 'properties' must not be empty"


def test_company_schema_required_fields() -> None:
    path = OS_DIR / "07_COMPANY_MEMORY_SCHEMA.json"
    data = json.loads(path.read_text())
    required = data.get("required", [])
    assert "company_id" in required
    assert "status" in required


def test_client_schema_required_fields() -> None:
    path = OS_DIR / "08_CLIENT_MEMORY_SCHEMA.json"
    data = json.loads(path.read_text())
    required = data.get("required", [])
    assert "client_id" in required
    assert "status" in required


def test_project_schema_required_fields() -> None:
    path = OS_DIR / "09_PROJECT_MEMORY_SCHEMA.json"
    data = json.loads(path.read_text())
    required = data.get("required", [])
    assert "project_id" in required
    assert "status" in required
