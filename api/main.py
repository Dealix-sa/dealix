"""
FastAPI application entry point.
نقطة دخول تطبيق FastAPI.
"""

from __future__ import annotations

# value_os, data_os and agent_os routers are imported defensively: an
# optional router with a broken module-level import must not abort app
# boot for every other endpoint. A skipped router is logged at
# registration time with the full traceback so silent failures are
# investigable. In development DEALIX_STRICT_OPTIONAL_ROUTERS=1 promotes
# any skipped optional router to a startup error.
import os as _os
import traceback as _traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.middleware import (
    AuditLogMiddleware,
    ETagMiddleware,
    RateLimitHeadersMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
)
from api.routers import (
    admin_tenants,
    agent_mesh_os,
    assurance_contract_os,
    auth,
    compliance_product,
    compliance_status,
    control_plane_os,
    cost_tracking,
    customer_usage,
    customer_webhooks,
    enterprise_pmo,
    human_ai_os,
    jobs,
    nps,
    org_graph_os,
    pdpl,
    pdpl_dsar,
    referral_program,
    revenue_metrics,
    runtime_safety_os,
    sandbox_os,
    saudi_prospect_search,
    sector_intel,
    self_evolving_os,
    service_setup,
    simulation_os,
    tenant_theming,
    value_engine_os,
    zatca,
)
from api.routers import audit_export as audit_export_router

# Wave 13 — Full Ops Productization routers
from api.routers import bottleneck_radar as bottleneck_radar_router
from api.routers import business_metrics_board as business_metrics_board_router
from api.routers import (
    business_now as business_now_router,
)
from api.routers import customer_success_scores as customer_success_scores_router
from api.routers import deliverables as deliverables_router

# Wave 12.7 — Intelligence Layer + Expansion Engine routers
from api.routers import expansion_engine as expansion_engine_router
from api.routers import founder_dashboard as founder_dashboard_router

# Wave 14 — Canonical Trust MVP + Retainer Engine (Phase 2)
from api.routers import friction_log as friction_log_router
from api.routers import integration_capability as integration_capability_router
from api.routers import intelligence_layer as intelligence_layer_router
from api.routers import service_catalog as service_catalog_router

# 90-day commercial activation — Wave 14B
from api.routers import sprint_runner as sprint_runner_router
from api.routers import (
    transformation_os as transformation_os_router,
)

# ── Domain router aggregators (replaces 80+ flat imports) ─────────
from api.routers.domains import admin as admin_domain
from api.routers.domains import agents as agents_domain
from api.routers.domains import analytics as analytics_domain
from api.routers.domains import compliance as compliance_domain
from api.routers.domains import customers as customers_domain
from api.routers.domains import deprecated as deprecated_domain
from api.routers.domains import sales as sales_domain
from api.routers.domains import webhooks as webhooks_domain

_OPTIONAL_ROUTER_ERRORS: dict[str, str] = {}


def _import_optional_router(name: str, module_path: str):
    try:
        return __import__(module_path, fromlist=[name])
    except Exception as exc:
        _OPTIONAL_ROUTER_ERRORS[name] = (
            f"{type(exc).__name__}: {exc}\n{_traceback.format_exc()}"
        )
        return None


value_os_router = _import_optional_router("value_os", "api.routers.value_os")
data_os_router = _import_optional_router("data_os", "api.routers.data_os")
# Wave 14F — Agent OS
agent_os_router = _import_optional_router("agent_os", "api.routers.agent_os")
# Wave 14J — Commercial wiring map (source of truth for landing↔backend)
from api.routers import commercial_map as commercial_map_router
# Wave 15B — Commercial chain (diagnostic → warm-intro → pilot → proof → payment → upsell)
from api.routers import commercial as commercial_chain_router

# Wave 15 — Founder launch-status (single-pane production readiness)
from api.routers import founder_launch_status as founder_launch_status_router

# Enterprise Foundation Core — platform_core enterprise-loop proof endpoints
from api.routers import platform_foundation as platform_foundation_router
# Autonomous product distribution engine
from api.routers import autonomous_distribution as autonomous_distribution_router

# Wave 16 — Customer Intelligence + Market Intelligence + Onboarding
from api.routers import customer_health_scoring as customer_health_scoring_router
from api.routers import market_intelligence as market_intelligence_router
from api.routers import onboarding as onboarding_router

# 90-day commercial plan — KPI Dashboard (admin-gated comprehensive metrics)
from api.routers import kpi_dashboard as kpi_dashboard_router
# Weekly business reports (admin-gated, approval-required)
from api.routers import weekly_reports as weekly_reports_router

from api.security import APIKeyMiddleware, setup_rate_limit
from core.config.settings import get_settings
from core.errors import AICompanyError
from core.logging import configure_logging, get_logger


def _validate_production_secrets(settings: Settings) -> None:  # type: ignore[name-defined]
    """
    Fail fast if production is started with insecure defaults.
    يرفض تشغيل الإنتاج بإعدادات غير آمنة.
    """
    if not settings.is_production:
        return
    secret_val = settings.app_secret_key.get_secret_value()
    if secret_val in ("change-me", "CHANGE_ME_to_64_byte_hex", "", "changeme"):
        raise RuntimeError(
            "SECURITY: APP_SECRET_KEY is set to the default placeholder. "
            "Generate a real key: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    jwt_val = settings.jwt_secret_key.get_secret_value()
    if "change-me" in jwt_val or len(jwt_val) < 32:
        raise RuntimeError(
            "SECURITY: JWT_SECRET_KEY is insecure in production. "
            "Generate a real key: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    import os
    if not os.getenv("API_KEYS", "").strip():
        raise RuntimeError(
            "SECURITY: API_KEYS is empty in production. "
            "Set a comma-separated list of secret API keys."
        )
    if not os.getenv("ADMIN_API_KEYS", "").strip():
        raise RuntimeError(
            "SECURITY: ADMIN_API_KEYS is empty in production. "
            "Set a comma-separated list of admin API keys for /api/v1/admin/* endpoints."
        )


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """App startup/shutdown hook."""
    configure_logging()
    log = get_logger(__name__)
    settings = get_settings()

    # ── Security: fail fast on insecure production config ───────
    _validate_production_secrets(settings)

    log.info(
        "app_startup",
        app=settings.app_name,
        version=settings.app_version,
        env=settings.app_env,
    )
    # Auto-create tables ONLY in development/test — in staging/production
    # run `alembic upgrade head` instead (init_db create_all is excluded).
    if settings.app_env in ("development", "test"):
        try:
            from db.session import init_db
            await init_db()
            log.info("db_init_complete")
        except Exception as exc:
            log.warning("db_init_skipped", error=str(exc))
    else:
        log.info("db_init_skipped", reason="use_alembic_migrations")
    yield
    log.info("app_shutdown")


def create_app() -> FastAPI:
    """FastAPI factory."""
    settings = get_settings()

    _OPENAPI_TAGS = [
        {"name": "Sales", "description": "Lead intake, pipeline, outreach, pricing, revenue."},
        {"name": "Customers", "description": "Customer success, CRM, portals, inbox, support."},
        {"name": "Agents", "description": "LLM gateway, AI workforce, observability, safety, delivery."},
        {"name": "Admin", "description": "Health, config, founder ops, roles, diagnostics."},
        {"name": "Compliance", "description": "PDPL, security, privacy, data quality, reliability."},
        {"name": "Analytics", "description": "Growth, company brain, GTM, market intelligence, radar."},
        {"name": "Webhooks", "description": "Inbound/outbound webhooks — WhatsApp, HubSpot, n8n."},
        {"name": "Deprecated", "description": "Legacy versioned endpoints (v3/v6/v7/v10/v11) — to be removed in v2.0."},
        {"name": "root", "description": "Root discovery endpoint."},
    ]

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Multi-agent AI platform for the Saudi Arabian market.\n\n"
            "**Phase 8**: Auto Client Acquisition — intake, ICP match, "
            "pain extraction, qualification, CRM sync, booking, proposals.\n\n"
            "**Phase 9**: Autonomous Growth — sector intel, content, distribution, "
            "enrichment, competitor analysis, market research.\n\n"
            "**Phase 10 / v3**: Autonomous Saudi Revenue OS — revenue memory, "
            "safe agent runtime, market radar, compliance OS, revenue science, "
            "and Sami Personal Strategic Operator."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
        openapi_tags=_OPENAPI_TAGS,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "X-API-Key", "X-Request-ID", "Content-Type", "Accept"],
    )
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RateLimitHeadersMiddleware)
    app.add_middleware(ETagMiddleware)
    app.add_middleware(AuditLogMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(APIKeyMiddleware)
    setup_rate_limit(app)

    try:
        from dealix.observability import instrument_fastapi, setup_sentry, setup_tracing

        setup_sentry()
        setup_tracing(service_name=settings.app_name, version=settings.app_version)
        instrument_fastapi(app)
    except Exception:  # pragma: no cover
        pass

    @app.exception_handler(AICompanyError)
    async def ai_company_error_handler(_: Request, exc: AICompanyError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": exc.__class__.__name__, "detail": str(exc)},
        )

    # Trust layer — /version + /api/v1/meta (public probes; register once at root)
    from api.routers import platform_meta as platform_meta_router

    app.include_router(platform_meta_router.router)

    from api.routers import mcp_tools as mcp_tools_router

    app.include_router(mcp_tools_router.router)

    # ── Routers registered by domain (replaces 90 flat app.include_router calls) ─
    _DOMAIN_GROUPS = [
        admin_domain,
        sales_domain,
        customers_domain,
        agents_domain,
        compliance_domain,
        analytics_domain,
        webhooks_domain,
        deprecated_domain,
    ]
    for domain in _DOMAIN_GROUPS:
        for router in domain.get_routers():
            app.include_router(router)

    # ── Enterprise additions ───────────────────────────────────────
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(jobs.router, prefix="/api/v1")
    app.include_router(zatca.router)
    app.include_router(pdpl.router)
    app.include_router(compliance_product.router)

    # ── Wave 12.7 — Intelligence Layer + Expansion Engine ─────────
    # Both routers self-prefix /api/v1/intelligence and /api/v1/expansion-engine.
    app.include_router(intelligence_layer_router.router)
    app.include_router(expansion_engine_router.router)

    # ── Wave 13 — Full Ops Productization ─────────────────────────
    # Self-prefix /api/v1/services. Registry-only; no live actions.
    app.include_router(service_catalog_router.router)
    # Self-prefix /api/v1/deliverables. State-machine-gated.
    app.include_router(deliverables_router.router)
    # Self-prefix /api/v1/customer-success. 5-score read-only.
    app.include_router(customer_success_scores_router.router)
    # Self-prefix /api/v1/bottleneck-radar. Read-only.
    app.include_router(bottleneck_radar_router.router)
    # Self-prefix /api/v1/integrations. Truth registry; no live actions.
    app.include_router(integration_capability_router.router)
    # Self-prefix /api/v1/metrics. Read-only; tenant-isolated for {handle}.
    app.include_router(business_metrics_board_router.router)
    # Wave 13B — Founder ops-autopilot (War Room, cockpit, strongest-plan, evidence)
    from api.routers.revenue_ops_autopilot import AUTOPILOT_ROUTERS

    for _autopilot_router in AUTOPILOT_ROUTERS:
        app.include_router(_autopilot_router)
    # Wave 7 W7.5 — Tenant theming: GET tenant theme.css + POST admin theme update
    app.include_router(tenant_theming.router)
    # Wave 7 W7.2 — Sector Intelligence (R4 productization)
    app.include_router(sector_intel.router)
    # Wave 7 W7.3 — Admin tenants: CRUD for tenant management (R6 enabler)
    app.include_router(admin_tenants.router)
    # Wave 8 W8.1 — Bespoke AI Service Setup intake (R5 productization)
    app.include_router(service_setup.router)
    # Wave 8 W8.3 — Customer-facing usage dashboard
    app.include_router(customer_usage.router)
    # Wave 9 W9.1 — Enterprise PMO (R7 productization)
    app.include_router(enterprise_pmo.router)
    # Wave 9 W9.6 — Live compliance status (PDPL+ZATCA posture, public read-only)
    app.include_router(compliance_status.router)
    # Wave 9 W9.8 — Saudi B2B prospect search (read-only public + PDPL-safe view)
    app.include_router(saudi_prospect_search.router)
    # Wave 9 W9.9 — PDPL DSAR (data subject access/rectify/port/erase)
    app.include_router(pdpl_dsar.router)
    # Wave 11 W11.2 — Cost tracking (per-tier + admin summary)
    app.include_router(cost_tracking.router)
    # Wave 12 W12.1 — Customer-side webhook subscriptions (Dealix→customer)
    app.include_router(customer_webhooks.router)
    # Wave 13 W13.7 — Revenue metrics dashboard (MRR/ARR/NRR/churn/cohort)
    app.include_router(revenue_metrics.router)
    # Wave 13 W13.13 — Customer referral program (5K SAR per closed deal)
    app.include_router(referral_program.router)
    # Wave 13 W13.4 — NPS survey + detractor intervention
    app.include_router(nps.router)
    # Wave 14 — Canonical Trust MVP + Retainer Engine (Phase 2)
    app.include_router(friction_log_router.router)
    app.include_router(transformation_os_router.router, prefix="/api/v1")
    app.include_router(business_now_router.router, prefix="/api/v1")
    if value_os_router is not None:
        app.include_router(value_os_router.router)
    # Wave 14B — Commercial activation: CSV upload for the Data Pack offer
    if data_os_router is not None:
        app.include_router(data_os_router.router)
    app.include_router(sprint_runner_router.router)
    app.include_router(founder_dashboard_router.router)
    app.include_router(audit_export_router.router)
    # Wave 14F — Agent OS (admin-gated)
    if agent_os_router is not None:
        app.include_router(agent_os_router.router)
    _strict_optional = _os.getenv("DEALIX_STRICT_OPTIONAL_ROUTERS", "").lower() in (
        "1", "true", "yes",
    )
    for _name, _err in _OPTIONAL_ROUTER_ERRORS.items():
        get_logger(__name__).error(
            "optional_router_skipped",
            router=_name,
            error=_err,
            hint="Set DEALIX_STRICT_OPTIONAL_ROUTERS=1 in dev to fail fast.",
        )
        if _strict_optional:
            raise RuntimeError(
                f"Optional router '{_name}' failed to import and "
                f"DEALIX_STRICT_OPTIONAL_ROUTERS=1.\n{_err}"
            )
    # Wave 14J — Commercial wiring map (public)
    app.include_router(commercial_map_router.router)
    # Wave 15B — Commercial chain: diagnostic → warm-intro → pilot → proof → payment → upsell
    app.include_router(commercial_chain_router.router)
    # Wave 15 — Founder launch-status (admin /launch-status + public /launch-status/public)
    app.include_router(founder_launch_status_router.router)
    # Systems 26–35 — Enterprise Control Plane hardening
    app.include_router(control_plane_os.router)
    app.include_router(agent_mesh_os.router)
    app.include_router(assurance_contract_os.router)
    app.include_router(sandbox_os.router)
    app.include_router(org_graph_os.router)
    app.include_router(runtime_safety_os.router)
    app.include_router(simulation_os.router)
    app.include_router(human_ai_os.router)
    app.include_router(value_engine_os.router)
    app.include_router(self_evolving_os.router)
    # Enterprise Foundation Core — /api/v1/platform/* loop proof endpoints
    app.include_router(platform_foundation_router.router)
    # Autonomous product distribution — /api/v1/autonomous-distribution/*
    app.include_router(autonomous_distribution_router.router)

    # Wave 16 — Customer Intelligence + Market Intelligence + Onboarding
    app.include_router(customer_health_scoring_router.router)
    app.include_router(market_intelligence_router.router)
    app.include_router(onboarding_router.router)

    # 90-day commercial plan — KPI Dashboard (admin-gated comprehensive metrics)
    app.include_router(kpi_dashboard_router.router)
    # Weekly business reports — /api/v1/reports
    app.include_router(weekly_reports_router.router)

    # Saudi Revenue Advisor — Saudi-market-specific B2B revenue guidance
    from api.routers import saudi_revenue_advisor as saudi_revenue_advisor_router
    app.include_router(saudi_revenue_advisor_router.router)

    # Vision 2030 Alignment — Saudi market strategic narrative builder
    from api.routers import vision2030_alignment as vision2030_alignment_router
    app.include_router(vision2030_alignment_router.router)

    # Wave 17 — Payment webhooks + Founder alert review
    from api.routers import payments_webhook as payments_webhook_router
    from api.routers import founder_alerts as founder_alerts_router

    app.include_router(payments_webhook_router.router)
    app.include_router(founder_alerts_router.router)

    # Wave 17 — Saudi sector intelligence catalogue + match API
    from api.routers import sector_intelligence as sector_intelligence_router

    app.include_router(sector_intelligence_router.router)

    # 90-day commercial plan — Customer Lifecycle Management
    from api.routers import customer_lifecycle as customer_lifecycle_router

    app.include_router(customer_lifecycle_router.router)

    # Wave 17 — Retainer Operations (renewal, upgrade, at-risk, MRR breakdown)
    from api.routers import retainer_ops as retainer_ops_router

    app.include_router(retainer_ops_router.router)

    # Wave 17 — ZATCA Readiness Assessment (open lead-gen tool)
    from api.routers import zatca_readiness as zatca_readiness_router

    app.include_router(zatca_readiness_router.router)

    # 90-day commercial plan — PDPL Readiness Assessment (open lead-gen tool)
    from api.routers import pdpl_readiness as pdpl_readiness_router

    app.include_router(pdpl_readiness_router.router)

    # 90-day commercial plan — Lead Intelligence + Growth Intelligence
    from api.routers import lead_intelligence as lead_intelligence_router
    from api.routers import growth_intelligence as growth_intelligence_router

    app.include_router(lead_intelligence_router.router)
    app.include_router(growth_intelligence_router.router)

    # Wave 17 — Health Intelligence (portfolio, trends, alerts, benchmarks)
    from api.routers import health_intelligence as health_intelligence_router

    app.include_router(health_intelligence_router.router)

    # 90-day commercial plan — Pricing Intelligence + Pipeline Ops (admin-gated)
    from api.routers import pricing_intelligence as pricing_intelligence_router
    from api.routers import pipeline_ops as pipeline_ops_router

    app.include_router(pricing_intelligence_router.router)
    app.include_router(pipeline_ops_router.router)

    # Master Cockpit — founder intelligence aggregator (pulse, kpis, alerts, approvals)
    from api.routers import master_cockpit as master_cockpit_router

    app.include_router(master_cockpit_router.router)

    # Competitor Intelligence + Sales Playbook (admin-gated)
    from api.routers import competitor_intel as competitor_intel_router
    from api.routers import sales_playbook as sales_playbook_router

    app.include_router(competitor_intel_router.router)
    app.include_router(sales_playbook_router.router)

    # Onboarding Operations — 12-step client onboarding workflow
    from api.routers import onboarding_ops as onboarding_ops_router

    app.include_router(onboarding_ops_router.router)

    # Referral Intelligence — referral tracking and program management
    from api.routers import referral_intelligence as referral_intelligence_router

    app.include_router(referral_intelligence_router.router)

    # Subscription Operations — lifecycle management (pause/cancel/reactivate)
    from api.routers import subscription_ops as subscription_ops_router

    app.include_router(subscription_ops_router.router)

    # Client Health Ops — 6-dimension scoring
    from api.routers import client_health_ops as client_health_ops_router

    app.include_router(client_health_ops_router.router)

    # Invoice Operations — ZATCA-native lifecycle
    from api.routers import invoice_ops as invoice_ops_router

    app.include_router(invoice_ops_router.router)

    # Team Operations — roster, hiring plan, capacity
    from api.routers import team_ops as team_ops_router

    app.include_router(team_ops_router.router)

    # Proof Pack Operations — draft→review→approved→delivered
    from api.routers import proof_pack_ops as proof_pack_ops_router

    app.include_router(proof_pack_ops_router.router)

    # Churn Prevention Operations — risk scoring, intervention logging
    from api.routers import churn_prevention_ops as churn_prevention_ops_router

    app.include_router(churn_prevention_ops_router.router)

    # Revenue Intelligence Ops — MRR breakdown, leakage, forecast, NRR
    from api.routers import revenue_intelligence_ops as revenue_intelligence_ops_router
    app.include_router(revenue_intelligence_ops_router.router)

    # Ops Metrics — unified KPI aggregator (snapshot, pulse, benchmarks, weekly-summary)
    from api.routers import ops_metrics_ops as ops_metrics_ops_router
    app.include_router(ops_metrics_ops_router.router)

    # Notification Operations — multi-type notifications with read/create/delete
    from api.routers import notification_ops as notification_ops_router
    app.include_router(notification_ops_router.router)

    # Analytics Operations — feature adoption, content, sprint performance, funnel
    from api.routers import analytics_ops as analytics_ops_router
    app.include_router(analytics_ops_router.router)

    # AI Training Operations — model training pipeline management
    from api.routers import ai_training_ops as ai_training_ops_router
    app.include_router(ai_training_ops_router.router)

    # Client Portal Operations — self-service account and deliverable views
    from api.routers import client_portal_ops as client_portal_ops_router
    app.include_router(client_portal_ops_router.router)

    # ZATCA Compliance Operations — Phase 2 e-invoicing
    from api.routers import zatca_compliance_ops as zatca_compliance_ops_router
    app.include_router(zatca_compliance_ops_router.router)

    # Saudi Revenue Advisor — Saudi-market-specific B2B revenue guidance
    from api.routers import saudi_revenue_advisor as saudi_revenue_advisor_router
    app.include_router(saudi_revenue_advisor_router.router)

    # Vision 2030 Alignment — Saudi market strategic narrative builder
    from api.routers import vision2030_alignment as vision2030_alignment_router
    app.include_router(vision2030_alignment_router.router)

    # Hijri Calendar — Gregorian↔Hijri conversion + Saudi national holidays
    from api.routers import hijri_calendar as hijri_calendar_router
    app.include_router(hijri_calendar_router.router)

    # Prayer Schedule — prayer-time-aware business scheduling for Saudi cities
    from api.routers import prayer_schedule as prayer_schedule_router
    app.include_router(prayer_schedule_router.router)

    # SME Accelerator — Saudi SME programs + Vision 2030 funding readiness
    from api.routers import sme_accelerator as sme_accelerator_router
    app.include_router(sme_accelerator_router.router)

    # Islamic Finance — Murabaha/Ijara structures + payment calculators
    from api.routers import islamic_finance as islamic_finance_router
    app.include_router(islamic_finance_router.router)

    # Saudization Compliance — Nitaqat band checker + upgrade path
    from api.routers import saudization_compliance as saudization_compliance_router
    app.include_router(saudization_compliance_router.router)

    # ROI Calculator — AI automation ROI, NPV, IRR, payback in SAR
    from api.routers import roi_calculator as roi_calculator_router
    app.include_router(roi_calculator_router.router)

    # Executive Briefing — persona-tailored one-page C-level briefings (Saudi context)
    from api.routers import executive_briefing as executive_briefing_router
    app.include_router(executive_briefing_router.router)

    # Saudi Objection Handler — sales objections with Saudi cultural context
    from api.routers import saudi_objection_handler as saudi_objection_handler_router
    app.include_router(saudi_objection_handler_router.router)

    # Deal Scoring — MEDDPICC deal scoring adapted for Saudi B2B
    from api.routers import deal_scoring as deal_scoring_router
    app.include_router(deal_scoring_router.router)

    # Market Sizing — Saudi B2B AI sector TAM/SAM/SOM intelligence
    from api.routers import market_sizing as market_sizing_router
    app.include_router(market_sizing_router.router)

    # Proposal Builder — structured bilingual B2B proposal generator
    from api.routers import proposal_builder as proposal_builder_router
    app.include_router(proposal_builder_router.router)

    # Customer Success Playbook — lifecycle playbooks + account health scoring
    from api.routers import customer_success_playbook as customer_success_playbook_router
    app.include_router(customer_success_playbook_router.router)

    # Content Calendar — Saudi B2B annual events, Ramadan strategy, monthly themes
    from api.routers import content_calendar as content_calendar_router
    app.include_router(content_calendar_router.router)

    # Competitive Positioning — battle cards + positioning briefs vs. competitor categories
    from api.routers import competitive_positioning as competitive_positioning_router
    app.include_router(competitive_positioning_router.router)

    # Account Plan — strategic account planning framework for Saudi B2B enterprise deals
    from api.routers import account_plan as account_plan_router
    app.include_router(account_plan_router.router)

    # Lead Scoring — 8-criteria lead scoring with grade bands and SLA targets
    from api.routers import lead_scoring as lead_scoring_router
    app.include_router(lead_scoring_router.router)

    # Pipeline Analytics — Saudi B2B pipeline health, stage playbooks, conversion benchmarks
    from api.routers import pipeline_analytics as pipeline_analytics_router
    app.include_router(pipeline_analytics_router.router)

    # Partner Ecosystem — ZATCA ISVs, cloud providers, SAMA FinTechs, accelerators, SIs
    from api.routers import partner_ecosystem as partner_ecosystem_router
    app.include_router(partner_ecosystem_router.router)

    # Onboarding Checklist — tier-specific client onboarding with PDPL compliance tracking
    from api.routers import onboarding_checklist as onboarding_checklist_router
    app.include_router(onboarding_checklist_router.router)

    # KPI Tracker — Saudi B2B KPI library with benchmarks and snapshot calculator
    from api.routers import kpi_tracker as kpi_tracker_router
    app.include_router(kpi_tracker_router.router)

    # Prospect Intelligence — ICP profiles, trigger events, prospect qualification
    from api.routers import prospect_intelligence as prospect_intelligence_router
    app.include_router(prospect_intelligence_router.router)

    # Saudi Sector Intelligence — 8 sector profiles, procurement thresholds, compliance map
    from api.routers import saudi_sector_intelligence as saudi_sector_intelligence_router
    app.include_router(saudi_sector_intelligence_router.router)

    # Pricing Psychology — pricing principles, anchor scripts, ROI simulator
    from api.routers import pricing_psychology as pricing_psychology_router
    app.include_router(pricing_psychology_router.router)

    # Email Templates — Saudi B2B outreach templates for human review and manual send
    from api.routers import email_templates as email_templates_router
    app.include_router(email_templates_router.router)

    # Meeting Agenda — Saudi B2B meeting agenda builder with cultural protocol
    from api.routers import meeting_agenda as meeting_agenda_router
    app.include_router(meeting_agenda_router.router)

    # Annual Business Review — structured ABR framework with renewal recommendation
    from api.routers import annual_business_review as annual_business_review_router
    app.include_router(annual_business_review_router.router)

    # Revenue Forecast — Saudi B2B seasonality-adjusted MRR forecasting
    from api.routers import revenue_forecast as revenue_forecast_router
    app.include_router(revenue_forecast_router.router)

    # Client Reporting — weekly brief, monthly intelligence report, QBR deck outlines
    from api.routers import client_reporting as client_reporting_router
    app.include_router(client_reporting_router.router)

    # Proof Pack Builder — evidence packages for proposals, renewals, and expansions
    from api.routers import proof_pack as proof_pack_router
    app.include_router(proof_pack_router.router)

    # Negotiation Playbook — Saudi B2B negotiation principles, concessions, scenario briefs
    from api.routers import negotiation_playbook as negotiation_playbook_router
    app.include_router(negotiation_playbook_router.router)

    # Champion Development — archetype profiles, development stages, health assessment
    from api.routers import champion_development as champion_development_router
    app.include_router(champion_development_router.router)

    # Win/Loss Analysis — weighted deal scoring, loss guidance, debrief templates
    from api.routers import win_loss_analysis as win_loss_analysis_router
    app.include_router(win_loss_analysis_router.router)

    # Demo Script — demo flow, types, Saudi cultural rules, objection responses
    from api.routers import demo_script as demo_script_router
    app.include_router(demo_script_router.router)

    # Account Expansion — signals, playbooks, expansion score assessment
    from api.routers import account_expansion as account_expansion_router
    app.include_router(account_expansion_router.router)

    # Onboarding Playbook — phases, risks, plan builder
    from api.routers import onboarding_playbook as onboarding_playbook_router
    app.include_router(onboarding_playbook_router.router)

    # Retention Risk — churn factors, early-warning indicators, risk assessment
    from api.routers import retention_risk as retention_risk_router
    app.include_router(retention_risk_router.router)

    # Pipeline Velocity — stage benchmarks, stall detection, urgency scoring
    from api.routers import pipeline_velocity as pipeline_velocity_router
    app.include_router(pipeline_velocity_router.router)

    # Territory Intelligence — Saudi region profiles, sector penetration, territory plan builder
    from api.routers import territory_intelligence as territory_intelligence_router
    app.include_router(territory_intelligence_router.router)

    # Competitive Battlecard — sections, differentiators, objection counters, battlecard builder
    from api.routers import competitive_battlecard as competitive_battlecard_router
    app.include_router(competitive_battlecard_router.router)

    # Renewal Management — timeline milestones, risk thresholds, upsell triggers, renewal assessment
    from api.routers import renewal_management as renewal_management_router
    app.include_router(renewal_management_router.router)

    # Partner Referral — tiers, onboarding steps, commission rules, earnings calculator
    from api.routers import partner_referral as partner_referral_router
    app.include_router(partner_referral_router.router)

    # Data Quality Ops — 5 DQ dimensions, ZATCA requirements, weighted assessment
    from api.routers import data_quality_ops as data_quality_ops_router
    app.include_router(data_quality_ops_router.router)

    # Sales Cadence — 4 cadence templates, Saudi communication rules, plan builder
    from api.routers import sales_cadence as sales_cadence_router
    app.include_router(sales_cadence_router.router)

    # Contract Intelligence — clauses, Saudi requirements, compliance scoring
    from api.routers import contract_intelligence as contract_intelligence_router
    app.include_router(contract_intelligence_router.router)

    # Customer Journey — 6 stages, touchpoint library, journey mapping
    from api.routers import customer_journey as customer_journey_router
    app.include_router(customer_journey_router.router)

    # Proposal Builder — bilingual proposal outline generator per tier
    from api.routers import proposal_builder as proposal_builder_router
    app.include_router(proposal_builder_router.router)

    # KPI Dashboard v2 — 8 Saudi KPIs, benchmark comparison, overall grade
    from api.routers import kpi_dashboard as kpi_dashboard_module
    app.include_router(kpi_dashboard_module.router_v2)

    @app.get("/", tags=["root"])
    async def root() -> dict[str, object]:
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "status": "operational",
            "env": settings.app_env,
            "docs": "/docs",
            "health": "/health",
            "v3_command_center": "/api/v1/v3/command-center/snapshot",
            "personal_operator_daily_brief": "/api/v1/personal-operator/daily-brief",
            "personal_operator_launch_report": "/api/v1/personal-operator/launch-report",
            "business_pricing": "/api/v1/business/pricing",
            "decision_passport_golden_chain": "/api/v1/decision-passport/golden-chain",
            "decision_passport_evidence_levels": "/api/v1/decision-passport/evidence-levels",
            "revenue_os_catalog": "/api/v1/revenue-os/catalog",
            "founder_summary_daily": "/api/v1/founder-summary",
            "founder_summary_weekly_agenda": "/api/v1/founder-summary/weekly/agenda",
            "revenue_intelligence_import": "/api/v1/revenue-intelligence/{eid}/import",
            "proof_pack_generate": "/api/v1/proof-pack/{eid}/generate",
            "diagnostic_intent": "/api/v1/diagnostic/intent",
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "api.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.is_development,
    )
