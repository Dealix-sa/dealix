"""End-to-end tests for the Hermes API router (Wave 2).

Uses the local `async_hermes_client` fixture (see `tests/api/conftest.py`)
because the repo-wide `async_client` fixture is currently blocked by a
pre-existing pyo3 / cryptography panic.
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from api.routers import hermes as hermes_router
from dealix.hermes.core.opportunities import (
    Opportunity,
    OpportunityType,
    ScoredOpportunity,
)
from dealix.hermes.core.decisions import Decision
from dealix.hermes.core.schemas import Money
from dealix.trust.evidence import EvidenceBuilder


_HEADERS = {"X-Admin-API-Key": "test-admin-key"}


@pytest.mark.asyncio
async def test_signal_post_returns_200_and_run(async_hermes_client: AsyncClient) -> None:
    payload = {
        "source": "inbound_message",
        "raw_text": "Founder wants pricing proposal.",
        "channel": "email",
        "workspace": "internal",
        "metadata": {},
    }
    response = await async_hermes_client.post(
        "/api/v1/hermes/signals",
        json=payload,
        headers=_HEADERS,
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] in {"completed", "awaiting_approval", "blocked"}
    assert body["signal_id"].startswith("sig_")
    assert "events_published" in body


@pytest.mark.asyncio
async def test_invalid_admin_key_returns_401(async_hermes_client: AsyncClient) -> None:
    response = await async_hermes_client.get(
        "/api/v1/hermes/agents",
        headers={"X-Admin-API-Key": "wrong-key"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_pending_approvals_lists_submitted_ticket(
    async_hermes_client: AsyncClient,
) -> None:
    # An enterprise-tier monetary signal will land in S2_SAMI_APPROVAL.
    payload = {
        "source": "inbound_message",
        "raw_text": "Enterprise prospect wants a proposal for 30000 SAR contract.",
        "channel": "email",
        "workspace": "customer",
    }
    response = await async_hermes_client.post(
        "/api/v1/hermes/signals",
        json=payload,
        headers=_HEADERS,
    )
    assert response.status_code == 200, response.text
    # Now list pending approvals.
    pending = await async_hermes_client.get(
        "/api/v1/hermes/approvals/pending",
        headers=_HEADERS,
    )
    assert pending.status_code == 200
    data = pending.json()
    assert data["count"] >= 1


@pytest.mark.asyncio
async def test_approve_transitions_status(async_hermes_client: AsyncClient) -> None:
    # Push a signal that lands in approval, then approve the resulting ticket.
    payload = {
        "source": "inbound_message",
        "raw_text": "Customer requesting proposal worth 30000 SAR confidential.",
        "channel": "email",
        "workspace": "customer",
    }
    run_resp = await async_hermes_client.post(
        "/api/v1/hermes/signals",
        json=payload,
        headers=_HEADERS,
    )
    run = run_resp.json()
    ticket_id = run["approval_ticket_id"]
    assert ticket_id, run

    approve_resp = await async_hermes_client.post(
        f"/api/v1/hermes/approvals/{ticket_id}/approve",
        json={"by": "sami", "note": "looks good"},
        headers=_HEADERS,
    )
    assert approve_resp.status_code == 200
    body = approve_resp.json()
    assert body["status"] == "approved"
    assert body["decided_by"] == "sami"


@pytest.mark.asyncio
async def test_recent_events_returns_events(async_hermes_client: AsyncClient) -> None:
    # Run one signal to populate the bus.
    await async_hermes_client.post(
        "/api/v1/hermes/signals",
        json={
            "source": "inbound_message",
            "raw_text": "knowledge ask: how do you handle x?",
            "channel": "email",
        },
        headers=_HEADERS,
    )
    response = await async_hermes_client.get(
        "/api/v1/hermes/events/recent?limit=10",
        headers=_HEADERS,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1
    assert all("event_type" in e for e in data["events"])


@pytest.mark.asyncio
async def test_evidence_retrieval_by_pack_id(async_hermes_client: AsyncClient) -> None:
    # Build an evidence pack inside the state so we can fetch it.
    state = hermes_router.get_state()
    opp = Opportunity(
        signal_id="sig_test",
        opp_type=OpportunityType.REVENUE,
        title="Demo lead",
        narrative="demo narrative",
        expected_value=Money.sar(5000),
    )
    scored = ScoredOpportunity(
        opportunity=opp,
        score=3.2,
        rationale="weighted score",
        components={"revenue": 1.0},
    )
    decision = Decision(
        opportunity_id=opp.opp_id,
        summary="ship the proposal",
        options=["ship", "park"],
        chosen_option="ship",
        rationale="testing",
    )
    builder = EvidenceBuilder()
    pack = builder.build_from_decision(decision, scored)
    state.evidence.save(pack, entity_ref=opp.opp_id)

    response = await async_hermes_client.get(
        f"/api/v1/hermes/evidence/{pack.pack_id}",
        headers=_HEADERS,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["pack_id"] == pack.pack_id
    assert body["recommendation"] == "ship"


@pytest.mark.asyncio
async def test_list_agents_and_tools(async_hermes_client: AsyncClient) -> None:
    agents = await async_hermes_client.get(
        "/api/v1/hermes/agents",
        headers=_HEADERS,
    )
    tools = await async_hermes_client.get(
        "/api/v1/hermes/tools",
        headers=_HEADERS,
    )
    assert agents.status_code == 200
    assert tools.status_code == 200
    assert agents.json()["count"] >= 5
    assert tools.json()["count"] >= 5


@pytest.mark.asyncio
async def test_declare_incident_pauses_agents(
    async_hermes_client: AsyncClient,
) -> None:
    response = await async_hermes_client.post(
        "/api/v1/hermes/incidents/declare",
        json={
            "severity": "sev1",
            "summary": "Test incident — auto-pause check",
            "owner": "sami",
            "implicated_agents": ["ProposalFactoryAgent"],
            "implicated_tools": ["email_send"],
        },
        headers=_HEADERS,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["severity"] == "sev1"
    assert "ProposalFactoryAgent" in body["agents_paused"]
