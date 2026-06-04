import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _v5util import run


def test_api_no_send_static_check_passes():
    assert run("api_commercial_static_check.py").returncode == 0
