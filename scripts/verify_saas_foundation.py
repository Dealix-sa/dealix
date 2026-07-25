#!/usr/bin/env python3
"""Verify Dealix SaaS foundation contracts without external services.

This verifier proves repository-level SaaS foundations only. It deliberately
reports production activation gates separately because secrets, domains,
deployments, migrations, and live smoke evidence cannot be inferred from code.
"""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    evidence: str


def _read(root: Path, relative: str) -> str:
    path = root / relative
    source = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        ast.parse(source)
    return source


def evaluate(root: Path) -> dict[str, object]:
    models = _read(root, "db/models.py")
    subscription_models = _read(root, "db/models_subscription.py")
    auth = _read(root, "api/routers/auth.py")
    main = _read(root, "api/main.py")
    onboarding_router = _read(root, "api/routers/onboarding.py")
    onboarding_service = _read(root, "dealix/onboarding/service.py")
    invite_email = _read(root, "core/email/invites.py")
    deploy_identity = _read(root, "core/config/deployment_identity.py")
    health_router = _read(root, "api/routers/health.py")
    platform_meta = _read(root, "api/routers/platform_meta.py")

    invite_section = onboarding_service.split("async def invite_team_member", 1)[1]
    checks = [
        Check(
            "tenant_model",
            "class TenantRecord" in models and "tenant_id" in models,
            "TenantRecord and tenant-scoped records exist",
        ),
        Check(
            "rbac_and_sessions",
            "class RoleRecord" in models
            and "class RefreshTokenRecord" in models
            and "DEFAULT_TENANT_ROLES" in onboarding_service,
            "RBAC, refresh sessions, and canonical role bootstrap exist",
        ),
        Check(
            "subscription_and_usage",
            all(
                token in subscription_models
                for token in (
                    "class PlanRecord",
                    "class SubscriptionRecord",
                    "class InvoiceRecord",
                    "class UsageRecord",
                )
            ),
            "plans, subscriptions, invoices, and usage metering exist",
        ),
        Check(
            "self_serve_signup",
            '@router.post("/signup"' in onboarding_router
            and "Role.TENANT_ADMIN.value" in onboarding_service,
            "self-serve signup creates a canonical tenant administrator",
        ),
        Check(
            "safe_team_invites",
            "UserInviteRecord(" in invite_section
            and "hash_token(invite_token)" in invite_section
            and 'hashed_password=""' not in invite_section
            and "Depends(require_tenant_admin)" in onboarding_router
            and "_VALID_ROLE_NAMES = {role.value for role in Role}" in onboarding_service,
            "single-use hashed invites; tenant-role constrained; no placeholder users",
        ),
        Check(
            "approval_first_invite_delivery",
            'os.getenv("EMAIL_ALLOW_LIVE_SEND", "false")' in invite_email
            and "if not live_invite_email_enabled():" in invite_email
            and "blocked_by_policy=True" in invite_email
            and "send_email: bool = False" in onboarding_router
            and "if not send_email:" in onboarding_router
            and "await send_invite_email(" in onboarding_router
            and "manual_share_required" in onboarding_router,
            "invite email requires per-action approval plus operator policy; manual fallback remains",
        ),
        Check(
            "canonical_legacy_invite",
            "def _install_auth_invite_compatibility()" in onboarding_router
            and 'getattr(route_item, "path", None) == "/invite"' in onboarding_router
            and "auth_module.router.routes = retained_routes" in onboarding_router
            and 'name="legacy_auth_invite_compatibility"' in onboarding_router
            and main.index("    auth,")
            < main.index("from api.routers import onboarding as onboarding_router")
            < main.index('app.include_router(auth.router, prefix="/api/v1")'),
            "legacy auth invite is replaced before router inclusion and delegates to canonical flow",
        ),
        Check(
            "deployment_identity",
            "VERCEL_GIT_COMMIT_SHA" in deploy_identity
            and "RAILWAY_GIT_COMMIT_SHA" in deploy_identity
            and "GIT_SHA" in deploy_identity
            and "resolve_deployment_git_sha" in health_router
            and "resolve_deployment_git_sha" in platform_meta,
            "health and metadata prefer platform-managed deployment identity",
        ),
        Check(
            "auth_lifecycle",
            all(
                route in auth
                for route in (
                    '@router.post("/login"',
                    '@router.post("/refresh"',
                    '@router.post("/logout"',
                    '@router.post("/mfa/setup"',
                    '@router.post("/password/reset"',
                )
            ),
            "login, token rotation, logout, MFA, and password reset exist",
        ),
        Check(
            "audit_and_pdpl",
            "class AuditLogRecord" in models
            and "class ConsentRequestRecord" in models
            and "class SuppressionRecord" in models,
            "audit, consent, and suppression records exist",
        ),
        Check(
            "billing_proof",
            "class PaymentRecord" in models
            and "class ProofReportRecord" in models,
            "payment evidence and customer proof records exist",
        ),
        Check(
            "approval_first_outbound",
            "class OutreachDraftRecord" in models
            and "class OutboundMessageRecord" in models
            and 'default="draft_only"' in models,
            "outbound is modeled through drafts and controlled execution",
        ),
    ]

    passed = all(check.passed for check in checks)
    return {
        "foundation_status": "READY" if passed else "NOT_READY",
        "production_activation_status": "OPERATOR_GATES_REQUIRED",
        "checks": [asdict(check) for check in checks],
        "operator_gates": [
            {
                "issue": 898,
                "action": "restore Railway deploy credential and prove backend deploy",
            },
            {
                "issue": 884,
                "action": "synchronize the dedicated protected-route smoke key",
            },
            {
                "issue": 894,
                "action": "complete Vercel frontend / Railway API domain cutover",
            },
        ],
        "claim_boundary": (
            "READY proves repository SaaS foundations only; production-ready requires "
            "migrations, deployment, protected-route smoke, and domain evidence."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = evaluate(args.root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"SaaS foundation: {result['foundation_status']}")
        for check in result["checks"]:
            mark = "PASS" if check["passed"] else "FAIL"
            print(f"[{mark}] {check['name']}: {check['evidence']}")
        print(f"Production activation: {result['production_activation_status']}")
        for gate in result["operator_gates"]:
            print(f"- #{gate['issue']}: {gate['action']}")
        print(result["claim_boundary"])

    return 0 if result["foundation_status"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
