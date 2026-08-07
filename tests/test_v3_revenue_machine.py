"""V3 — Revenue Machine registry is a check, not a promise.

Asserts the registry declares all seven layers and that every canonical artifact it
references actually exists on disk. If a canonical path is wrong or a referenced file
is deleted, this test fails — keeping the "Revenue Machine is wired" claim honest.
"""

from __future__ import annotations

from dealix.commercial_ops.v3_revenue_machine import (
    build_v3_revenue_machine_snapshot,
    load_v3_revenue_machine_config,
    verify_v3_revenue_machine_repo,
)

EXPECTED_LAYER_IDS = {
    "lead_capture_attribution",
    "crm_ledger",
    "offer_builder",
    "case_study_engine",
    "analytics_kpis",
    "delivery_os",
    "security_doctrine",
}


def test_registry_declares_seven_layers() -> None:
    cfg = load_v3_revenue_machine_config()
    assert cfg.get("version")
    ids = {layer["id"] for layer in cfg["layers"]}
    assert ids == EXPECTED_LAYER_IDS


def test_every_canonical_artifact_exists() -> None:
    repo = verify_v3_revenue_machine_repo()
    assert repo["ok"], f"missing artifacts: {repo['issues']}"
    assert repo["layers_checked"] == 7
    assert repo["artifacts_checked"] >= 40


def test_snapshot_shape_is_serializable() -> None:
    snap = build_v3_revenue_machine_snapshot()
    assert snap["version"]
    assert snap["map_doc"]
    assert len(snap["layers"]) == 7
    for layer in snap["layers"]:
        assert layer["id"]
        assert layer["artifact_count"] >= 1
        assert isinstance(layer["doctrine"], list)


def test_doctrine_binding_present_for_security_layer() -> None:
    cfg = load_v3_revenue_machine_config()
    sec = next(layer for layer in cfg["layers"] if layer["id"] == "security_doctrine")
    assert "no_cold_whatsapp" in sec["doctrine"]
    assert "no_scraping" in sec["doctrine"]
