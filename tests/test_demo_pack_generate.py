"""V9 test: demo pack generator produces a safe, sandbox-only pack."""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts"))

import demo_pack_generate  # noqa: E402


def test_generate_creates_all_files(tmp_path) -> None:
    out_dir = demo_pack_generate.generate(out_root=tmp_path, pack_date="2026-01-01")
    expected = {"demo_script.md", "demo_companies.jsonl",
                "vertical_demo_map.md", "founder_demo_notes.md"}
    produced = {p.name for p in out_dir.iterdir()}
    assert expected <= produced


def test_demo_companies_are_sample_only(tmp_path) -> None:
    out_dir = demo_pack_generate.generate(out_root=tmp_path, pack_date="2026-01-01")
    rows = [json.loads(line) for line in
            (out_dir / "demo_companies.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert rows, "expected sample companies"
    for row in rows:
        # every demo company must be flagged as a synthetic example
        assert "EXAMPLE" in row["name"].upper() or "sample" in row.get("note", "").lower()


def test_founder_notes_mention_approval(tmp_path) -> None:
    out_dir = demo_pack_generate.generate(out_root=tmp_path, pack_date="2026-01-01")
    notes = (out_dir / "founder_demo_notes.md").read_text(encoding="utf-8").lower()
    assert "sandbox" in notes
    assert "guarant" not in notes or "never guaranteed" in notes
