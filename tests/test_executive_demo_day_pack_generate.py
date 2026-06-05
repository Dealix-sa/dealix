"""V10 — executive_demo_day_pack_generate writes the 4 demo-day drafts."""

from __future__ import annotations

import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
_SCRIPT = REPO / "scripts" / "executive_demo_day_pack_generate.py"


def _load():
    spec = importlib.util.spec_from_file_location("executive_demo_day_pack_generate", _SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_main_writes_four_drafts(tmp_path: Path) -> None:
    mod = _load()
    rc = mod.main(["--date", "2026-01-01", "--out-root", str(tmp_path)])
    assert rc == 0
    out_dir = tmp_path / "2026-01-01"
    files = sorted(p.name for p in out_dir.glob("*.md"))
    assert files == sorted(
        [
            "demo_day_script.md",
            "demo_assets_checklist.md",
            "executive_followup.md",
            "conversion_plan.md",
        ]
    )


def test_followup_is_draft_review_only() -> None:
    mod = _load()
    pack = mod.build_pack()
    assert "DRAFT" in pack["executive_followup.md"]
    assert "يدويًا" in pack["executive_followup.md"]
