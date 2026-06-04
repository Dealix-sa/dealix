"""Website launch static check passes and enforces page/SEO/CTA presence."""

from __future__ import annotations

import site_launch_static_check as site
from _launch_util import ROOT


def test_site_check_passes():
    report = site.run("2099-01-01")
    assert report["passed"], report.get("errors")


def test_all_vertical_pages_exist():
    for slug in site.VERTICAL_SLUGS:
        assert (site.APP / "verticals" / slug / "page.tsx").exists()


def test_shared_data_has_ctas():
    data = (site.APP / "_launch" / "data.ts").read_text(encoding="utf-8")
    for label in site.CTA_LABELS:
        assert label in data
