"""Founder agent queue + packet printing."""

from __future__ import annotations

from dealix.commercial_ops.founder_agent_tasks import (
    build_queue_status,
    seed_today_queue,
    templates_as_packets,
)


def test_templates_as_packets_has_engineer() -> None:
    packets = templates_as_packets()
    assert packets["engineer_gates"]["agent"] == "dealix-engineer"


def test_seed_and_status() -> None:
    seed_today_queue(force=True)
    status = build_queue_status()
    assert status["seeded"] is True
    assert status["pending_p0_count"] >= 1
