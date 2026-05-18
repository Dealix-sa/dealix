"""Agent fleet unified tasks."""

from dealix.commercial_ops.agent_fleet_tasks import (
    build_agent_fleet_today_pack,
    load_unified_daily_tasks,
)


def test_unified_daily_tasks_non_empty() -> None:
    tasks = load_unified_daily_tasks()
    assert len(tasks) >= 3


def test_agent_fleet_today_pack_schema() -> None:
    pack = build_agent_fleet_today_pack()
    assert pack["schema_version"] == "1.0"
    assert "queue_tasks" in pack
