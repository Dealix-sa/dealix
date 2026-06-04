import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _v5util import run, ensure_chain


def test_quality_gate_passes():
    ensure_chain()
    assert run("commercial_quality_gate.py").returncode == 0
