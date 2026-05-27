"""Audit-chain doctrine — the sprint persists the Proof Pack and emits
an auditable evidence chain.

Covers the rung 0-1 delivery-finish work: ``run_sprint`` must write a
``proof_pack_assembled`` proof-ledger entry, emit ``proof_pack_assembled``
and ``output_delivered`` audit events, and surface — never swallow — a
persistence failure (doctrine ``no_silent_failures`` / ``no_fake_proof``).
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.auditability_os import audit_event as audit_mod
from auto_client_acquisition.auditability_os.audit_event import list_events
from auto_client_acquisition.auditability_os.evidence_chain import build_chain
from auto_client_acquisition.delivery_factory.delivery_sprint import run_sprint
from auto_client_acquisition.proof_ledger import file_backend
from auto_client_acquisition.proof_ledger.factory import (
    get_default_ledger,
    reset_default_ledger,
)

_DEMO_CSV = (
    "company_name,sector,city,relationship_status,last_interaction,notes\n"
    "شركة الواحة,b2b_services,Riyadh,warm,2026-04-12,clean fit\n"
    "Madar Logistics,logistics,Jeddah,warm,2026-04-22,past pilot\n"
    "Rawabi,real_estate,Riyadh,cold,2026-02-18,stale\n"
)

_GOOD_PASSPORT = {
    "source_id": "SRC-DEMO-1",
    "source_type": "client_upload",
    "owner": "client",
    "allowed_use": ("internal_analysis", "scoring"),
    "contains_pii": False,
    "sensitivity": "low",
    "ai_access_allowed": True,
    "external_use_allowed": False,
    "retention_policy": "project_duration",
}

_ACCOUNTS = [
    {
        "company_name": "Co1",
        "sector": "b2b_services",
        "city": "Riyadh",
        "relationship_status": "warm",
        "last_interaction": "2026-05",
        "notes": "fit",
    },
    {
        "company_name": "Co2",
        "sector": "logistics",
        "city": "Jeddah",
        "relationship_status": "cold",
    },
]


@pytest.fixture(autouse=True)
def isolated_ledgers(tmp_path, monkeypatch):
    """Isolate every ledger the sprint touches into ``tmp_path``.

    The file-backed proof ledger has no env override, so we redirect its
    module-level ``DEFAULT_DIR`` and drop the cached factory singleton so
    the next ``get_default_ledger()`` re-creates it under ``tmp_path``.
    """
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "capital.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))

    proof_dir = tmp_path / "proof-events"
    proof_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(file_backend, "DEFAULT_DIR", proof_dir)
    reset_default_ledger()
    audit_mod.clear_for_test()
    yield
    reset_default_ledger()


def test_sprint_writes_proof_ledger_entry() -> None:
    """A completed sprint writes a proof_pack_assembled proof-ledger entry
    whose payload carries the assembled sections and the score."""
    run = run_sprint(
        engagement_id="eng_pl1",
        customer_id="cust_pl1",
        source_passport=_GOOD_PASSPORT,
        raw_csv=_DEMO_CSV,
        accounts=_ACCOUNTS,
        problem_summary="rank Saudi B2B accounts",
    )
    assert run.proof_pack and run.proof_pack.get("sections")

    events = get_default_ledger().list_events(
        customer_handle="cust_pl1", event_type="proof_pack_assembled"
    )
    assert events, "no proof_pack_assembled entry was persisted"
    entry = events[0]
    assert entry.payload.get("sections"), "ledger entry payload missing sections"
    assert "score" in entry.payload, "ledger entry payload missing score"
    assert entry.payload.get("engagement_id") == "eng_pl1"
    assert entry.approval_status == "approval_required"

    # The run also records a non-blocked proof_pack_persist step.
    persist_steps = [s for s in run.steps if s.name == "proof_pack_persist"]
    assert persist_steps and persist_steps[0].status == "ran"


def test_sprint_emits_audit_events() -> None:
    """The sprint emits both proof_pack_assembled and output_delivered
    customer-scoped audit events."""
    run_sprint(
        engagement_id="eng_ae1",
        customer_id="cust_ae1",
        source_passport=_GOOD_PASSPORT,
        raw_csv=_DEMO_CSV,
        accounts=_ACCOUNTS,
        problem_summary="rank Saudi B2B accounts",
    )
    kinds = {ev.kind for ev in list_events(customer_id="cust_ae1")}
    assert "proof_pack_assembled" in kinds
    assert "output_delivered" in kinds


def test_audit_chain_intact() -> None:
    """build_chain returns >= 2 nodes and the proof-pack node's output_refs
    references the proof-ledger entry id."""
    run = run_sprint(
        engagement_id="eng_ch1",
        customer_id="cust_ch1",
        source_passport=_GOOD_PASSPORT,
        raw_csv=_DEMO_CSV,
        accounts=_ACCOUNTS,
        problem_summary="rank Saudi B2B accounts",
    )
    chain = build_chain(customer_id="cust_ch1", engagement_id="eng_ch1")
    assert chain.node_count >= 2, "audit chain must link at least two nodes"

    ledger_entry = get_default_ledger().list_events(
        customer_handle="cust_ch1", event_type="proof_pack_assembled"
    )[0]
    proof_nodes = [n for n in chain.nodes if n.kind == "proof_pack_assembled"]
    assert proof_nodes, "no proof_pack node in evidence chain"
    assert ledger_entry.id in proof_nodes[0].output_refs, (
        "proof-pack node does not reference the ledger entry id"
    )

    # The persist step on the run carries the same ledger id.
    persist_step = next(s for s in run.steps if s.name == "proof_pack_persist")
    assert persist_step.output["proof_ledger_entry_id"] == ledger_entry.id


def test_persist_failure_surfaces_not_swallowed(monkeypatch) -> None:
    """If the proof ledger record() raises, the failure is surfaced — the
    run flips to needs_review and gets a blocked proof_pack_persist step.
    No bare except, no silent swallow."""
    ledger = get_default_ledger()

    def _boom(_event):  # noqa: ANN001
        raise RuntimeError("simulated ledger outage")

    monkeypatch.setattr(ledger, "record", _boom)

    run = run_sprint(
        engagement_id="eng_fail1",
        customer_id="cust_fail1",
        source_passport=_GOOD_PASSPORT,
        raw_csv=_DEMO_CSV,
        accounts=_ACCOUNTS,
        problem_summary="rank Saudi B2B accounts",
    )
    assert run.governance_decision == "needs_review"
    blocked = [
        s
        for s in run.steps
        if s.name == "proof_pack_persist" and s.status == "blocked"
    ]
    assert blocked, "persist failure did not produce a blocked step"
    assert "simulated ledger outage" in blocked[0].output["error"]
