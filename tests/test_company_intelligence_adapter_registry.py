"""Tests for the Company Intelligence adapter registry.

Validates that:
1. Every entity in the ownership registry has a registry entry.
2. All normalize functions in __init__.__all__ are covered.
3. Active adapters have at least one function name.
4. Registry entries are frozen (immutable).
5. Coverage is deterministic across calls.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from dealix.company_intelligence.adapter_registry import (
    AdapterStatus,
    get_active_adapters,
    get_adapter_entry,
    get_adapter_registry,
    get_all_normalize_functions,
    validate_coverage,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
OWNERSHIP_PATH = REPO_ROOT / "dealix" / "registers" / "company_intelligence_entity_ownership.json"


class TestRegistryCoverage:
    """Verify the registry covers the entity ownership JSON."""

    def test_all_ownership_entities_have_entries(self) -> None:
        ownership = json.loads(OWNERSHIP_PATH.read_text(encoding="utf-8"))
        entity_names = [e["name"] for e in ownership["entities"]]
        missing = validate_coverage(entity_names)
        assert missing == [], f"Entities missing from adapter registry: {missing}"

    def test_registry_has_25_entities(self) -> None:
        registry = get_adapter_registry()
        assert len(registry) == 25

    def test_no_extra_entities_beyond_ownership(self) -> None:
        ownership = json.loads(OWNERSHIP_PATH.read_text(encoding="utf-8"))
        ownership_names = {e["name"] for e in ownership["entities"]}
        registry_names = set(get_adapter_registry().keys())
        extra = registry_names - ownership_names
        assert extra == set(), f"Registry has entities not in ownership: {extra}"


class TestActiveAdapters:
    """Verify active adapter entries."""

    def test_active_count(self) -> None:
        active = get_active_adapters()
        assert len(active) == 15

    def test_active_entries_have_functions(self) -> None:
        for entry in get_active_adapters():
            assert entry.adapter_functions, (
                f"{entry.entity_name}: active adapter has no functions"
            )

    def test_active_entries_have_module(self) -> None:
        for entry in get_active_adapters():
            assert entry.module, (
                f"{entry.entity_name}: active adapter has no module"
            )


class TestNormalizeFunctions:
    """Verify all normalize functions are accounted for."""

    def test_all_normalize_functions_in_init_all(self) -> None:
        import dealix.company_intelligence as ci

        init_normalize = {
            name for name in ci.__all__
            if name.startswith("normalize_")
        }
        registry_normalize = set(get_all_normalize_functions())
        missing = init_normalize - registry_normalize
        assert missing == set(), (
            f"normalize functions in __all__ but not in registry: {missing}"
        )

    def test_normalize_function_count(self) -> None:
        functions = get_all_normalize_functions()
        assert len(functions) == 18

    def test_normalize_functions_sorted(self) -> None:
        functions = get_all_normalize_functions()
        assert functions == sorted(functions)


class TestEntryProperties:
    """Verify adapter entry invariants."""

    def test_entries_are_frozen(self) -> None:
        entry = get_adapter_entry("Company")
        assert entry is not None
        with pytest.raises(AttributeError):
            entry.entity_name = "tampered"  # type: ignore[misc]

    def test_lookup_returns_none_for_unknown(self) -> None:
        assert get_adapter_entry("NonExistent") is None

    @pytest.mark.parametrize("entity_name", [
        "Tenant", "Persona", "PartnershipOpportunity", "DepartmentPlan",
    ])
    def test_no_operational_source_has_no_functions(self, entity_name: str) -> None:
        entry = get_adapter_entry(entity_name)
        assert entry is not None
        assert entry.status == AdapterStatus.NO_OPERATIONAL_SOURCE
        assert entry.adapter_functions == ()

    @pytest.mark.parametrize("entity_name", [
        "OutcomeEvent", "DailyCommand", "CompanyBrain",
    ])
    def test_builder_only_has_no_functions(self, entity_name: str) -> None:
        entry = get_adapter_entry(entity_name)
        assert entry is not None
        assert entry.status == AdapterStatus.BUILDER_ONLY
        assert entry.adapter_functions == ()
        assert entry.notes  # builder-only should explain why


class TestDeterminism:
    """Verify registry is deterministic across calls."""

    def test_same_registry_on_repeated_calls(self) -> None:
        r1 = get_adapter_registry()
        r2 = get_adapter_registry()
        assert r1 is r2  # same object (lazy singleton)

    def test_same_functions_on_repeated_calls(self) -> None:
        f1 = get_all_normalize_functions()
        f2 = get_all_normalize_functions()
        assert f1 == f2
