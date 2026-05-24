"""Tests for founder commercial KPI registry apply script."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

_REPO = Path(__file__).resolve().parents[1]


def test_registry_loads_commercial_entries():
    reg = _REPO / "dealix/transformation/kpi_founder_commercial_registry.yaml"
    data = yaml.safe_load(reg.read_text(encoding="utf-8"))
    entries = data.get("commercial_entries") or {}
    assert "measured_customer_value_sar" in entries
    assert "conversion_discovery_to_pilot" in entries


def test_patch_snapshot_line_updates_value_and_ref():
    from scripts.apply_kpi_founder_commercial import _patch_snapshot_line

    text = """snapshots:
  conversion_discovery_to_pilot:
    value_numeric: null
    source_ref: ""
"""
    out = _patch_snapshot_line(text, "conversion_discovery_to_pilot", 18.5, "crm:test:2026")
    assert "value_numeric: 18.5" in out
    assert 'source_ref: "crm:test:2026"' in out


def test_verify_cutover_pr_body_requires_markers():
    from scripts.verify_cutover_pr_body import validate

    errs = validate("PROOF_LEDGER_BACKEND=postgres")
    assert len(errs) == 2
    ok = validate(
        "PROOF_LEDGER_BACKEND=dual\nexternal_signal: pilot_scope_locked\n"
        "contract_or_pilot_ref: acct-001"
    )
    assert ok == []


def test_forbidden_commercial_source_ref():
    from scripts.apply_kpi_founder_commercial import _validate_ref

    assert _validate_ref("x", "crm:REPLACE:foo") is not None
    assert _validate_ref("x", "crm:hubspot:deal:1;period=2026-Q1") is None


def test_check_import_readiness_missing_file(tmp_path: Path) -> None:
    from scripts.apply_kpi_founder_commercial import check_import_readiness

    missing = tmp_path / "absent_import.yaml"
    verdict, messages = check_import_readiness(missing)
    assert verdict == "WAITING_ON_FOUNDER_CRM_EXPORT"
    assert any("missing import file" in msg for msg in messages)


def test_check_import_readiness_placeholder_data(tmp_path: Path) -> None:
    from scripts.apply_kpi_founder_commercial import check_import_readiness

    placeholder = tmp_path / "import.yaml"
    placeholder.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "entries": {
                    "measured_customer_value_sar": {
                        "value_numeric": 0.0,
                        "source_ref": "crm:hubspot:not_synced_yet",
                    },
                    "conversion_discovery_to_pilot": {
                        "value_numeric": None,
                        "source_ref": "<fill_from_crm>",
                    },
                    "approval_cycle_time_hours": {
                        "value_numeric": 0,
                        "source_ref": "TBD",
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    verdict, messages = check_import_readiness(placeholder)
    assert verdict == "WAITING_ON_FOUNDER_CRM_EXPORT"
    assert messages, "expected at least one placeholder message"


def test_check_import_readiness_real_data(tmp_path: Path) -> None:
    from scripts.apply_kpi_founder_commercial import check_import_readiness

    real = tmp_path / "import.yaml"
    real.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "entries": {
                    "measured_customer_value_sar": {
                        "value_numeric": 124000.0,
                        "source_ref": "crm:hubspot:deal:12345;period=2026-Q1",
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    verdict, _ = check_import_readiness(real)
    assert verdict == "READY"


def test_main_refuses_when_import_missing(monkeypatch, tmp_path: Path) -> None:
    """CLI integration: missing file => verdict printed, exit 2."""
    from scripts import apply_kpi_founder_commercial as mod

    missing = tmp_path / "absent.yaml"
    monkeypatch.setattr(mod, "_IMPORT", missing)
    monkeypatch.setattr(sys, "argv", ["apply_kpi_founder_commercial.py"])
    rc = mod.main()
    assert rc == 2


def test_main_refuses_when_placeholder(monkeypatch, tmp_path: Path) -> None:
    from scripts import apply_kpi_founder_commercial as mod

    placeholder = tmp_path / "import.yaml"
    placeholder.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "entries": {
                    "measured_customer_value_sar": {
                        "value_numeric": 0.0,
                        "source_ref": "<fill_from_crm>",
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "_IMPORT", placeholder)
    monkeypatch.setattr(sys, "argv", ["apply_kpi_founder_commercial.py"])
    rc = mod.main()
    assert rc == 2


def test_main_check_mode_returns_waiting_code(monkeypatch, tmp_path: Path) -> None:
    from scripts import apply_kpi_founder_commercial as mod

    missing = tmp_path / "absent.yaml"
    monkeypatch.setattr(mod, "_IMPORT", missing)
    monkeypatch.setattr(sys, "argv", ["apply_kpi_founder_commercial.py", "--check"])
    rc = mod.main()
    assert rc == 2


def test_main_applies_when_real_data(monkeypatch, tmp_path: Path) -> None:
    """With real data + dry-run we should hit the apply branch and exit 0."""
    from scripts import apply_kpi_founder_commercial as mod

    real_import = tmp_path / "import.yaml"
    real_import.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "entries": {
                    "measured_customer_value_sar": {
                        "value_numeric": 124000.0,
                        "source_ref": "crm:hubspot:deal:12345;period=2026-Q1",
                    },
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "_IMPORT", real_import)
    # Use a tmp registry + baselines so we don't mutate the repo's real files.
    reg = tmp_path / "registry.yaml"
    reg.write_text(
        yaml.safe_dump(
            {
                "commercial_entries": {
                    "measured_customer_value_sar": {
                        "value_numeric": None,
                        "source_ref": "",
                    },
                }
            }
        ),
        encoding="utf-8",
    )
    baselines = tmp_path / "baselines.yaml"
    baselines.write_text(
        "snapshots:\n"
        "  measured_customer_value_sar:\n"
        "    value_numeric: null\n"
        '    source_ref: ""\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(mod, "_REGISTRY", reg)
    monkeypatch.setattr(mod, "_BASELINES", baselines)
    monkeypatch.setattr(sys, "argv", ["apply_kpi_founder_commercial.py", "--dry-run"])
    rc = mod.main()
    assert rc == 0
