import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from _v5util import run


def test_seed_leads_validate_passes():
    assert run("commercial_seed_leads_validate.py").returncode == 0


def test_lead_intake_validate_passes():
    assert run("commercial_lead_intake_validate.py").returncode == 0
