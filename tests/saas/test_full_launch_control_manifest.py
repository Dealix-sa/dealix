import json
from pathlib import Path


def test_full_launch_control_manifest_exists_and_has_contract():
    path = Path("data/commercial/full_launch_control_manifest.json")
    assert path.exists(), "missing full launch control manifest"
    data = json.loads(path.read_text(encoding="utf-8"))

    assert data["company"] == "Dealix"
    assert isinstance(data["required_reports"], list)
    assert isinstance(data["required_pages"], list)
    assert isinstance(data["required_guardrails"], list)
    assert isinstance(data["founder_actions"], list)
    assert len(data["required_reports"]) >= 5
    assert len(data["required_pages"]) >= 5


def test_full_launch_control_manifest_references_frontend_pages():
    data = json.loads(Path("data/commercial/full_launch_control_manifest.json").read_text(encoding="utf-8"))
    for rel in data["required_pages"]:
        assert Path(rel).exists(), f"missing frontend page: {rel}"
