# Dealix Stage Status

**القاعدة:** المرحلة لا تعتبر منتهية إلا إذا صار عندها `PASS` في هذا الملف + دليل داخل الريبو + اختبار/تحقق خارجي.

_Last rendered: 2026-05-22 20:58 UTC by `scripts/render_stage_status.py`_

> هذا الملف يُولَّد آلياً. لا تعدّله يدويًا — عدّل الأدلة في الريبو ثم نفّذ `make stage-status`.

## Decision

**SELL_ONLY_READY_SERVICES**

Sales-blocking gates:
- Gate 3 Product Readiness (MVP) = BLOCKED
- Gate 6 Sales Readiness = FIX

Sale rule: must PASS Gates 0, 1, 2, 4, 5, 6 + Gate 3 as MVP.

## Master Table

<!-- AUTO:STAGE_STATUS_START -->
| Gate | Name | Status | Score | Threshold | Owner | Evidence | Next Action |
|---:|---|:---:|---:|---:|---|---|---|
| 0 | Founder Clarity | ✅ PASS | 100 | 85 | Sami (Founder) | `docs/company/POSITIONING.md` | Re-read POSITIONING.md monthly; lock if unchanged. |
| 1 | Offer Readiness | ✅ PASS | 100 | 85 | Sami + Delivery | `docs/services/lead_intelligence_sprint/offer.md` | All three starter offers PASS — keep offer.md scope + pricing locked. |
| 2 | Delivery Readiness | ✅ PASS | 100 | 85 | Delivery | `docs/delivery/DELIVERY_STANDARD.md` | Dry-run handoff on a fake client every 2 weeks. |
| 3 | Product Readiness (MVP) | 🔴 BLOCKED | 100 | 80 | Engineering | `DEALIX_COMPANY_OPERATIONAL_STATE.md` | Unblock Moyasar (Sami sends activated sk_live_/sk_test_ key). |
| 4 | Governance Readiness | ✅ PASS | 100 | 90 | Governance | `dealix/registers/no_overclaim.yaml` | Review claims register monthly; PII spot-check weekly. |
| 5 | Demo Readiness | ✅ PASS | 100 | 85 | Sami + Sales | `demos/lead_intelligence_demo/` | Record 5-minute walkthrough per demo pack. |
| 6 | Sales Readiness | 🟡 FIX | 100 | 85 | Sami (Sales) | `docs/sales/SALES_PLAYBOOK.md` | Sami sends DM #1 from launch_content_queue.md and logs sent_at. |
| 7 | Client Delivery Readiness | ✅ PASS | 100 | 85 | Delivery | `docs/delivery/client_onboarding/welcome_message.md` | First paid client triggers full onboarding walk-through. |
| 8 | Retainer Readiness | ✅ PASS | 100 | 85 | Sami + Delivery | `docs/delivery/RETAINER_READINESS.md` | Activate when first sprint closes successfully. |
| 9 | Scale Readiness | ✅ PASS | 100 | 85 | Sami (Ops) | `docs/ops/DAILY_OPERATING_LOOP.md` | Defer until first 3 paid clients delivered with NPS ≥ 8. |
| 10 | World-Class Readiness | 🟡 FIX | 0 | 85 | Sami (Strategy) | `docs/company/WORLD_CLASS_READINESS_AR.md` | Do not measure until MRR is stable. |
<!-- AUTO:STAGE_STATUS_END -->

## Per-Gate Detail

### Gate 0 — Founder Clarity

- **Status:** ✅ PASS
- **Score:** 100/100 (Pass ≥ 85)
- **Owner:** Sami (Founder)
- **Evidence anchors:**
  - `docs/company/POSITIONING.md`
  - `docs/company/MISSION_VISION.md`
  - `docs/company/OPERATING_PRINCIPLES.md`
  - `docs/company/ICP.md`
  - `docs/company/NORTH_STAR_METRICS.md`
  - `docs/company/DO_NOT_SELL_YET.md`
- **Next action:** Re-read POSITIONING.md monthly; lock if unchanged.

### Gate 1 — Offer Readiness

- **Status:** ✅ PASS
- **Score:** 100/100 (Pass ≥ 85)
- **Owner:** Sami + Delivery
- **Notes:**
  - Lead Intelligence Sprint (lead_intelligence_sprint) = 100/100
  - AI Quick Win Sprint (quick_win_ops) = 100/100
  - Company Brain Sprint (company_brain_sprint) = 100/100
- **Evidence anchors:**
  - `docs/services/lead_intelligence_sprint/offer.md`
  - `docs/services/ai_quick_win_sprint/offer.md`
  - `docs/services/company_brain_sprint/offer.md`
  - `docs/company/OFFER_LADDER.md`
- **Next action:** All three starter offers PASS — keep offer.md scope + pricing locked.

### Gate 2 — Delivery Readiness

- **Status:** ✅ PASS
- **Score:** 100/100 (Pass ≥ 85)
- **Owner:** Delivery
- **Evidence anchors:**
  - `docs/delivery/DELIVERY_STANDARD.md`
  - `docs/delivery/DELIVERY_LIFECYCLE.md`
  - `docs/delivery/CLIENT_ONBOARDING.md`
  - `docs/delivery/SCOPE_CONTROL.md`
  - `docs/delivery/HANDOFF_PROCESS.md`
  - `docs/delivery/RENEWAL_PROCESS.md`
- **Next action:** Dry-run handoff on a fake client every 2 weeks.

### Gate 3 — Product Readiness (MVP)

- **Status:** 🔴 BLOCKED
- **Score:** 100/100 (Pass ≥ 80)
- **Owner:** Engineering
- **Blocked on:** external dependency (see notes).
- **Notes:**
  - Checkout BLOCKED on Moyasar account activation (external).
- **Evidence anchors:**
  - `DEALIX_COMPANY_OPERATIONAL_STATE.md`
  - `api/`
  - `auto_client_acquisition/data_os`
  - `auto_client_acquisition/revenue_os`
  - `auto_client_acquisition/knowledge_os`
  - `auto_client_acquisition/governance_os`
  - `auto_client_acquisition/reporting_os`
  - `auto_client_acquisition/delivery_os`
- **Next action:** Unblock Moyasar (Sami sends activated sk_live_/sk_test_ key).

### Gate 4 — Governance Readiness

- **Status:** ✅ PASS
- **Score:** 100/100 (Pass ≥ 90)
- **Owner:** Governance
- **Evidence anchors:**
  - `dealix/registers/no_overclaim.yaml`
  - `dealix/registers/compliance_saudi.yaml`
  - `docs/company/DECISION_RULES.md`
  - `docs/trust/HUMAN_OVERSIGHT_MODEL.md`
- **Next action:** Review claims register monthly; PII spot-check weekly.

### Gate 5 — Demo Readiness

- **Status:** ✅ PASS
- **Score:** 100/100 (Pass ≥ 85)
- **Owner:** Sami + Sales
- **Evidence anchors:**
  - `demos/lead_intelligence_demo/`
  - `demos/ai_quick_win_demo/`
  - `demos/company_brain_demo/`
  - `docs/sales/DEMO_SCRIPT.md`
- **Next action:** Record 5-minute walkthrough per demo pack.

### Gate 6 — Sales Readiness

- **Status:** 🟡 FIX
- **Score:** 100/100 (Pass ≥ 85)
- **Owner:** Sami (Sales)
- **Notes:**
  - First outbound DM not yet logged in pipeline_tracker.csv.
- **Evidence anchors:**
  - `docs/sales/SALES_PLAYBOOK.md`
  - `docs/sales/DISCOVERY_SCRIPT.md`
  - `docs/sales/OFFER_PAGES.md`
  - `docs/sales/OBJECTION_HANDLING.md`
  - `docs/sales/PROPOSAL_TEMPLATE.md`
  - `docs/sales/FOLLOW_UP_SEQUENCES.md`
  - `docs/ops/pipeline_tracker.csv`
  - `docs/ops/launch_content_queue.md`
- **Next action:** Sami sends DM #1 from launch_content_queue.md and logs sent_at.

### Gate 7 — Client Delivery Readiness

- **Status:** ✅ PASS
- **Score:** 100/100 (Pass ≥ 85)
- **Owner:** Delivery
- **Evidence anchors:**
  - `docs/delivery/client_onboarding/welcome_message.md`
  - `docs/delivery/client_onboarding/data_request.md`
  - `docs/delivery/client_onboarding/project_timeline.md`
  - `docs/delivery/client_onboarding/roles_and_responsibilities.md`
  - `docs/delivery/client_onboarding/review_call_agenda.md`
  - `docs/delivery/client_onboarding/approval_process.md`
  - `clients/_TEMPLATE/`
- **Next action:** First paid client triggers full onboarding walk-through.

### Gate 8 — Retainer Readiness

- **Status:** ✅ PASS
- **Score:** 100/100 (Pass ≥ 85)
- **Owner:** Sami + Delivery
- **Notes:**
  - Pending: first sprint completion + proof pack before activation.
- **Evidence anchors:**
  - `docs/delivery/RETAINER_READINESS.md`
- **Next action:** Activate when first sprint closes successfully.

### Gate 9 — Scale Readiness

- **Status:** ✅ PASS
- **Score:** 100/100 (Pass ≥ 85)
- **Owner:** Sami (Ops)
- **Notes:**
  - Hire / partner trigger only after 3 paid clients delivered.
- **Evidence anchors:**
  - `docs/ops/DAILY_OPERATING_LOOP.md`
  - `docs/company/WEEKLY_OPERATING_REVIEW.md`
- **Next action:** Defer until first 3 paid clients delivered with NPS ≥ 8.

### Gate 10 — World-Class Readiness

- **Status:** 🟡 FIX
- **Score:** 0/100 (Pass ≥ 85)
- **Owner:** Sami (Strategy)
- **Notes:**
  - Aspirational. Activate only after 10+ paid projects, 3+ retainers, case studies live.
- **Evidence anchors:**
  - `docs/company/WORLD_CLASS_READINESS_AR.md`
- **Next action:** Do not measure until MRR is stable.

## Verification commands

```bash
# Lightweight (no app deps):
python scripts/render_stage_status.py --check

# Full (needs app environment):
python scripts/verify_dealix_ready.py --skip-tests
```

## References

- Doctrine: [`docs/company/DEALIX_STAGE_GATES_AR.md`](docs/company/DEALIX_STAGE_GATES_AR.md)
- Live state: [`DEALIX_COMPANY_OPERATIONAL_STATE.md`](DEALIX_COMPANY_OPERATIONAL_STATE.md)
- Readiness center: [`DEALIX_READINESS.md`](DEALIX_READINESS.md)
- Render script: [`scripts/render_stage_status.py`](scripts/render_stage_status.py)

