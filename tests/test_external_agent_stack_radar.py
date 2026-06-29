from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_radar() -> ModuleType:
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "agents" / "external_agent_stack_radar.py"
    spec = importlib.util.spec_from_file_location("external_agent_stack_radar", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_radar_has_core_repos() -> None:
    module = load_radar()
    names = {signal.name for signal in module.REPO_SIGNALS}
    assert "LangGraph" in names
    assert "OpenAI Agents SDK" in names
    assert "Model Context Protocol" in names
    assert "NVIDIA NeMo Agent Toolkit" in names


def test_radar_is_safe_by_default() -> None:
    module = load_radar()
    payload = module.build_report()
    safety = payload["safety_posture"]
    assert safety["external_send_enabled"] is False
    assert safety["runtime_dependencies_added"] is False
    assert safety["repositories_vendored"] is False
    assert safety["mcp_enabled"] is False
    assert safety["outbound_mode"] == "draft_only"


def test_write_outputs_creates_markdown_and_json(tmp_path: Path) -> None:
    module = load_radar()
    markdown_path, json_path = module.write_outputs(tmp_path)
    assert markdown_path.exists()
    assert json_path.exists()
    markdown = markdown_path.read_text(encoding="utf-8")
    assert "Dealix External Agent Stack Radar" in markdown
    assert "No external runtime" in markdown
