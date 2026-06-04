"""API commercial static check: read-only endpoints, /health, no send routes."""

from __future__ import annotations

import api_commercial_static_check as apic


def test_api_check_passes():
    report = apic.run("2099-01-01")
    assert report["passed"], report.get("errors")


def test_readonly_router_exists():
    assert apic.READONLY_ROUTER.exists()


def test_readonly_router_is_get_only():
    text = apic.READONLY_ROUTER.read_text(encoding="utf-8")
    assert apic.SEND_ROUTE.search(text) is None
    assert apic.SEND_PATH.search(text) is None


def test_expected_endpoints_present():
    text = apic.READONLY_ROUTER.read_text(encoding="utf-8")
    for ep in apic.EXPECTED_ENDPOINTS:
        assert ep in text
