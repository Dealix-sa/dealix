import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _v5util import run, ensure_chain


def test_safety_audit_passes():
    ensure_chain()
    assert run("commercial_safety_audit.py").returncode == 0


def test_safety_audit_report_clean():
    import json
    d = ensure_chain()
    r = json.loads((d / "safety_audit.json").read_text())
    assert r["ok"] is True
    assert r["flag_violation_count"] == 0
    assert r["phrase_violation_count"] == 0
