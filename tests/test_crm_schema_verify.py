"""CRM schema is the canonical 14-stage, record-only pipeline."""

from __future__ import annotations

from _commercial_common import load_config
from _launch_util import ROOT
from commercial_crm_schema_verify import EXPECTED_STAGES, verify


def test_schema_verifies_clean():
    assert verify() == []


def test_canonical_stages():
    schema = load_config("crm_pipeline_schema.json")
    assert schema["stages"] == EXPECTED_STAGES
    assert len(EXPECTED_STAGES) == 14


def test_record_only_flags():
    schema = load_config("crm_pipeline_schema.json")
    assert schema["no_external_send"] is True
    assert schema["no_crm_push_send"] is True


def test_transitions_reference_valid_stages():
    schema = load_config("crm_pipeline_schema.json")
    valid = set(schema["stages"])
    for src, dests in schema["allowed_transitions"].items():
        assert src in valid
        for d in dests:
            assert d in valid
