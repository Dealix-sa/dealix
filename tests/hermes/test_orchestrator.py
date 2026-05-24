"""End-to-end orchestrator tests."""

from __future__ import annotations

from dealix.hermes import (
    Event,
    EventBus,
    EventType,
    HermesOrchestrator,
    Signal,
    SignalSource,
    Sovereignty,
    SovereigntyLevel,
)
from dealix.hermes.core.schemas import WorkspaceScope
from dealix.hermes.orchestrator import RunStatus
from dealix.trust.agent_registry import seed_default_registry
from dealix.trust.approvals import ApprovalQueue, ApprovalTicket
from dealix.trust.evidence import EvidenceBuilder, EvidenceStore
from dealix.trust.tool_registry import seed_default_tool_registry


def _orchestrator(events: list[Event]) -> HermesOrchestrator:
    bus = EventBus()
    bus.subscribe_all(events.append)
    return HermesOrchestrator(
        event_bus=bus,
        sovereignty=Sovereignty,
        agent_registry=seed_default_registry(),
        tool_registry=seed_default_tool_registry(),
        approval_center=ApprovalQueue(),
    )


def test_run_low_risk_signal_executes_end_to_end() -> None:
    events: list[Event] = []
    orch = _orchestrator(events)
    signal = Signal(
        source=SignalSource.INTERNAL_NOTE,
        raw_text="how do you handle onboarding internally?",
        channel="slack",
        workspace=WorkspaceScope.INTERNAL,
    )
    run = orch.run(signal)
    assert run.status == RunStatus.COMPLETED
    assert run.opportunity is not None
    assert run.scored is not None
    assert run.decision is not None
    assert run.plan is not None
    assert run.execution_result is not None
    assert run.outcome is not None
    assert run.recommendation is not None


def test_run_publishes_events_in_pipeline_order() -> None:
    events: list[Event] = []
    orch = _orchestrator(events)
    signal = Signal(
        source=SignalSource.INTERNAL_NOTE,
        raw_text="quick playbook ask",
        channel="slack",
    )
    orch.run(signal)
    order = [e.event_type for e in events]
    # Expected prefix in this exact order
    expected_prefix = [
        EventType.SIGNAL_CAPTURED,
        EventType.OPPORTUNITY_CREATED,
        EventType.OPPORTUNITY_SCORED,
        EventType.TRUST_CHECKED,
    ]
    assert order[: len(expected_prefix)] == expected_prefix


def test_high_risk_signal_routes_through_approval() -> None:
    events: list[Event] = []
    orch = _orchestrator(events)
    signal = Signal(
        source=SignalSource.INBOUND_MESSAGE,
        raw_text="please send a proposal at the SAR 60,000 quote we agreed",
        channel="email",
        workspace=WorkspaceScope.CUSTOMER,
    )
    run = orch.run(signal)
    assert run.status == RunStatus.AWAITING_APPROVAL
    assert run.approval_ticket_id is not None
    assert run.sovereignty_verdict is not None
    assert run.sovereignty_verdict.level.numeric >= SovereigntyLevel.S2_SAMI_APPROVAL.numeric
    assert run.sovereignty_verdict.requires_evidence_pack is True
    assert any(e.event_type == EventType.APPROVAL_REQUESTED for e in events)


def test_evidence_pack_buildable_for_high_risk_decision() -> None:
    events: list[Event] = []
    orch = _orchestrator(events)
    signal = Signal(
        source=SignalSource.INBOUND_MESSAGE,
        raw_text="please send a proposal at SAR 60,000",
        channel="email",
    )
    run = orch.run(signal)
    assert run.decision is not None and run.scored is not None
    builder = EvidenceBuilder()
    pack = builder.build_from_decision(run.decision, run.scored)
    store = EvidenceStore()
    pack_id = store.save(pack, entity_ref=f"opportunity:{run.opportunity.opp_id}")  # type: ignore[union-attr]
    assert store.get(pack_id) is pack
    assert pack.recommendation == run.decision.chosen_option


def test_run_step_ids_populated() -> None:
    events: list[Event] = []
    orch = _orchestrator(events)
    signal = Signal(
        source=SignalSource.INTERNAL_NOTE,
        raw_text="benchmark our QBR process",
        channel="slack",
    )
    run = orch.run(signal)
    ids = run.step_ids()
    assert ids["signal_id"] == signal.signal_id
    assert ids["opp_id"] is not None
    assert ids["decision_id"] is not None
    assert ids["plan_id"] is not None
    assert ids["outcome_id"] is not None


def test_classifier_marks_partner_signal_as_partner() -> None:
    events: list[Event] = []
    orch = _orchestrator(events)
    signal = Signal(
        source=SignalSource.INBOUND_MESSAGE,
        raw_text="we are interested in a white-label partnership",
        channel="email",
    )
    classification = orch.classify(signal)
    assert classification.category.value == "partner"


def test_approval_ticket_appears_in_queue() -> None:
    events: list[Event] = []
    bus = EventBus()
    bus.subscribe_all(events.append)
    queue = ApprovalQueue()
    orch = HermesOrchestrator(
        event_bus=bus,
        agent_registry=seed_default_registry(),
        tool_registry=seed_default_tool_registry(),
        approval_center=queue,
    )
    signal = Signal(
        source=SignalSource.INBOUND_MESSAGE,
        raw_text="please send proposal for SAR 80,000",
        channel="email",
    )
    run = orch.run(signal)
    pending = queue.pending()
    assert len(pending) == 1
    assert pending[0].ticket_id == run.approval_ticket_id


def test_run_without_optional_registries_still_works() -> None:
    events: list[Event] = []
    bus = EventBus()
    bus.subscribe_all(events.append)
    orch = HermesOrchestrator(event_bus=bus)
    signal = Signal(
        source=SignalSource.INTERNAL_NOTE,
        raw_text="internal playbook benchmark",
        channel="slack",
    )
    run = orch.run(signal)
    assert run.status == RunStatus.COMPLETED


def test_approval_ticket_carries_sovereignty_level() -> None:
    queue = ApprovalQueue()
    bus = EventBus()
    orch = HermesOrchestrator(
        event_bus=bus,
        agent_registry=seed_default_registry(),
        tool_registry=seed_default_tool_registry(),
        approval_center=queue,
    )
    signal = Signal(
        source=SignalSource.TENDER,
        raw_text="public tender request",
        channel="portal",
    )
    run = orch.run(signal)
    assert run.approval_ticket_id is not None
    ticket: ApprovalTicket = queue.get(run.approval_ticket_id)
    assert ticket.sovereignty_level.numeric >= SovereigntyLevel.S2_SAMI_APPROVAL.numeric
