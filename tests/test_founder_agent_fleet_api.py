"""Smoke: founder agent fleet today-pack handler."""

from dealix.commercial_ops.agent_fleet_tasks import build_agent_fleet_today_pack
from dealix.commercial_ops.ceo_gtm_operating_system import build_ceo_gtm_status
from dealix.commercial_ops.doctrine import build_soaen_daily


def test_today_pack_payload_shape() -> None:
    body = {
        "soaen": build_soaen_daily(),
        "agent_fleet": build_agent_fleet_today_pack(),
        "ceo_gtm_status": build_ceo_gtm_status(api_base=False),
    }
    assert "soaen_checklist_ar" in body["soaen"] or "soaen" in str(body["soaen"])
    assert body["agent_fleet"]["schema_version"] == "1.0"
    assert "verdict" in body["ceo_gtm_status"]
