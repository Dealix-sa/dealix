import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pathlib import Path
from _v5util import ROOT

APP = ROOT / "apps" / "web" / "app"


def test_commercial_page_has_sar():
    assert "SAR" in (APP / "commercial" / "page.tsx").read_text()


def test_all_vertical_pages_exist():
    for slug in ["facilities-management", "contracting-project-controls",
                 "real-estate-property-ops", "legal-professional-services",
                 "consulting-training-b2b"]:
        assert (APP / "verticals" / slug / "page.tsx").exists()


def test_no_roi_guarantee_in_pricing():
    txt = (APP / "pricing" / "page.tsx").read_text().lower()
    assert "guaranteed roi" not in txt
