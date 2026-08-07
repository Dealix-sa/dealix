from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_suite() -> ModuleType:
    repo_root = Path(__file__).resolve().parents[1]
    scripts_dir = repo_root / "scripts"
    sys.path.insert(0, str(scripts_dir))
    return load_module(scripts_dir / "design_os_suite.py", "design_os_suite")


def test_validate_artifact_blocks_live_sends() -> None:
    suite = load_suite()
    data = {
        "artifact_key": "x",
        "title": "X",
        "generated_at": "2026-01-01T00:00:00Z",
        "business_goal": "Goal",
        "primary_user": "User",
        "source_context": "Context",
        "generated_by": "test",
        "approval_state": "draft",
        "safety_status": "safe_draft_only",
        "handoff_target": "internal_review",
        "sections": [{"title": "A", "body": "B"}],
        "risks": [],
        "next_actions": [],
        "live_sends": 1,
    }
    findings = suite.validate_artifact(data)
    assert any(finding.code == "live_sends" for finding in findings)


def test_index_renders_artifact_table(tmp_path: Path) -> None:
    suite = load_suite()
    payload = {
        "artifact_key": "revenue-command-room",
        "title": "Revenue Command Room V0",
        "generated_at": "2026-01-01T00:00:00Z",
        "business_goal": "Goal",
        "primary_user": "User",
        "source_context": "Context",
        "generated_by": "test",
        "approval_state": "draft",
        "safety_status": "safe_draft_only",
        "handoff_target": "html_preview",
        "sections": [{"title": "A", "body": "B"}],
        "risks": [],
        "next_actions": [],
        "live_sends": 0,
    }
    (tmp_path / "revenue-command-room.json").write_text(
        suite.json.dumps(payload),
        encoding="utf-8",
    )
    index = suite.build_index(tmp_path)
    assert "Revenue Command Room V0" in index
    assert "safe_draft_only" in index


def test_markdown_to_html_includes_draft_banner() -> None:
    suite = load_suite()
    html = suite.markdown_to_html("# Title\n\n## Section\n\nBody", "Title")
    assert "Dealix Design OS Preview" in html
    assert "<h1>Title</h1>" in html
    assert "<h2>Section</h2>" in html


def test_validation_report_status_pass_for_valid_artifact(tmp_path: Path) -> None:
    suite = load_suite()
    payload = {
        "artifact_key": "company-brain",
        "title": "Company Brain Design Artifact V0",
        "generated_at": "2026-01-01T00:00:00Z",
        "business_goal": "Goal",
        "primary_user": "User",
        "source_context": "Context",
        "generated_by": "test",
        "approval_state": "draft",
        "safety_status": "safe_draft_only",
        "handoff_target": "internal_review",
        "sections": [{"title": "A", "body": "B"}],
        "risks": [],
        "next_actions": [],
        "live_sends": 0,
    }
    (tmp_path / "company-brain.json").write_text(
        suite.json.dumps(payload),
        encoding="utf-8",
    )
    findings, files = suite.validate_report_dir(tmp_path)
    report = suite.render_validation_report(tmp_path, findings, files)
    assert "Status: pass" in report
