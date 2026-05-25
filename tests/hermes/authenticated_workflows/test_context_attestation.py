"""Verify context attestation flags only approved policy_version hashes."""

from __future__ import annotations

from dealix.hermes.authenticated_workflows.context_attestation import (
    attest_context,
    clear_registry,
    register_approved_context,
)


def test_context_attestation_matches_only_when_hash_matches() -> None:
    clear_registry()
    packet = {"region": "SA", "scope": "delivery"}
    register_approved_context("v1", packet)
    assert attest_context("v1", packet).approved is True
    assert attest_context("v1", {**packet, "scope": "billing"}).approved is False
