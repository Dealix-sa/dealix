"""Enterprise Transformation OS — catalog tests.

Validates the 10 transformation offerings added to the canonical registry:
- exactly 10, all customer_journey_stage == "transformation"
- setup/monthly range fields are coherent
- doctrine-safe: no live action modes, required hard_gates present
- no guaranteed-outcome language anywhere
- Growth Engine OS is explicitly outreach-safe (draft-only, gated)

Sandbox-safe — loads the registry via importlib without importing api/* (mirrors
tests/test_service_catalog.py to avoid the python-jose/pyo3 cascade).
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

_TRANSFORMATION_IDS = {
    "ai_command_center_os",
    "whatsapp_revenue_os",
    "brand_intelligence_os",
    "ai_agent_workforce_os",
    "client_experience_os",
    "operations_automation_os",
    "executive_reporting_os",
    "trust_governance_os",
    "growth_engine_os",
    "custom_enterprise_system",
}


def _load_registry():
    repo_root = Path(__file__).resolve().parent.parent
    schemas_path = repo_root / "auto_client_acquisition" / "service_catalog" / "schemas.py"
    spec_s = importlib.util.spec_from_file_location(
        "_test_tx_catalog_schemas", schemas_path
    )
    assert spec_s is not None and spec_s.loader is not None
    schemas_mod = importlib.util.module_from_spec(spec_s)
    sys.modules["_test_tx_catalog_schemas"] = schemas_mod
    spec_s.loader.exec_module(schemas_mod)

    registry_path = repo_root / "auto_client_acquisition" / "service_catalog" / "registry.py"
    src = registry_path.read_text(encoding="utf-8")
    src = src.replace(
        "from auto_client_acquisition.service_catalog.schemas import ServiceOffering",
        "from _test_tx_catalog_schemas import ServiceOffering",
    )
    ns: dict = {}
    exec(compile(src, str(registry_path), "exec"), ns)
    return ns


_NS = _load_registry()
OFFERINGS = _NS["OFFERINGS"]
get_offering = _NS["get_offering"]
_TX = [o for o in OFFERINGS if o.customer_journey_stage == "transformation"]


def test_ten_transformation_offerings_present():
    ids = {o.id for o in _TX}
    assert len(_TX) == 10
    assert ids == _TRANSFORMATION_IDS, f"id mismatch: {ids ^ _TRANSFORMATION_IDS}"


def test_setup_and_monthly_ranges_coherent():
    for o in _TX:
        if o.price_sar_max is not None:
            assert o.price_sar <= o.price_sar_max, f"{o.id} setup floor > ceiling"
        if o.price_monthly_sar_min is not None and o.price_monthly_sar_max is not None:
            assert o.price_monthly_sar_min <= o.price_monthly_sar_max, f"{o.id} monthly range"
    # The 9 paid systems are setup ranges; custom system is custom-priced.
    ranged = [o for o in _TX if o.setup_is_range]
    assert len(ranged) == 9
    custom = get_offering("custom_enterprise_system")
    assert custom.price_unit == "custom"
    assert custom.price_sar == 0.0


def test_required_hard_gates_present():
    required = {"no_live_send", "no_live_charge", "no_cold_whatsapp", "no_scraping", "no_fake_proof"}
    for o in _TX:
        assert required <= set(o.hard_gates), f"{o.id} missing gates: {required - set(o.hard_gates)}"
        for g in o.hard_gates:
            assert g.startswith("no_"), f"{o.id} non-prohibition gate: {g}"


def test_no_forbidden_action_modes():
    forbidden = {"live_send", "live_charge", "auto_send", "auto_charge"}
    for o in _TX:
        assert not (set(o.action_modes_used) & forbidden), f"{o.id} uses live/auto mode"


def test_no_guaranteed_language_anywhere():
    forbidden = [re.compile(r"\bguarantee", re.IGNORECASE), re.compile("نضمن")]
    for o in _TX:
        blob = " ".join([
            o.name_ar, o.name_en, o.kpi_commitment_ar, o.kpi_commitment_en,
            o.refund_policy_ar, o.refund_policy_en, *o.deliverables,
        ])
        for pat in forbidden:
            m = pat.search(blob)
            assert m is None, f"{o.id}: forbidden token {m.group(0)!r}"


def test_growth_engine_is_outreach_safe():
    ge = get_offering("growth_engine_os")
    assert ge is not None
    # Must explicitly forbid cold/automated/bulk outreach + scraping.
    for gate in ("no_cold_whatsapp", "no_linkedin_auto", "no_blast", "no_scraping"):
        assert gate in ge.hard_gates, f"growth_engine_os missing {gate}"
    # No autonomous execution beyond approval.
    assert "approved_manual" not in ge.action_modes_used
    assert set(ge.action_modes_used) <= {"suggest_only", "draft_only", "approval_required"}
    # Deliverables must not advertise cold/blast/scrape.
    joined = " ".join(ge.deliverables).lower()
    for bad in ("cold", "blast", "scrape", "scraping"):
        assert bad not in joined, f"growth_engine_os deliverable advertises {bad!r}"


def test_all_transformation_offerings_are_estimates():
    for o in _TX:
        assert o.is_estimate is True, f"{o.id} not flagged is_estimate"
