import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _v5util import run, ensure_chain


def test_compliance_gate_passes():
    ensure_chain()
    run("commercial_safety_audit.py")
    assert run("commercial_compliance_gate.py").returncode == 0
