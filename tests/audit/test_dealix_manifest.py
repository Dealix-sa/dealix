"""Structural tests for dealix_manifest.yaml — the Audit-First Remediation contract.

These tests guarantee the manifest itself is well-formed before any
verifier reads it. They are intentionally cheap (no I/O outside the
repo, no network).
"""
from __future__ import annotations

from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")

REPO = Path(__file__).resolve().parents[2]
MANIFEST = REPO / "dealix_manifest.yaml"


@pytest.fixture(scope="module")
def manifest() -> dict:
    assert MANIFEST.exists(), "dealix_manifest.yaml is missing"
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_manifest_has_version_and_owner(manifest: dict) -> None:
    assert manifest.get("version"), "manifest.version required"
    assert manifest.get("owner"), "manifest.owner required"


def test_manifest_has_layers(manifest: dict) -> None:
    layers = manifest.get("layers")
    assert isinstance(layers, dict)
    assert layers, "manifest.layers cannot be empty"


def test_manifest_has_global_rules(manifest: dict) -> None:
    rules = manifest.get("global_rules")
    assert isinstance(rules, dict)
    for key in (
        "min_doc_size_bytes",
        "min_script_size_bytes",
        "banned_claims",
        "required_external_action_gates",
    ):
        assert key in rules, f"global_rules.{key} required"


def test_each_layer_declares_required_files(manifest: dict) -> None:
    for name, layer in manifest["layers"].items():
        assert isinstance(layer, dict), f"layer {name} is not a mapping"
        assert "required_files" in layer, f"layer {name} missing required_files"
        files = layer["required_files"]
        assert isinstance(files, list) and files, (
            f"layer {name}.required_files must be a non-empty list"
        )


def test_each_layer_has_verifier(manifest: dict) -> None:
    for name, layer in manifest["layers"].items():
        verifier = layer.get("verifier")
        assert verifier, f"layer {name} missing verifier"
        assert (REPO / verifier).exists(), (
            f"layer {name} verifier missing on disk: {verifier}"
        )


def test_banned_claims_non_empty(manifest: dict) -> None:
    banned = manifest["global_rules"]["banned_claims"]
    assert isinstance(banned, list) and banned
    # The two we will never tolerate.
    low = {c.lower() for c in banned}
    assert any("guaranteed revenue" in c for c in low)
    assert any("no risk" in c or "no-risk" in c for c in low)


def test_required_external_action_gates_cover_basics(manifest: dict) -> None:
    gates = set(manifest["global_rules"]["required_external_action_gates"])
    for required in ("approval", "policy", "audit", "suppression_check"):
        assert required in gates


def test_core_layers_present(manifest: dict) -> None:
    expected = {
        "founder_console",
        "ceo_operating_system",
        "ai_governance",
        "policy_as_code",
        "agent_registry",
        "machine_registry",
        "eval_gate",
        "live_send_safety",
        "railway_production",
        "audit_reports",
    }
    layers = set(manifest["layers"].keys())
    missing = expected - layers
    assert not missing, f"missing core layers: {missing}"
