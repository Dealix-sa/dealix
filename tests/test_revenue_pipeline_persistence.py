"""Revenue Pipeline durability — survives a process restart.

The pipeline kept leads in memory only, so a redeploy wiped every
tracked lead and deal. These tests cover the durable-storage layer and
its graceful degradation when the database is unreachable.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_pipeline import persistence
from auto_client_acquisition.revenue_pipeline.lead import Lead
from auto_client_acquisition.revenue_pipeline.pipeline import RevenuePipeline


def test_to_row_preserves_evidence_fields() -> None:
    lead = Lead.make(slot_id="A", sector="b2b")
    lead = lead.model_copy(update={
        "stage": "commitment_received",
        "commitment_evidence": "email_2026-05-17_signed_intent.png",
        "payment_evidence": "moyasar_dashboard.png",
        "actual_amount_sar": 499,
    })
    row = persistence._to_row(lead)
    assert row["id"] == lead.id
    assert row["stage"] == "commitment_received"
    assert row["commitment_evidence"] == "email_2026-05-17_signed_intent.png"
    assert row["payment_evidence"] == "moyasar_dashboard.png"
    assert row["actual_amount_sar"] == 499
    # payload is the full serialized Lead — the hydration source of truth.
    assert row["payload"]["id"] == lead.id


def test_payload_round_trips_through_lead_model() -> None:
    lead = Lead.make(slot_id="X", sector="logistics")
    lead = lead.model_copy(update={"stage": "pilot_offered", "expected_amount_sar": 1500})
    payload = persistence._to_row(lead)["payload"]
    restored = Lead.model_validate(payload)
    assert restored.id == lead.id
    assert restored.stage == "pilot_offered"
    assert restored.expected_amount_sar == 1500


def test_bulk_load_repopulates_a_fresh_pipeline() -> None:
    leads = [
        Lead.make(slot_id="A", sector="b2b"),
        Lead.make(slot_id="B", sector="retail"),
    ]
    fresh = RevenuePipeline()
    loaded = fresh.bulk_load(leads)
    assert loaded == 2
    for lead in leads:
        assert fresh.get(lead.id) is not None


def test_restart_simulation_preserves_lead_and_evidence() -> None:
    # Lifecycle in one process...
    p1 = RevenuePipeline()
    p1.add(Lead.make(slot_id="A", sector="b2b"))
    lead = p1.list_all()[0]
    for stage in (
        "message_drafted", "founder_sent_manually", "replied",
        "diagnostic_requested", "diagnostic_delivered", "pilot_offered",
    ):
        p1.advance(lead.id, stage)
    advanced = p1.advance(
        lead.id, "commitment_received",
        commitment_evidence="signed_intent.png",
    )

    # ...the process restarts: a fresh pipeline hydrates from the payloads.
    serialized = [_l.model_dump(mode="json") for _l in p1.list_all()]
    p2 = RevenuePipeline()
    p2.bulk_load([Lead.model_validate(s) for s in serialized])

    survived = p2.get(advanced.id)
    assert survived is not None
    assert survived.stage == "commitment_received"
    assert survived.commitment_evidence == "signed_intent.png"


@pytest.mark.asyncio
async def test_upsert_degrades_gracefully_without_db() -> None:
    # No database is configured in the test environment; upsert must
    # return False, never raise — a missing DB cannot crash the API.
    lead = Lead.make(slot_id="A", sector="b2b")
    result = await persistence.upsert(lead)
    assert result is False


@pytest.mark.asyncio
async def test_load_all_returns_empty_without_db() -> None:
    leads = await persistence.load_all()
    assert leads == []


@pytest.mark.asyncio
async def test_upsert_many_empty_is_noop_success() -> None:
    assert await persistence.upsert_many([]) is True
