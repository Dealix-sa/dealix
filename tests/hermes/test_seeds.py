"""
Tests for db/seeds — verify shape, counts, and uniqueness so future drift
shows up in CI before it reaches a deployment seeder.

The seeds are imported by absolute filesystem path to avoid the heavy
`db.__init__` side-effects (which pull in optional deps like `phonenumbers`).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


SEEDS_DIR = Path(__file__).resolve().parents[2] / "db" / "seeds"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(
        f"db.seeds.{name}", SEEDS_DIR / f"{name}.py"
    )
    assert spec and spec.loader, f"could not build spec for db.seeds.{name}"
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "module_name,attr,expected_min",
    [
        ("agents_seed", "AGENTS", 8),
        ("tools_seed", "TOOLS", 10),
        ("offers_seed", "OFFERS", 10),
        ("policies_seed", "POLICIES", 6),
        ("controls_seed", "CONTROLS", 9),
        ("icp_seed", "ICPS", 5),
    ],
)
def test_seed_module_exposes_expected_list(
    module_name: str, attr: str, expected_min: int
) -> None:
    mod = _load(module_name)
    items = getattr(mod, attr)
    assert isinstance(items, list)
    assert len(items) >= expected_min
    assert all(isinstance(i, dict) for i in items)


def test_agents_seed_each_has_owner_and_role() -> None:
    agents = _load("agents_seed").AGENTS
    for a in agents:
        assert a.get("owner"), f"agent missing owner: {a}"
        assert a.get("role") or a.get("id"), f"agent missing role/id: {a}"


def test_tools_seed_each_has_owner_and_sensitivity() -> None:
    tools = _load("tools_seed").TOOLS
    # seeds use a risk-tier vocabulary ({low, medium, high}); ToolGateway
    # accepts both this set and the {read, write, external} vocabulary the
    # in-process descriptor uses. Either is fine — we just enforce that the
    # value is non-empty and from one of the known sets.
    allowed = {"low", "medium", "high", "read", "write", "external"}
    for t in tools:
        assert t.get("owner"), f"tool missing owner: {t}"
        assert t.get("sensitivity") in allowed, t


def test_offers_seed_has_unique_ids_and_price_bands() -> None:
    offers = _load("offers_seed").OFFERS
    ids = [o["offer_id"] for o in offers]
    assert len(ids) == len(set(ids)), "offer ids must be unique"
    for o in offers:
        assert o["price_min_sar"] > 0
        assert o["price_min_sar"] <= o["price_max_sar"]


def test_controls_seed_has_known_control_ids() -> None:
    controls = _load("controls_seed").CONTROLS
    ids = {c["control_id"] for c in controls}
    # core controls from the architecture spec
    for required in [
        "CTRL-GOV-001",
        "CTRL-GOV-002",
        "CTRL-GOV-003",
        "CTRL-SEC-001",
        "CTRL-OPS-001",
        "CTRL-TRANS-001",
        "CTRL-COM-001",
    ]:
        assert required in ids, f"missing control {required}"


def test_icp_seed_each_has_geography_and_pain() -> None:
    icps = _load("icp_seed").ICPS
    for icp in icps:
        assert icp.get("icp_id"), f"missing icp_id: {icp}"
        assert icp.get("geography"), f"missing geography: {icp}"
        assert icp.get("primary_pain"), f"missing primary_pain: {icp}"
