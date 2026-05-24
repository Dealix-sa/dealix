"""Tests for the Hermes EventBus + Event envelope."""

from __future__ import annotations

import asyncio

import pytest

from dealix.hermes.events import Event, EventBus, EventType


def _make_event(event_type: EventType = EventType.SIGNAL_CAPTURED) -> Event:
    return Event(
        event_type=event_type,
        actor="test_actor",
        entity_type="signal",
        entity_id="sig_abc",
        payload={"k": "v"},
    )


def test_publish_records_in_recent_buffer() -> None:
    bus = EventBus()
    bus.publish(_make_event())
    assert len(bus.recent()) == 1
    assert bus.recent(limit=0) == []


def test_subscribe_receives_only_target_event_type() -> None:
    bus = EventBus()
    received: list[Event] = []
    bus.subscribe(EventType.OPPORTUNITY_CREATED, lambda e: received.append(e))
    bus.publish(_make_event(EventType.SIGNAL_CAPTURED))
    bus.publish(_make_event(EventType.OPPORTUNITY_CREATED))
    assert len(received) == 1
    assert received[0].event_type == EventType.OPPORTUNITY_CREATED


def test_subscribe_all_receives_everything() -> None:
    bus = EventBus()
    received: list[Event] = []
    bus.subscribe_all(lambda e: received.append(e))
    for et in (
        EventType.SIGNAL_CAPTURED,
        EventType.OPPORTUNITY_CREATED,
        EventType.DECISION_CREATED,
    ):
        bus.publish(_make_event(et))
    assert len(received) == 3


def test_unsubscribe_stops_delivery() -> None:
    bus = EventBus()
    received: list[Event] = []
    handler = received.append
    bus.subscribe(EventType.SIGNAL_CAPTURED, handler)
    assert bus.unsubscribe(EventType.SIGNAL_CAPTURED, handler) is True
    bus.publish(_make_event())
    assert received == []


def test_recent_capacity_is_bounded() -> None:
    bus = EventBus(recent_capacity=3)
    for i in range(5):
        ev = _make_event()
        ev = ev.model_copy(update={"payload": {"i": i}})
        bus.publish(ev)
    recent = bus.recent()
    assert len(recent) == 3
    assert [e.payload["i"] for e in recent] == [2, 3, 4]


def test_async_publish_dispatches_async_handlers() -> None:
    bus = EventBus()
    received: list[str] = []

    async def handler(ev: Event) -> None:
        await asyncio.sleep(0)
        received.append(ev.event_id)

    bus.subscribe(EventType.SIGNAL_CAPTURED, handler)
    asyncio.run(bus.apublish(_make_event()))
    assert len(received) == 1


def test_handler_must_be_callable() -> None:
    bus = EventBus()
    with pytest.raises(TypeError):
        bus.subscribe(EventType.SIGNAL_CAPTURED, "not_callable")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        bus.subscribe_all(42)  # type: ignore[arg-type]


def test_event_envelope_required_fields() -> None:
    with pytest.raises(Exception):
        Event(event_type=EventType.SIGNAL_CAPTURED)  # type: ignore[call-arg]


def test_clear_recent_resets_buffer() -> None:
    bus = EventBus()
    bus.publish(_make_event())
    bus.clear()
    assert bus.recent() == []


def test_async_safety_concurrent_publishes() -> None:
    bus = EventBus()
    received: list[Event] = []
    bus.subscribe_all(lambda e: received.append(e))

    async def producer(n: int) -> None:
        for _ in range(n):
            await bus.apublish(_make_event())

    async def main() -> None:
        await asyncio.gather(producer(5), producer(5))

    asyncio.run(main())
    assert len(received) == 10
