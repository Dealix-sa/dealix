from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest


def load_design_command_room() -> ModuleType:
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "design_command_room.py"
    spec = importlib.util.spec_from_file_location("design_command_room", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def set_safe_env(module: ModuleType, monkeypatch: pytest.MonkeyPatch) -> None:
    for key, value in module.SAFE_ENV_DEFAULTS.items():
        monkeypatch.setenv(key, value)


def test_templates_cover_core_dealix_surfaces() -> None:
    module = load_design_command_room()
    expected = {
        "revenue-command-room",
        "founder-war-room",
        "client-proof-pack",
        "sales-deck",
        "landing-page",
        "client-growth",
        "delivery-os",
        "company-brain",
    }
    assert expected.issubset(set(module.TEMPLATES))


def test_generated_artifact_is_draft_only_and_has_no_live_sends(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = load_design_command_room()
    set_safe_env(module, monkeypatch)
    template = module.TEMPLATES["revenue-command-room"]
    artifact = module.build_artifact(template, "Saudi B2B launch workflow")
    assert artifact.approval_state == "draft"
    assert artifact.live_sends == 0
    assert artifact.safety_status == "safe_draft_only"
    assert artifact.sections


def test_write_artifact_outputs_markdown_and_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module = load_design_command_room()
    set_safe_env(module, monkeypatch)
    monkeypatch.setattr(module, "LATEST_MARKDOWN", tmp_path / "latest.md")
    monkeypatch.setattr(module, "LATEST_JSON", tmp_path / "latest.json")
    template = module.TEMPLATES["client-proof-pack"]
    artifact = module.build_artifact(template, "Client delivery sprint")
    markdown_path, json_path = module.write_artifact(artifact, tmp_path)
    assert markdown_path.exists()
    assert json_path.exists()
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "Approval state: draft" in markdown
    assert "Live sends: 0" in markdown
    assert "Claims Review" in markdown


def test_blocked_claims_are_detected() -> None:
    module = load_design_command_room()
    blocked = module.review_claims("This guarantees revenue and guaranteed ROI.")
    assert "guaranteed revenue" in blocked
    assert "guaranteed roi" in blocked
