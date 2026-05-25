"""Provenance check flags chains containing untrusted hops."""

from __future__ import annotations

from dealix.hermes.agent_comms.provenance_checker import ProvenanceHop, check


def test_provenance_flags_external_hop() -> None:
    chain = [
        ProvenanceHop(source="system", actor="orchestrator"),
        ProvenanceHop(source="approved_agent", actor="agent.sales"),
        ProvenanceHop(source="external", actor="webhook"),
    ]
    report = check(chain, minimum=50)
    assert report.trustworthy is False
    assert report.weakest_hop is not None
    assert report.weakest_hop.source == "external"
