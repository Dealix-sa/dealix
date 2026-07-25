"""Static contracts for the browser-facing SaaS signup and dashboard journey."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_signup_loads_canonical_plans_and_establishes_session() -> None:
    source = _read("apps/web/app/signup/page.tsx")

    assert 'apiUrl("/api/v1/onboarding/plans")' in source
    assert 'apiUrl("/api/v1/onboarding/signup")' in source
    assert 'apiUrl("/api/v1/auth/login")' in source
    assert "persistSession(tokens" in source
    assert "signup.tenant_slug" in source
    assert "const plans = [" not in source
    assert 'id: "scale"' not in source
    assert 'price: "199"' not in source
    assert 'price: "599"' not in source


def test_login_and_dashboard_use_canonical_runtime_api() -> None:
    login = _read("apps/web/app/login/page.tsx")
    dashboard = _read("apps/web/app/[tenant]/dashboard/page.tsx")
    entry = _read("apps/web/app/dashboard/page.tsx")

    assert 'apiUrl("/api/v1/auth/login")' in login
    assert "persistSession(data" in login
    assert 'apiUrl("/api/v1/customer/dashboard/")' in dashboard
    assert "Authorization: `Bearer ${token}`" in dashboard
    assert '"x-tenant-id"' not in dashboard.lower()
    assert 'apiUrl("/api/v1/auth/me")' in entry
    assert "profile.tenant_id" in entry


def test_next_config_keeps_signup_active_and_proxies_api() -> None:
    source = _read("apps/web/next.config.js")

    assert "NEXT_PUBLIC_DEALIX_API_BASE" in source
    assert 'source: "/api/v1/:path*"' in source
    assert "destination: `${dealixApiBase}/api/v1/:path*`" in source
    assert 'source: "/signup"' not in source


def test_runtime_helper_never_embeds_platform_api_key() -> None:
    source = _read("apps/web/lib/runtime-api.ts")

    assert "NEXT_PUBLIC_DEALIX_API_BASE" in source
    assert "NEXT_PUBLIC_API_URL" in source
    assert "dealix_access_token" in source
    assert "dealix_refresh_token" in source
    assert "X-API-Key" not in source
    assert "ADMIN_API" not in source


def test_backend_exposes_self_serve_plans_and_jwt_customer_paths() -> None:
    onboarding = _read("api/routers/onboarding.py")
    middleware = _read("api/security/api_key.py")

    assert 'SELF_SERVE_PLAN_SLUGS = ("free", "starter", "growth")' in onboarding
    assert '@router.get("/plans"' in onboarding
    assert '"tenant_slug": result["tenant"].slug' in onboarding
    assert '"/api/v1/customer/",' in middleware
    assert "current_user=Depends(get_current_user)" in onboarding
    assert "current_user=Depends(require_tenant_admin)" in onboarding
