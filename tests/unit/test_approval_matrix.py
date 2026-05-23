"""ApprovalMatrix classifies actions per the YAML register."""
from __future__ import annotations

from dealix.trust.approval_matrix import ApprovalMatrix


def test_blocks_doctrine_violations():
    m = ApprovalMatrix.from_register()
    assert m.is_blocked("auto_send_external_outbound")


def test_founder_required_for_outbound():
    m = ApprovalMatrix.from_register()
    assert m.requires_founder("send_outbound_message")


def test_ops_manager_can_tune_thresholds():
    m = ApprovalMatrix.from_register()
    assert m.classify("update_lead_scoring_threshold").approval_class == "ops_manager"


def test_default_class_is_founder_for_unknown():
    m = ApprovalMatrix(register={})
    assert m.classify("frobulate_the_widget").approval_class == "founder"
