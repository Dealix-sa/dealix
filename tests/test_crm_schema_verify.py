import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import json
from _v5util import run, ROOT


def test_crm_schema_verify_passes():
    assert run("commercial_crm_schema_verify.py").returncode == 0


def test_external_send_forbidden_in_schema():
    s = json.loads((ROOT / "config" / "crm_pipeline_schema.json").read_text())
    assert s["external_send"] == "forbidden"
    assert s["invariants"]["no_crm_push_send"] is True
