"""Regression tests for import-time crashes found by a full-repo import sweep.

Each of these modules raised at import/construction time before the fix:
  - integrations/gulf_phone.py, integrations/qiwa.py: mutable dataclass
    field defaults raised ValueError on any import.
  - dealix/commercial_ops/paths.py: missing path constants raised
    ImportError in founder_north_star.py / founder_excellence_os.py.
  - tools/patch_intake_contract.py: a botched edit left a syntax error.
"""
from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_gulf_phone_validation_errors_default_is_independent_per_instance():
    from integrations.gulf_phone import PhoneValidation

    a = PhoneValidation(phone="+966501234567", is_valid=True)
    b = PhoneValidation(phone="+966501234568", is_valid=True)

    assert a.errors == []
    a.errors.append("some error")
    assert b.errors == [], "mutable default must not be shared across instances"


def test_qiwa_nitaqat_status_levels_is_shared_class_constant():
    from integrations.qiwa import NitaqatStatus

    status = NitaqatStatus(cr_number="123", nitaqat_level="green", nitaqat_level_ar="")

    assert status.nitaqat_level_ar == "أخضر"
    assert status.is_compliant is True
    assert "green" in NitaqatStatus.NITAQAT_LEVELS


def test_commercial_ops_paths_defines_founder_config_constants():
    from dealix.commercial_ops import paths

    assert paths.FOUNDER_NORTH_STAR_YAML.name == "founder_north_star.yaml"
    assert paths.FOUNDER_EXCELLENCE_OS_YAML.name == "founder_excellence_os.yaml"
    assert paths.FOUNDER_WELLBEING_YAML.name == "founder_wellbeing.yaml"


def test_founder_north_star_status_importable_and_callable():
    from dealix.commercial_ops.founder_north_star import build_north_star_status

    status = build_north_star_status()
    assert "verdict" in status


def test_founder_excellence_os_status_importable_and_callable():
    from dealix.commercial_ops.founder_excellence_os import build_excellence_os_status

    status = build_excellence_os_status(skip_live=True)
    assert "overall_rag" in status


def test_patch_intake_contract_tool_has_no_syntax_error():
    source = (REPO_ROOT / "tools" / "patch_intake_contract.py").read_text(encoding="utf-8")
    ast.parse(source)  # raises SyntaxError if the botched edit regresses
