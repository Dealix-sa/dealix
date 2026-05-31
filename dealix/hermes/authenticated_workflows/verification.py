"""Aggregate verification of a Workflow Trust Object."""

from __future__ import annotations

from .intent_proof import verify_intent
from .workflow_signature import WorkflowTrustObject, signature_valid


def verify_workflow(obj: WorkflowTrustObject) -> tuple[bool, list[str]]:
    """Verify every attestation in a WorkflowTrustObject, returning (ok, reasons)."""
    reasons: list[str] = []
    if not verify_intent(obj.intent):
        reasons.append("intent signature invalid")
    if not obj.context.approved:
        reasons.append(f"context not approved for policy_version={obj.context.policy_version}")
    if not obj.tool.approved:
        reasons.append(f"tool {obj.tool.tool_name}@{obj.tool.tool_version} not on registry")
    if not obj.data.approved:
        reasons.append(f"data scope rejected: {obj.data.reason}")
    if not signature_valid(obj):
        reasons.append("workflow trust object signature invalid")
    return (len(reasons) == 0, reasons)
