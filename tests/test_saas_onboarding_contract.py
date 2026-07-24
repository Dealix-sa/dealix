"""Static contracts for the SaaS onboarding security boundary."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICE_PATH = ROOT / "dealix" / "onboarding" / "service.py"
ROUTER_PATH = ROOT / "api" / "routers" / "onboarding.py"


def _source(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    ast.parse(source)
    return source


def test_signup_uses_canonical_tenant_roles() -> None:
    source = _source(SERVICE_PATH)

    assert "DEFAULT_TENANT_ROLES" in source
    assert "Role.TENANT_ADMIN.value" in source
    assert 'name="owner"' not in source
    assert 'permissions=["*:*"]' not in source


def test_team_invite_uses_single_use_invite_record() -> None:
    source = _source(SERVICE_PATH)

    assert "UserInviteRecord(" in source
    assert "create_invite_token(" in source
    assert "hash_token(invite_token)" in source
    assert "token_expires_at(invite_token)" in source
    assert 'hashed_password=""' not in source
    assert "UserRecord(" not in source.split("async def invite_team_member", 1)[1]


def test_team_invite_is_admin_gated_and_never_claims_send() -> None:
    source = _source(ROUTER_PATH)

    assert "Depends(require_tenant_admin)" in source
    assert "manual_share_required" not in source or "delivery_status" in source
    assert "Nothing was sent." in source
    assert "لم يتم إرسال أي رسالة" in source
    assert "send_email" not in source
    assert "send_invite_email" not in source


def test_signup_response_matches_current_verification_contract() -> None:
    service = _source(SERVICE_PATH)
    router = _source(ROUTER_PATH)

    assert "is_verified=True" in service
    assert '"requires_email_verification": False' in service
    assert '"requires_email_verification": result["requires_email_verification"]' in router
