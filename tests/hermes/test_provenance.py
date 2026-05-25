from __future__ import annotations

from dealix.hermes.provenance import (
    ProvenanceLedger,
    TrustLevel,
    build_lineage,
    build_source_metadata,
    score_trust_level,
    validate_for_downstream,
)


def test_score_trust_level_defaults_to_untrusted():
    assert score_trust_level("random_external_blog") == TrustLevel.UNTRUSTED


def test_internal_source_is_trusted():
    assert score_trust_level("dealix_internal") == TrustLevel.TRUSTED


def test_ledger_records_use_and_sanitization():
    ledger = ProvenanceLedger()
    meta = build_source_metadata("external_website", "scraper_v1")
    obj = ledger.append("tool_output", meta, "scraper_v1", payload_preview="hello")
    ledger.record_use(obj.object_id, "proposal_factory")
    ledger.mark_sanitized(obj.object_id, "stripped instructions")
    fetched = ledger.get(obj.object_id)
    assert "proposal_factory" in fetched.used_by
    assert fetched.sanitized is True


def test_untrusted_cannot_act_as_instructions():
    meta = build_source_metadata("external_website", "scraper_v1")
    ledger = ProvenanceLedger()
    obj = ledger.append("tool_output", meta, "scraper_v1")
    verdict = validate_for_downstream(
        obj,
        downstream_agent_id="proposal_factory",
        downstream_risk_band="medium",
        will_be_used_as_instruction=True,
    )
    assert verdict.allowed is False


def test_untrusted_data_requires_sanitization_for_high_risk():
    meta = build_source_metadata("external_website", "scraper_v1")
    ledger = ProvenanceLedger()
    obj = ledger.append("tool_output", meta, "scraper_v1")
    verdict = validate_for_downstream(
        obj,
        downstream_agent_id="proposal_factory",
        downstream_risk_band="high",
        will_be_used_as_instruction=False,
    )
    assert verdict.allowed is True
    assert verdict.must_sanitize is True


def test_lineage_traversal():
    g = build_lineage([("a", "b"), ("b", "c"), ("a", "d")])
    assert g.ancestors("c") == {"a", "b"}
    assert g.descendants("a") == {"b", "c", "d"}
