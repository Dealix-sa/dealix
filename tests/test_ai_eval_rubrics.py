import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import json
from _v5util import run, ROOT, ensure_chain


def test_rubrics_load_and_have_hard_gates():
    r = json.loads((ROOT / "config" / "ai_eval_rubrics.json").read_text())
    comp = r["rubrics"]["compliance"]
    assert any(d.get("hard_gate") for d in comp)


def test_sample_eval_compliance_is_100pct():
    ensure_chain()
    assert run("ai_eval_sample_drafts.py").returncode == 0
