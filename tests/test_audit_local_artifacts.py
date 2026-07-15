"""Unit tests for scripts/audit_local_artifacts.py classifier."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "audit_local_artifacts.py"

spec = importlib.util.spec_from_file_location("audit_local_artifacts", SCRIPT_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
sys.modules["audit_local_artifacts"] = mod
spec.loader.exec_module(mod)


def test_keep_real_static_asset_in_whitelisted_path(tmp_path: Path) -> None:
    rel = "docs/sales-kit/new_onepager.html"
    f = tmp_path / rel
    f.parent.mkdir(parents=True)
    f.write_text("<html>one pager</html>")
    finding = mod.classify(tmp_path, rel)
    assert finding.bucket == "KEEP_REAL"


def test_reject_stub_by_filename_phrase(tmp_path: Path) -> None:
    rel = "auto_client_acquisition/sovereign_registry.py"
    f = tmp_path / rel
    f.parent.mkdir(parents=True)
    f.write_text("def list_engines(): return []\n")
    finding = mod.classify(tmp_path, rel)
    assert finding.bucket == "REJECT_STUB"
    assert "sovereign_registry" in finding.stub_hits


def test_reject_stub_by_weak_phrase_in_diff_mode(tmp_path: Path) -> None:
    """In diff mode (a new file from a parallel local copy), WEAK phrases such
    as ceo_simulator are enough to reject — these patterns are the prior
    session's signature."""
    rel = "auto_client_acquisition/ceo_simulator.py"
    f = tmp_path / rel
    f.parent.mkdir(parents=True)
    f.write_text("def directive(): return 'scale ARR'\n")
    finding = mod.classify(tmp_path, rel)
    assert finding.bucket == "REJECT_STUB"
    assert "ceo_simulator" in finding.stub_hits


def test_weak_phrase_does_not_match_in_canonical_scan(tmp_path: Path) -> None:
    """In canonical-scan mode (auditing the committed repo) WEAK phrases are
    legitimate vocabulary and must not trigger. Only STRONG phrases count."""
    rel = "auto_client_acquisition/meta_os/flywheel.py"
    f = tmp_path / rel
    f.parent.mkdir(parents=True)
    f.write_text("# meta_os module — flywheel utilities\n")
    finding = mod.classify(tmp_path, rel, canonical_scan=True)
    assert finding.bucket != "REJECT_STUB"


def test_strong_phrase_matches_in_canonical_scan(tmp_path: Path) -> None:
    """Even in canonical-scan mode, a STRONG phrase like sovereign_registry
    indicates leaked theater debt and must be flagged."""
    rel = "auto_client_acquisition/sovereign_registry.py"
    f = tmp_path / rel
    f.parent.mkdir(parents=True)
    f.write_text("def list_engines(): return []\n")
    finding = mod.classify(tmp_path, rel, canonical_scan=True)
    assert finding.bucket == "REJECT_STUB"
    assert "sovereign_registry" in finding.stub_hits


def test_self_exempt_paths_are_not_flagged(tmp_path: Path) -> None:
    """The audit tool itself, its tests, and the reality-check doc legitimately
    enumerate the stub phrases. They must never flag themselves."""
    rel = "scripts/audit_local_artifacts.py"
    f = tmp_path / rel
    f.parent.mkdir(parents=True)
    # Mimic the script enumerating the phrases.
    f.write_text("# sovereign_registry execute_50_storm 100-engine sovereign\n")
    finding = mod.classify(tmp_path, rel)
    assert finding.bucket != "REJECT_STUB"


def test_reject_evidence_ledger_file(tmp_path: Path) -> None:
    rel = "data/evidence_events_tracker.csv"
    f = tmp_path / rel
    f.parent.mkdir(parents=True)
    f.write_text("date,event\n2026-05-19,payment_received\n")
    finding = mod.classify(tmp_path, rel)
    assert finding.bucket == "REJECT_STUB"
    assert "doctrine" in finding.reason


def test_review_for_unhinted_python(tmp_path: Path) -> None:
    rel = "scripts/import_lead_helper.py"
    f = tmp_path / rel
    f.parent.mkdir(parents=True)
    f.write_text("def main(): pass\n")
    finding = mod.classify(tmp_path, rel)
    assert finding.bucket == "REVIEW"


def test_review_for_yaml_outside_whitelist(tmp_path: Path) -> None:
    rel = "config_random.yaml"
    f = tmp_path / rel
    f.write_text("foo: bar\n")
    finding = mod.classify(tmp_path, rel)
    assert finding.bucket == "REVIEW"


def test_keep_real_brand_png_under_public_brand(tmp_path: Path) -> None:
    rel = "frontend/public/brand/logo.png"
    f = tmp_path / rel
    f.parent.mkdir(parents=True)
    f.write_bytes(b"\x89PNG\r\n\x1a\n")
    finding = mod.classify(tmp_path, rel)
    assert finding.bucket == "KEEP_REAL"
