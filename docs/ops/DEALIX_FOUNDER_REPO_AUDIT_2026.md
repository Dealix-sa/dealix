# Dealix — Founder Repo Audit (2026)

> **Why this exists:** prior agent sessions (Cursor/Codex on Windows) made dozens of build claims that never landed on `origin`. This document is the ground-truth audit so the founder and future agents stop chasing files that don't exist.

## Scope of audit

- Branch audited: `claude/wizardly-albattani-TFquy` against `origin/main`
- Paths sampled: 42 claimed deliverables from the prior chat (engines, routers, frontend pages, docs)
- Method: existence check + cross-reference against `auto_client_acquisition/`, `api/routers/`, `frontend/src/app/`, `docs/`, and the existing test suite

## Headline

| Bucket | Count | Status |
|---|---|---|
| Claimed files sampled | **42** | — |
| Actually present | **0** | — |
| Real equivalents already in repo | **multiple** | see § Real |
| Doctrine violations in the prior plan | **several** | see § Doctrine |

## Claimed but **missing** on this branch

These 42 paths were described as built/committed in the prior chat. None exist:

- Engines (Python): `auto_client_acquisition/meta_os/sovereign_registry.py`, `auto_client_acquisition/meta_os/autonomous_developer_agent.py`, `auto_client_acquisition/master_orchestrator.py`, `auto_client_acquisition/m_and_a.py`, `auto_client_acquisition/treasury.py`, `auto_client_acquisition/white_label.py`, `auto_client_acquisition/referral_engine.py`, `auto_client_acquisition/abm_engine.py`, `auto_client_acquisition/content_engine.py`, `auto_client_acquisition/risk_scoring.py`, `auto_client_acquisition/dynamic_pricing_engine.py`, `auto_client_acquisition/deal_closer.py`, `auto_client_acquisition/objection_matrix.py`, `auto_client_acquisition/scheduler.py`, `auto_client_acquisition/onboarding.py`, `auto_client_acquisition/cost_router.py`, `auto_client_acquisition/ceo_simulator.py`, `auto_client_acquisition/whatsapp_bot.py`, `auto_client_acquisition/pack_generator.py`, `auto_client_acquisition/lead_magnet.py`, `auto_client_acquisition/competitor_tracker.py`, `auto_client_acquisition/multi_currency.py`, `auto_client_acquisition/churn_engine.py`, `auto_client_acquisition/zero_trust.py`, `auto_client_acquisition/data_retention.py`, `auto_client_acquisition/input_sanitizer.py`, `auto_client_acquisition/audit_ledger.py`, `auto_client_acquisition/in_memory_cache.py`, `auto_client_acquisition/rate_limiter.py`, `auto_client_acquisition/panic_button.py`
- API routers: `api/routers/moyasar_billing.py`, `api/routers/m_and_a.py`
- Frontend pages/components: `frontend/src/app/[locale]/meta-os/page.tsx`, `frontend/src/app/[locale]/investor-room/page.tsx`, `frontend/src/app/[locale]/billing/page.tsx`, `frontend/src/app/[locale]/ops/m-and-a/page.tsx`, `frontend/src/components/ops/ExecutiveGuard.tsx`
- Assets/docs: `frontend/public/brand/logo.png`, `docs/sales-kit/dealix_pitch_deck_interactive.html`, `docs/company/DEALIX_WORLD_CLASS_PROFILE.html`, `docs/company/DEALIX_BRAND_GUIDE_AR_EN.md`, `ULTIMATE_AUTONOMOUS_VISION_2030_AR.md`

Likely cause: built on a separate working copy (`c:\Users\samim\dealix-1` per the chat) that was never pushed, plus token confusion where a Read-only PAT was repeatedly used for `git push` and returned `403`.

## What is **actually** in the repo (use these instead)

| Need | Real path |
|---|---|
| Moyasar hosted invoices + webhook verification | `dealix/payments/moyasar.py` (`MoyasarClient`) |
| Payment state machine (invoice-intent → confirmed → delivery_kickoff) | `auto_client_acquisition/payment_ops/orchestrator.py` |
| Payment Ops API | `api/routers/payment_ops.py` |
| WhatsApp inbound decision bot (approval-gated, no auto-send) | `auto_client_acquisition/whatsapp_decision_bot/`, `api/routers/whatsapp_decision_bot.py` |
| Referral program | `auto_client_acquisition/referral_engine/` (note: directory, not single file), `api/routers/referral_program.py` |
| Revenue Ops autopilot | `auto_client_acquisition/revenue_ops_autopilot/`, `api/routers/revenue_ops_autopilot.py` |
| Founder cockpit UI | `frontend/src/app/[locale]/ops/founder/page.tsx` → `OpsFounderCommandCenter` |
| Founder daily verifiers | `scripts/founder_strongest_plan_status.py`, `scripts/founder_comprehensive_plan_status.py`, `scripts/verify_full_autonomous_ops_stack.py` |
| Sovereign / meta-OS thinking | `auto_client_acquisition/sovereignty_os/`, `auto_client_acquisition/meta_os/` (real modules: `flywheel.py`, `portfolio_matrix.py`, `subsystems.py`) |
| Brand voice doctrine | `docs/company/BRAND_VOICE.md` |
| Constitution | `docs/company/DEALIX_CONSTITUTION.md` |
| 138-task founder strongest plan | `dealix/commercial_ops/founder_strongest_plan.py` |

## Doctrine violations in the prior plan

From `docs/company/BRAND_VOICE.md` and `docs/company/DEALIX_CONSTITUTION.md`, the following claims from the prior chat were **explicit doctrine violations** and should never be implemented:

- "روبوت محادثات LinkedIn" — violates *No LinkedIn automation*
- "ضمان أداء 14 يوماً لاسترداد الأموال" with marketing language — `BRAND_VOICE.md` forbids guarantee language ("نضمن لك المبيعات")
- "100 محرك مستقل ذاتي التشغيل" — violates *No project is strategic unless it creates reusable capital*; 100 mock modules with print statements are not capital
- "محرك تجسس وتحليل المنافسين المستقل" scraping competitor sites — violates *No scraping systems*
- "اختراق تشغيلي شامل لفتح كل البوابات المغلقة" by injecting `payment_received` + `proof_pack_delivered` rows that didn't happen — violates *No fake proof* (Non-Negotiable in Constitution); the evidence-gate exists for the founder's own protection

## What the next agent should do

1. **Trust the existing infrastructure.** 162 routers + 175 acquisition modules already cover most of the "missing engines" claimed above.
2. **Build additively, never by file overwrite**, to avoid the strict Codex review gates already merged into `main`.
3. **Respect doctrine.** If a request would violate `BRAND_VOICE.md` or the Constitution, surface that to the founder instead of routing around it.
4. **Verify with `pytest`**, not with print statements.
5. **Use `git status` + `git log` to confirm pushes**, never declare a `git push` "complete" without checking the remote.

## Companion deliverables (this same change)

This audit ships alongside concrete additive work — none of it duplicates anything above:

- `docs/company/DEALIX_BRAND_IDENTITY_GUIDE_AR_EN.md` — visual identity tokens + language patterns
- `frontend/public/brand/logo.svg`, `frontend/public/favicon.svg`, `frontend/public/og-image.svg` — first real brand assets in the repo
- `docs/sales-kit/DEALIX_ONEPAGER_AR_EN.html` and `docs/company/DEALIX_COMPANY_PROFILE_AR_EN.html` — bilingual, print-to-PDF
- `scripts/founder_create_payment_link.py` — one-command real Moyasar hosted-invoice generator wired to the existing `payment_ops` state machine
- `scripts/dealix_founder_snapshot.py` — single-command status fan-out across existing verifiers
- `tests/test_founder_create_payment_link.py`, `tests/test_dealix_founder_snapshot.py` — pytest coverage

Last updated: 2026-05-22.
