import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _v5util import run, ensure_chain


def test_launch_readiness_passes():
    ensure_chain()
    assert run("commercial_launch_readiness.py").returncode == 0
