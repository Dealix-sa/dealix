# Dealix Production Readiness Checklist

_Last reviewed: 2026-05-26_

Use this checklist before any public launch, enterprise pilot, or production redeploy. The goal is to make launch readiness repeatable, evidence-based, and easy to audit.

## 1. Source and release integrity

- [ ] Default branch is protected or governed by a ruleset.
- [ ] CI is green on the target commit.
- [ ] The release commit is tagged.
- [ ] `CHANGELOG.md` or release notes explain the customer-visible changes.
- [ ] Rollback commit/tag/container image is known.
- [ ] Docker image digest is recorded for the deployed build.

## 2. Configuration and secrets

- [ ] `.env.example` matches the actual runtime settings used by API, workers, and frontend.
- [ ] No required production variable has duplicate or contradictory definitions.
- [ ] `APP_SECRET_KEY`, `ADMIN_API_KEYS`, payment secrets, webhook secrets, and provider keys are set through the hosting platform, not committed files.
- [ ] `CORS_ORIGINS` includes only expected production and staging origins.
- [ ] Public frontend variables do not expose privileged admin keys unless intentionally routed through a proxy.
- [ ] Secret scanning has run on the release diff.

## 3. Database and persistence

- [ ] Database URL points to the intended production database.
- [ ] Migrations apply cleanly from the previous production state.
- [ ] Alembic has a single head.
- [ ] Backup and restore process has been tested.
- [ ] Retention, suppression, and deletion workflows have test evidence.
- [ ] Event/proof ledgers use the intended backend mode for production.

## 4. API and backend

- [ ] `/health` returns healthy.
- [ ] Public endpoints are reachable without credentials only where intended.
- [ ] Admin endpoints reject missing or invalid credentials.
- [ ] Webhook HMAC or equivalent verification is active.
- [ ] OpenAPI schema exports successfully.
- [ ] Critical route smoke tests pass: pricing, checkout, demo request, leads, approval, and proof-pack flows.

## 5. Frontend and public surface

- [ ] Landing pages build successfully.
- [ ] Pricing, service catalog, and demo flows point to the correct API base URL.
- [ ] Arabic and English copy match the intended commercial claims.
- [ ] SEO audit has no required gaps.
- [ ] Analytics capture is configured and respects privacy posture.
- [ ] Browser console is free of production-blocking errors.

## 6. Trust, compliance, and claims

- [ ] No-overclaim register is updated for all public claims.
- [ ] PDPL consent, lawful basis, opt-out, retention, and suppression paths are represented in tests or operational scripts.
- [ ] ZATCA/payment claims reflect the actual deployed payment/invoice flow.
- [ ] High-stakes AI actions require the correct approval class.
- [ ] Evidence packs include source references, model/tool traceability, and bilingual summaries where required.
- [ ] External commitments cannot be sent automatically without policy approval.

## 7. Observability and incident response

- [ ] Structured logs are enabled in production.
- [ ] Request IDs are propagated through API and integrations.
- [ ] Sentry or equivalent error capture is configured if used.
- [ ] PostHog/Langfuse/metrics destinations are configured where enabled.
- [ ] Incident owner, escalation path, and rollback steps are known.
- [ ] Smoke-test URL and expected success payloads are documented.

## 8. Commercial readiness

- [ ] Pricing page and checkout amounts match approved offer packaging.
- [ ] Demo request workflow routes to the right inbox/CRM/calendar.
- [ ] Onboarding checklist is current.
- [ ] Customer-facing security/compliance answers are aligned with implemented controls.
- [ ] Support and refund/payment escalation processes are documented.

## Minimum launch gate

A commit is launch-ready only when:

1. CI is green.
2. `make docker-build` or platform image build succeeds.
3. `/health` and the core public endpoints pass smoke tests.
4. The production env contract is verified.
5. Security scanning has no unresolved high/critical findings.
6. The no-overclaim register has no stale customer-facing claims.
7. Rollback instructions are available to the operator running the launch.

## Arabic summary

قائمة الإطلاق هذه تمنع الاعتماد على الذاكرة. قبل أي إطلاق أو Pilot لازم يكون عندك: CI ناجح، متغيرات بيئة صحيحة، أسرار غير مكشوفة، قاعدة بيانات قابلة للترقية والرجوع، اختبارات دخان للـ API والواجهة، إثبات للامتثال، وم plan واضح للرجوع عند الفشل.
