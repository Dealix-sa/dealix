"""
Schema + Examples Validation Tests
====================================
Validates example JSON files against their schemas.
"""

import pytest
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OS_DIR = REPO_ROOT / "os"

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


def load_schema(name: str) -> dict:
    path = OS_DIR / "schemas" / f"{name}.schema.json"
    with path.open() as f:
        return json.load(f)


def load_example(name: str) -> dict:
    path = OS_DIR / "examples" / name
    with path.open() as f:
        return json.load(f)


class TestSchemaStructure:
    """Test that all schemas have valid structure."""

    REQUIRED_SCHEMAS = [
        "company", "contact", "opportunity", "project",
        "persuasion-dossier", "draft-queue", "channel-job",
        "execution-log", "reply", "finance",
    ]

    @pytest.mark.parametrize("schema_name", REQUIRED_SCHEMAS)
    def test_schema_has_required_fields(self, schema_name):
        schema = load_schema(schema_name)
        assert "$schema" in schema
        assert "title" in schema
        assert "type" in schema
        assert schema["type"] == "object"

    @pytest.mark.parametrize("schema_name", REQUIRED_SCHEMAS)
    def test_schema_has_properties(self, schema_name):
        schema = load_schema(schema_name)
        assert "properties" in schema

    def test_company_schema_required_fields(self):
        schema = load_schema("company")
        required = schema.get("required", [])
        assert "company" in required
        assert "country" in required
        assert "sector" in required

    def test_opportunity_schema_has_stage_enum(self):
        schema = load_schema("opportunity")
        stage_prop = schema["properties"]["stage"]
        assert "enum" in stage_prop
        assert "lead" in stage_prop["enum"]
        assert "won" in stage_prop["enum"]

    def test_persuasion_dossier_schema_required_fields(self):
        schema = load_schema("persuasion-dossier")
        required = schema.get("required", [])
        for field in ["company", "country", "language", "sector", "buyer",
                      "likely_pain", "best_offer", "best_channel",
                      "persuasion_score", "message_pack"]:
            assert field in required, f"Missing required field: {field}"

    def test_persuasion_score_is_bounded(self):
        schema = load_schema("persuasion-dossier")
        score_prop = schema["properties"]["persuasion_score"]
        assert score_prop.get("minimum") == 0
        assert score_prop.get("maximum") == 100

    def test_execution_log_pii_blocked(self):
        """execution-log must have pii_present with default false."""
        schema = load_schema("execution-log")
        pii_prop = schema["properties"]["pii_present"]
        assert pii_prop.get("default") is False


@pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not installed")
class TestExamplesAgainstSchemas:
    """Validate example files against schemas."""

    def test_company_fm_ksa_valid(self):
        example_path = OS_DIR / "examples" / "company_fm_ksa.json"
        if not example_path.exists():
            pytest.skip("Example file not yet created")
        schema = load_schema("company")
        data = json.loads(example_path.read_text())
        jsonschema.validate(data, schema)

    def test_company_legal_ksa_valid(self):
        example_path = OS_DIR / "examples" / "company_legal_ksa.json"
        if not example_path.exists():
            pytest.skip("Example file not yet created")
        schema = load_schema("company")
        data = json.loads(example_path.read_text())
        jsonschema.validate(data, schema)

    def test_persuasion_dossier_example_valid(self):
        example_path = OS_DIR / "examples" / "persuasion_dossier_legal.json"
        if not example_path.exists():
            pytest.skip("Example file not yet created")
        schema = load_schema("persuasion-dossier")
        data = json.loads(example_path.read_text())
        jsonschema.validate(data, schema)
