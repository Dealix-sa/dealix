"""Launch readiness reports GO when configs, docs, and data are present."""

from __future__ import annotations

import commercial_launch_readiness as readiness
from _launch_util import ROOT


def test_configs_and_docs_present():
    report = readiness.run("2099-01-01")
    # Critical checks (configs, seed data, docs) must pass even before a draft run.
    critical = [c for c in report["checks"] if c["critical"]]
    failed = [c for c in critical if not c["passed"]]
    assert failed == [], failed


def test_required_configs_listed():
    assert "commercial_launch.json" in readiness.REQUIRED_CONFIGS
    assert "crm_pipeline_schema.json" in readiness.REQUIRED_CONFIGS
