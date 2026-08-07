from __future__ import annotations

import pytest


def test_admin_domain_retires_auto_send_even_when_env_is_enabled(monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_ENABLE_AUTO_SEND_LOW_RISK", "1")

    from api.routers import drafts
    from api.routers.domains import admin as admin_domain

    assert admin_domain.get_routers()
    assert drafts._auto_send_low_risk_enabled("auto_send_low_risk") is False
    assert drafts._auto_send_low_risk_enabled("draft_only") is False


@pytest.mark.asyncio
async def test_legacy_auto_send_adapter_is_fail_closed() -> None:
    from api.routers import drafts
    from api.routers.domains import admin as admin_domain

    assert admin_domain.get_routers()
    with pytest.raises(RuntimeError, match="auto_send_low_risk_retired"):
        await drafts.gmail_send_email(
            to_email="synthetic@example.com",
            subject="Synthetic",
            body_plain="Synthetic",
        )


def test_explicit_approved_send_route_remains_registered() -> None:
    from api.routers import email_send

    paths = {route.path for route in email_send.router.routes}
    assert "/api/v1/email/send-approved" in paths
