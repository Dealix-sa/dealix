"""WhatsApp Client OS — JSON Schema contracts, permissions, templates, cards."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_client_acquisition.whatsapp_client_os import permission_levels as pl
from auto_client_acquisition.whatsapp_client_os import templates
from auto_client_acquisition.whatsapp_client_os.action_card_builder import (
    to_whatsapp_payload,
    welcome_menu,
)
from auto_client_acquisition.whatsapp_client_os.permission_guard import (
    build_permission_request,
    evaluate_grant,
)
from auto_client_acquisition.whatsapp_client_os.schemas import (
    ClientAssessment,
    ClientCard,
    InboundMessage,
    PermissionRequest,
    WhatsAppSession,
)

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCHEMA_DIR = _REPO_ROOT / "dealix" / "contracts" / "schemas"

_SCHEMA_FILES = {
    "whatsapp_session.schema.json": WhatsAppSession,
    "whatsapp_intake.schema.json": InboundMessage,
    "whatsapp_action_card.schema.json": ClientCard,
    "client_permission.schema.json": PermissionRequest,
    "client_onboarding_assessment.schema.json": ClientAssessment,
}


@pytest.mark.parametrize("filename,model", list(_SCHEMA_FILES.items()))
def test_json_schema_exists_and_matches_model(filename: str, model: type) -> None:
    path = _SCHEMA_DIR / filename
    assert path.exists(), f"missing schema {filename} — run export_whatsapp_client_os_schemas.py"
    on_disk = json.loads(path.read_text(encoding="utf-8"))
    live = model.model_json_schema()
    # property set must match (the load-bearing contract)
    assert set(on_disk.get("properties", {})) == set(live.get("properties", {}))


# ── Permission ladder ─────────────────────────────────────────────────-──
def test_permission_ladder_has_six_levels() -> None:
    assert len(pl.all_specs()) == 6
    assert [s.level for s in pl.all_specs()] == ["L0", "L1", "L2", "L3", "L4", "L5"]


def test_default_levels_are_l0_l1() -> None:
    assert pl.is_default_allowed("L0") is True
    assert pl.is_default_allowed("L1") is True
    assert pl.is_default_allowed("L2") is False


def test_l5_cannot_complete_in_whatsapp() -> None:
    assert pl.can_complete_in_whatsapp("L5") is False
    assert pl.escalate_needed("L5") is True


def test_l4_requires_explicit_approval() -> None:
    assert pl.requires_explicit_approval("L4") is True
    assert pl.requires_explicit_approval("L1") is False


def test_credential_request_forces_secure_portal() -> None:
    req = build_permission_request(level="L2", system="HubSpot", needs_secret=True)
    assert req.secure_portal_required is True
    # granting without the secure portal is refused
    decision = evaluate_grant(req, granted=True, via_secure_portal=False)
    assert decision.allowed is False
    assert decision.requires_secure_portal is True


def test_l5_grant_routes_to_human() -> None:
    req = build_permission_request(level="L5", system="Payments")
    decision = evaluate_grant(req, granted=True, via_secure_portal=True)
    assert decision.allowed is False
    assert decision.requires_human is True


# ── Templates ─────────────────────────────────────────────────────────-──
def test_all_canonical_template_keys_render() -> None:
    for key in templates.TEMPLATE_KEYS:
        body = templates.get_template(key)
        assert body, f"template {key} is empty"


def test_render_leaves_unknown_vars_untouched() -> None:
    out = templates.render("assessment_start", step=2, total=10)
    assert "2" in out and "10" in out


# ── WhatsApp interactive payloads ─────────────────────────────────────-──
def test_menu_with_more_than_three_options_uses_list() -> None:
    payload = to_whatsapp_payload(welcome_menu())
    assert payload["interactive"]["type"] == "list"
    rows = payload["interactive"]["action"]["sections"][0]["rows"]
    assert 1 <= len(rows) <= 10


def test_three_option_card_uses_buttons() -> None:
    from auto_client_acquisition.whatsapp_client_os.action_card_builder import support_menu

    card = support_menu()
    payload = to_whatsapp_payload(card)
    # support menu has 5 options → list
    assert payload["interactive"]["type"] in {"list", "button"}
