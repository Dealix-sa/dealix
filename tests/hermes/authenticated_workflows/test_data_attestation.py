"""Verify data scope attestation enforces declared workspace boundary."""

from __future__ import annotations

from dealix.hermes.authenticated_workflows.data_attestation import DataBoundary, attest_data


def test_data_attestation_rejects_out_of_scope() -> None:
    boundary = DataBoundary(
        workspace_id="ws_1",
        allowed_scopes=frozenset({"deals.read"}),
        allowed_classifications=frozenset({"public", "internal"}),
    )
    assert attest_data(boundary, "deals.read", "internal").approved is True
    assert attest_data(boundary, "billing.read", "internal").approved is False
    assert attest_data(boundary, "deals.read", "restricted").approved is False
