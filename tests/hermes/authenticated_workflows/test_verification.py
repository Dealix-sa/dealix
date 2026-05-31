"""verify_workflow returns False with reasons when any attestation is missing."""

from __future__ import annotations

from dealix.hermes.authenticated_workflows.context_attestation import (
    clear_registry as clear_ctx,
    register_approved_context,
    attest_context,
)
from dealix.hermes.authenticated_workflows.data_attestation import DataBoundary, attest_data
from dealix.hermes.authenticated_workflows.intent_proof import sign_intent
from dealix.hermes.authenticated_workflows.tool_attestation import (
    clear_registry as clear_tool,
    register_tool,
    attest_tool,
)
from dealix.hermes.authenticated_workflows.verification import verify_workflow
from dealix.hermes.authenticated_workflows.workflow_signature import sign_workflow


def test_verify_workflow_collects_all_failures() -> None:
    clear_ctx()
    clear_tool()
    register_approved_context("v1", {"a": 1})
    register_tool("crm", "2.0.0")
    proof = sign_intent("close_deal", actor="agent.sales")
    ctx = attest_context("v1", {"a": 1})
    tool = attest_tool("crm", "1.0.0")
    data = attest_data(DataBoundary("ws_1", frozenset({"deals.write"})), "deals.write", "internal")
    ok, reasons = verify_workflow(sign_workflow(proof, ctx, tool, data))
    assert ok is False
    assert any("tool" in r for r in reasons)
