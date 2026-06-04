import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import json
from _v5util import run, ROOT, ensure_chain


def test_startup_os_verify_passes():
    ensure_chain()
    assert run("startup_os_verify.py").returncode == 0
    r = json.loads((ROOT / "outputs" / "startup_os" / "startup_os_verification.json").read_text())
    assert r["status"] == "PASS"
    assert r["critical_failures"] == []
