import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _v5util import run


def test_final_launch_control_is_go():
    # Runs the full safety-critical chain; exit 0 == GO.
    assert run("final_launch_control_verify.py").returncode == 0
