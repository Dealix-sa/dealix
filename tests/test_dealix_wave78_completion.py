"""Tests for the Wave 7/8 founder-operations completion pack.

Covers the public functions introduced by the new scripts:

- ``create_customer_workspace.create_workspace`` writes 12 files.
- ``run_dealix_e2e_dry_run`` stage functions return PASS structures and the
  full chain reports an overall PASS.
- ``founder_daily_command.build_daily_command`` / report writer produce output
  and degrade gracefully on an empty data directory.
- The four verifier ``check_*`` functions return well-formed structured results.

All tests are offline and fast. Scripts are loaded by file path so the test does
not depend on ``scripts`` being an importable package.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load(name: str, filename: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


# --- create_customer_workspace -------------------------------------------------


def test_create_workspace_writes_twelve_files(tmp_path: Path) -> None:
    mod = _load("ws_mod", "create_customer_workspace.py")
    workspace = mod.create_workspace("Dry Run Client", force=True, base_dir=tmp_path)
    files = sorted(p.name for p in workspace.iterdir() if p.is_file())
    assert len(files) == 12
    assert files[0] == "00_intake.md"
    assert "11_upsell_recommendation.md" in files


def test_create_workspace_files_carry_governance_status(tmp_path: Path) -> None:
    mod = _load("ws_mod2", "create_customer_workspace.py")
    workspace = mod.create_workspace("Gov Check", force=True, base_dir=tmp_path)
    for path in workspace.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert "governance_status: draft" in text


def test_create_workspace_refuses_overwrite_without_force(tmp_path: Path) -> None:
    mod = _load("ws_mod3", "create_customer_workspace.py")
    mod.create_workspace("Repeat Client", force=True, base_dir=tmp_path)
    with pytest.raises(FileExistsError):
        mod.create_workspace("Repeat Client", force=False, base_dir=tmp_path)


def test_slugify_is_filesystem_safe() -> None:
    mod = _load("ws_mod4", "create_customer_workspace.py")
    assert mod.slugify("ACME  Trading Co.!!") == "acme-trading-co"
    assert mod.slugify("") == "customer"


# --- e2e dry run ---------------------------------------------------------------


def test_e2e_stage_functions_pass() -> None:
    mod = _load("e2e_mod", "run_dealix_e2e_dry_run.py")
    for stage in (
        mod.stage_target,
        mod.stage_outreach_approval,
        mod.stage_diagnostic,
        mod.stage_offer,
        mod.stage_paid_sprint,
        mod.stage_proof_pack,
        mod.stage_founder_daily_command,
    ):
        result = stage()
        assert result["status"] == "PASS", result
        assert "stage" in result and "detail" in result


def test_e2e_outreach_never_auto_sends() -> None:
    mod = _load("e2e_mod2", "run_dealix_e2e_dry_run.py")
    result = mod.stage_outreach_approval()
    assert result["status"] == "PASS"
    assert result["requires_approval"] is True


def test_e2e_upsell_blocked_without_proof_pack() -> None:
    mod = _load("e2e_mod3", "run_dealix_e2e_dry_run.py")
    blocked = mod.stage_upsell_recommendation(proof_pack_ready=False)
    assert blocked["status"] == "BLOCKER"
    allowed = mod.stage_upsell_recommendation(proof_pack_ready=True)
    assert allowed["status"] == "PASS"


def test_e2e_offer_is_on_ladder() -> None:
    mod = _load("e2e_mod4", "run_dealix_e2e_dry_run.py")
    result = mod.stage_offer()
    assert result["offer"] in mod.OFFER_LADDER


def test_e2e_run_all_overall_pass() -> None:
    mod = _load("e2e_mod5", "run_dealix_e2e_dry_run.py")
    results = mod.run_all_stages()
    assert mod.overall_status(results) == "PASS"


# --- founder daily command -----------------------------------------------------


def test_build_daily_command_degrades_on_empty_dir(tmp_path: Path) -> None:
    mod = _load("fdc_mod", "founder_daily_command.py")
    command = mod.build_daily_command(revenue_dir=tmp_path)
    assert command["degraded"] is True
    assert command["revenue_events_today_count"] == 0
    assert len(command["next_actions"]) == 3
    assert command["founder_action_en"]
    assert command["founder_action_ar"]


def test_build_daily_command_counts_proof_packs(tmp_path: Path) -> None:
    mod = _load("fdc_mod2", "founder_daily_command.py")
    (tmp_path / "revenue_events.jsonl").write_text(
        '{"event": "proof_pack_delivered", "date": "2020-01-01", "mode": "dry_run"}\n'
        "\n"
        "not-json\n",
        encoding="utf-8",
    )
    (tmp_path / "payments.jsonl").write_text("", encoding="utf-8")
    command = mod.build_daily_command(revenue_dir=tmp_path)
    assert command["degraded"] is False
    assert command["proof_packs_delivered_count"] == 1


def test_render_markdown_and_write_report() -> None:
    mod = _load("fdc_mod3", "founder_daily_command.py")
    command = mod.build_daily_command()
    md = mod.render_markdown(command)
    assert "Founder Daily Command" in md
    path = mod.write_report(command)
    assert path.is_file()
    assert path.read_text(encoding="utf-8")


# --- verifiers -----------------------------------------------------------------


def test_check_positioning_structure() -> None:
    mod = _load("pos_mod", "verify_dealix_positioning.py")
    result = mod.check_positioning()
    assert result["verdict"] in {"PASS", "FAIL"}
    assert len(result["items"]) == len(mod.POSITIONING_DOCS)
    for item in result["items"]:
        assert item["status"] in {"PASS", "FAIL"}


def test_check_modules_present_on_disk() -> None:
    mod = _load("modstat_mod", "verify_dealix_module_status.py")
    result = mod.check_modules()
    # All canonical modules are present in this repo.
    assert result["verdict"] == "PASS", result["missing"]
    statuses = {i["module"]: i["status"] for i in result["items"]}
    assert "governance_os" in statuses


def test_check_growth_assets_structure() -> None:
    mod = _load("growth_mod", "verify_dealix_growth_assets.py")
    result = mod.check_growth_assets()
    assert result["verdict"] in {"PASS", "FAIL"}
    labels = {i["label"] for i in result["items"]}
    assert "first_30_targets_csv" in labels


def test_check_launch_readiness_scores() -> None:
    mod = _load("launch_mod", "verify_dealix_launch_readiness.py")
    result = mod.check_launch_readiness()
    assert result["verdict"] in {"PASS", "NOT-READY"}
    assert result["total"] == 5
    assert 0 <= result["score"] <= result["total"]
