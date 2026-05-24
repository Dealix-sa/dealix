"""Tests for the M-3 inline-dashboard wiring in scripts/dealix_morning_digest.py.

Phase 1b (M-3) embeds the live dashboard snapshot inline in the founder
digest body so the morning email contains everything — no external link,
no separate attachment. These tests assert:

  1. The digest body in --print mode contains the dashboard section
     header and a fenced ```json block.
  2. Inline mode (no --dashboard-file) renders without raising and
     without hitting the network.
  3. The --dashboard-file flag overrides the inline producer.

Offline. Stdlib only. Runs in < 5s.
"""
from __future__ import annotations

import asyncio
import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "dealix_morning_digest.py"
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))


def _load_digest_module():
    """Load the digest script as a module (mirrors test_dealix_morning_digest.py)."""
    spec = importlib.util.spec_from_file_location(
        "dealix_morning_digest_m3", str(SCRIPT)
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


digest = _load_digest_module()


def _fake_loop() -> dict:
    return {
        "schema_version": 1,
        "generated_at": "2026-05-24T07:00:00+00:00",
        "decisions": [{"title_ar": "demo", "title_en": "demo"}],
        "service_to_promote": {},
        "partner_focus": {},
        "seo_gap_pages": [],
        "perimeter_status": {},
        "open_loops": [],
        "guardrails": {
            "no_live_send": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "approval_required_for_external_actions": True,
        },
    }


def test_render_dashboard_section_contains_header_and_fenced_json():
    section = digest.render_dashboard_section({"hello": "world"})
    assert digest.DASHBOARD_SECTION_HEADER in section
    assert "```json" in section
    # The payload itself is round-trippable through json.loads.
    fenced = section.split("```json", 1)[1].split("```", 1)[0].strip()
    assert json.loads(fenced) == {"hello": "world"}


def test_load_dashboard_inline_returns_dict_offline():
    """Inline producer must return a dict and never raise — either the
    real snapshot or the deterministic stub."""
    payload = digest._load_dashboard_inline()
    assert isinstance(payload, dict)


def test_print_mode_embeds_dashboard_section(capsys):
    """In --print mode the body printed to stdout must contain the M-3
    dashboard section. Proves inline mode works end-to-end with no
    --dashboard-file and no network."""
    sys.argv = ["dealix_morning_digest.py", "--print"]
    args = digest.parse_args()

    with patch.object(
        digest.daily_growth_loop, "build_today", return_value=_fake_loop()
    ):
        result = asyncio.run(digest._build_and_send(args))

    out = capsys.readouterr().out
    assert result.success is True
    assert result.provider == "print_only"
    assert "Live Dashboard Snapshot" in out
    assert "```json" in out


def test_dashboard_file_flag_overrides_inline(tmp_path, capsys):
    """--dashboard-file PATH must read JSON from disk instead of
    invoking the inline producer."""
    payload = {"override": True, "marker": "from_file"}
    f = tmp_path / "dash.json"
    f.write_text(json.dumps(payload), encoding="utf-8")

    sys.argv = [
        "dealix_morning_digest.py",
        "--print",
        "--dashboard-file",
        str(f),
    ]
    args = digest.parse_args()

    sentinel_called = {"hit": False}

    def _should_not_be_called():
        sentinel_called["hit"] = True
        return {"unused": True}

    with patch.object(
        digest.daily_growth_loop, "build_today", return_value=_fake_loop()
    ), patch.object(
        digest, "_load_dashboard_inline", side_effect=_should_not_be_called
    ):
        result = asyncio.run(digest._build_and_send(args))

    out = capsys.readouterr().out
    assert result.success is True
    assert sentinel_called["hit"] is False, (
        "inline producer must not run when --dashboard-file is provided"
    )
    assert "from_file" in out


def test_parse_args_exposes_dashboard_file_flag(tmp_path):
    target = tmp_path / "x.json"
    sys.argv = ["dealix_morning_digest.py", "--dashboard-file", str(target)]
    args = digest.parse_args()
    assert args.dashboard_file == target
    # Default (no flag) is None.
    sys.argv = ["dealix_morning_digest.py", "--print"]
    args2 = digest.parse_args()
    assert args2.dashboard_file is None


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
