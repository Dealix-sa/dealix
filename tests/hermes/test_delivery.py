from __future__ import annotations

from dealix.hermes.delivery import (
    ALL_PLAYBOOKS,
    AI_TRUST_KIT_PLAYBOOK,
    REVENUE_HUNTER_PLAYBOOK,
    run_quality_checklist,
)


def test_every_playbook_has_required_fields():
    for offer_id, pb in ALL_PLAYBOOKS.items():
        assert pb.offer_id == offer_id
        assert pb.name
        assert pb.inputs_required
        assert pb.steps
        assert pb.outputs
        assert pb.quality_gates


def test_quality_checklist_passes_with_all_evidence():
    evidence = {gate: True for gate in REVENUE_HUNTER_PLAYBOOK.quality_gates}
    res = run_quality_checklist(REVENUE_HUNTER_PLAYBOOK, evidence)
    assert res.passed is True


def test_quality_checklist_fails_with_missing_evidence():
    evidence = {gate: True for gate in AI_TRUST_KIT_PLAYBOOK.quality_gates}
    evidence["data_scope_defined"] = False
    res = run_quality_checklist(AI_TRUST_KIT_PLAYBOOK, evidence)
    assert res.passed is False
    assert "data_scope_defined" in res.failing_gates
