from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/verify_company_intelligence_entity_ownership.py"
SPEC = importlib.util.spec_from_file_location("entity_ownership_verifier", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_registry_is_valid() -> None:
    data = MODULE.load_registry()
    assert MODULE.validate_registry(data) == []


def test_registry_covers_required_execution_spine() -> None:
    data = MODULE.load_registry()
    names = {entity["name"] for entity in data["entities"]}
    assert MODULE.REQUIRED_CANONICAL_ENTITIES <= names


def test_external_tools_cannot_be_source_of_truth() -> None:
    data = MODULE.load_registry()
    assert all(entity["external_source_of_truth_allowed"] is False for entity in data["entities"])


def test_parallel_aliases_are_unique_and_noncanonical() -> None:
    data = MODULE.load_registry()
    names = {entity["name"] for entity in data["entities"]}
    aliases = [alias for entity in data["entities"] for alias in entity["forbidden_parallel_names"]]
    assert len(aliases) == len(set(aliases))
    assert names.isdisjoint(aliases)


def test_duplicate_entity_is_rejected() -> None:
    data = MODULE.load_registry()
    data["entities"].append(dict(data["entities"][0]))
    errors = MODULE.validate_registry(data)
    assert any("duplicate canonical entity" in error for error in errors)
