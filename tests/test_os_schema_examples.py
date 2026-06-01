"""
test_os_schema_examples.py — Validate os/ JSON schemas are well-formed
and that any example payloads conform to the declared schemas.

Doctrine: every schema shipped in os/ must be parseable and structurally valid.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
OS_DIR = REPO_ROOT / "os"
GROWTH_DIR = OS_DIR / "growth"
SCHEMAS_DIR = OS_DIR / "schemas"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _json_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(directory.glob("*.json"))


# ---------------------------------------------------------------------------
# All JSON files parse cleanly
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "json_path",
    _json_files(SCHEMAS_DIR) + _json_files(GROWTH_DIR) + _json_files(OS_DIR),
    ids=lambda p: p.relative_to(REPO_ROOT).as_posix(),
)
def test_json_parses_cleanly(json_path: Path) -> None:
    """Every os JSON file must parse without error."""
    data = _load_json(json_path)
    assert data is not None
    assert isinstance(data, dict)


# ---------------------------------------------------------------------------
# os/07_COMPANY_MEMORY_SCHEMA.json
# ---------------------------------------------------------------------------


class TestCompanyMemorySchema:
    path = OS_DIR / "07_COMPANY_MEMORY_SCHEMA.json"

    def test_file_exists(self) -> None:
        assert self.path.exists(), "07_COMPANY_MEMORY_SCHEMA.json is missing"

    def test_has_required_structure(self) -> None:
        data = _load_json(self.path)
        # Must have either 'type'/'properties' (JSON Schema) or 'fields' dict
        has_schema_structure = "type" in data or "properties" in data or "fields" in data
        assert has_schema_structure, (
            "07_COMPANY_MEMORY_SCHEMA.json must define type, properties, or fields"
        )


# ---------------------------------------------------------------------------
# os/08_CLIENT_MEMORY_SCHEMA.json
# ---------------------------------------------------------------------------


class TestClientMemorySchema:
    path = OS_DIR / "08_CLIENT_MEMORY_SCHEMA.json"

    def test_file_exists(self) -> None:
        assert self.path.exists(), "08_CLIENT_MEMORY_SCHEMA.json is missing"

    def test_has_required_structure(self) -> None:
        data = _load_json(self.path)
        has_schema_structure = "type" in data or "properties" in data or "fields" in data
        assert has_schema_structure


# ---------------------------------------------------------------------------
# os/09_PROJECT_MEMORY_SCHEMA.json
# ---------------------------------------------------------------------------


class TestProjectMemorySchema:
    path = OS_DIR / "09_PROJECT_MEMORY_SCHEMA.json"

    def test_file_exists(self) -> None:
        assert self.path.exists(), "09_PROJECT_MEMORY_SCHEMA.json is missing"

    def test_has_required_structure(self) -> None:
        data = _load_json(self.path)
        has_schema_structure = "type" in data or "properties" in data or "fields" in data
        assert has_schema_structure


# ---------------------------------------------------------------------------
# Growth schemas (conditional)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    not (GROWTH_DIR / "PERSUASION_DOSSIER_SCHEMA.json").exists(),
    reason="PERSUASION_DOSSIER_SCHEMA.json not yet created",
)
class TestPersuasionDossierSchema:
    path = GROWTH_DIR / "PERSUASION_DOSSIER_SCHEMA.json"

    def test_is_json_schema_draft07(self) -> None:
        data = _load_json(self.path)
        assert "$schema" in data
        assert "draft-07" in data["$schema"]

    def test_has_title_and_type(self) -> None:
        data = _load_json(self.path)
        assert data.get("title") == "PersuasionDossier"
        assert data.get("type") == "object"

    def test_required_fields_present_in_schema(self) -> None:
        data = _load_json(self.path)
        required = set(data.get("required", []))
        mandatory = {
            "company",
            "country",
            "sector",
            "buyer_persona",
            "likely_pain",
            "trust_angle",
            "best_offer",
            "best_channel",
            "message_pack",
        }
        missing = mandatory - required
        assert not missing, f"PersuasionDossier schema missing required fields: {missing}"

    def test_country_enum_includes_gcc(self) -> None:
        data = _load_json(self.path)
        props = data.get("properties", {})
        country_enum = props.get("country", {}).get("enum", [])
        gcc = {"SA", "AE", "KW", "QA", "BH", "OM"}
        missing = gcc - set(country_enum)
        assert not missing, f"country enum missing GCC codes: {missing}"

    def test_persuasion_score_bounded(self) -> None:
        data = _load_json(self.path)
        props = data.get("properties", {})
        score_prop = props.get("persuasion_score", {})
        assert score_prop.get("minimum") == 0
        assert score_prop.get("maximum") == 100

    def test_example_dossier_matches_schema(self) -> None:
        """Validate a minimal well-formed dossier against the required fields."""
        try:
            import jsonschema
        except ImportError:
            pytest.skip("jsonschema not installed")

        data = _load_json(self.path)
        example = {
            "company": "ACME FM Co",
            "country": "SA",
            "sector": "Facilities Management",
            "buyer_persona": "Operations Director",
            "likely_pain": ["Manual SLA tracking"],
            "trust_angle": "Workflow audit with proof",
            "best_offer": "ai_workflow_audit",
            "best_channel": "Email",
            "message_pack": {
                "subject_line": "نظام AI لإدارة SLA",
                "opening_ar": "مرحباً",
                "opening_en": "Hello",
                "value_prop_ar": "نوفر لكم الوقت",
                "value_prop_en": "We save you time",
                "cta_ar": "حدد موعداً",
                "cta_en": "Book a call",
            },
        }
        jsonschema.validate(example, data)


@pytest.mark.skipif(
    not (GROWTH_DIR / "DRAFT_QUEUE_SCHEMA.json").exists(),
    reason="DRAFT_QUEUE_SCHEMA.json not yet created",
)
class TestDraftQueueSchema:
    path = GROWTH_DIR / "DRAFT_QUEUE_SCHEMA.json"

    def test_is_valid_json_schema(self) -> None:
        data = _load_json(self.path)
        assert "type" in data
        assert data["type"] == "object"

    def test_has_core_draft_fields(self) -> None:
        data = _load_json(self.path)
        required = set(data.get("required", []))
        core = {"draft_id", "company_id", "channel", "offer_tier", "status"}
        missing = core - required
        assert not missing, f"DraftQueue schema missing required fields: {missing}"

    def test_status_enum_is_defined(self) -> None:
        data = _load_json(self.path)
        props = data.get("properties", {})
        status_prop = props.get("status", {})
        assert "enum" in status_prop, "status field must define enum values"
        assert len(status_prop["enum"]) >= 3, "status must have at least 3 enum values"

    def test_requires_approval_is_boolean(self) -> None:
        data = _load_json(self.path)
        props = data.get("properties", {})
        approval_prop = props.get("requires_approval", {})
        assert approval_prop.get("type") == "boolean"
