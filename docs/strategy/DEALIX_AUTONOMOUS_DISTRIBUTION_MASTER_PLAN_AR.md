# Dealix — خطة التصريف الذاتي الكامل للمنتجات
# Dealix — End-to-End Autonomous Product Distribution Master Plan

> **الإصدار / Version:** v1.0
> **التاريخ / Date:** 2026-05-24
> **الفرع / Branch:** `claude/vibrant-lovelace-KwZio`
> **المالك / Owner:** dealix-pm
> **النطاق / Scope:** بناء محرك ذاتي يربط 9 لايرات + 4 حلقات + رحلة العميل الكاملة.

---

## 0. الإطار الاستراتيجي / Strategic Frame

Dealix تبيع **عمليات ذكاء اصطناعي محوكَمة للسوق السعودي B2B** — قدرة تشغيلية + إثبات قابل للتدقيق. ليست أدوات AI، ليست spam.

سلّم تجاري بخمس درجات (مسعّر، موصول بالمنتج، جاهز للتفعيل):

| الدرجة | العرض | السعر (ريال) |
|---|---|---|
| 0 | Free AI Ops Diagnostic | 0 |
| 1 | 7-Day Revenue Intelligence Sprint | 499 |
| 2 | Data-to-Revenue Pack | 1,500 |
| 3 | Managed Revenue Ops (شهري) | 2,999–4,999 |
| 4 | Custom AI Service Setup | 5,000–25,000 + 1,000/شهر |
| Enterprise | AI Governance Review | 25,000–50,000 |

الهدف 90 يوم: **8-15K SAR MRR + 30-40K SAR one-time = ~40-55K SAR cumulative**.

---

## 1. اللايرات التسع / The 9 Layers

كل لايير له: (أ) موديول كانوني تحت `auto_client_acquisition/`، (ب) routers ضمن `api/routers/`، (ج) سكربتات تشغيل ضمن `scripts/`، (د) سجلات/registries لتدقيق الأثر.

### 1.1 DATA OS — جمع وتنظيف بيانات الـ leads

| الحقل | القيمة |
|---|---|
| Canonical module | `auto_client_acquisition/data_os/` |
| Public API | `compute_dq`, `validate_account_row`, `source_passport_valid_for_ai`, `import_preview_csv`, `normalize_account_row_fields`, `pii_flags_for_row` |
| Routers | `api/routers/data_os.py`, `api/routers/data.py`, `api/routers/diagnostic.py` |
| Registries | Source Passport ledger, DQ score per lead |
| Status | **OPERATIONAL** — يُستخدم في كل lead intake وفي sprint delivery |
| KPIs | Source coverage ratio ≥ 0.9، DQ score ≥ 70، PII flags = 0 |
| Inputs المسموحة (PDPL) | founder warm list, partner referrals, inbound forms, Calendly bookings, demo signups, customer-provided data (consent-bearing) |
| Inputs الممنوعة | scraping, cold-purchased lists, LinkedIn auto-pulls |

### 1.2 GOVERNANCE OS — البوابة الحوكميَّة قبل أي إجراء

| الحقل | القيمة |
|---|---|
| Canonical module | `auto_client_acquisition/governance_os/` |
| Public API | `policy_check_draft`, `policy_check_intake_source`, `audit_claim_safety`, `audit_draft_text`, `approval_for_external_channel`, `governance_decision_from_policy_check` |
| Routers | `api/routers/governance.py`, `api/routers/approval_center.py`, `api/routers/policy_check.py` |
| Registries | Decision Passport, Approval Center events, governance review log |
| Status | **OPERATIONAL** — كل output يحمل `governance_decision` |
| KPIs | Live-action gates = BLOCKED بشكل صريح حتى approval صريح، 0 doctrine violations |
| Doctrine controls | draft-only، PDPL-only، L0-L5 evidence levels، 11 non-negotiables |

### 1.3 PROOF OS — تجميع Proof Packs بعد كل sprint

| الحقل | القيمة |
|---|---|
| Canonical module | `auto_client_acquisition/proof_os/` |
| Public API | `build_empty_proof_pack_v2`, `merge_proof_pack_v2`, `proof_pack_v2_sections_complete`, `proof_pack_completeness_score`, `proof_pack_score_with_governance_penalty` |
| Routers | `api/routers/proof_pack_v2.py`, `api/routers/audit_export.py`, `api/routers/case_study_engine.py` |
| Registries | Proof Pack registry، evidence sources، before/after metrics |
| Status | **OPERATIONAL** — يلزم لكل engagement مدفوع |
| KPIs | Proof Pack score ≥ 70، evidence_level claimed ≤ evidence_level provided |

### 1.4 VALUE OS — تسجيل القيمة بثلاثة tiers

| الحقل | القيمة |
|---|---|
| Canonical module | `auto_client_acquisition/value_os/` |
| Public API | `add_event`, `list_events`, `summarize`, `value_ledger_event_valid` |
| Routers | `api/routers/value_ledger.py`, `api/routers/value_capture.py` |
| Registries | Value Ledger (estimated / verified / client_confirmed) |
| Status | **OPERATIONAL** — مع آلية تأكيد المصدر |
| KPIs | Estimated ≠ Verified (لا تخلطها)، client_confirmed يلزم رابطين مصدر |
| Doctrine | كل markdown يخرج للعميل ينتهي بـ "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" |

### 1.5 CAPITAL OS — تسجيل الأصول الرأسمالية لكل engagement

| الحقل | القيمة |
|---|---|
| Canonical module | `auto_client_acquisition/capital_os/` |
| Public API | `add_asset`, `list_assets`, `CapitalAssetType` |
| Routers | `api/routers/capital_ledger.py`, `api/routers/payments_*.py` |
| Registries | Capital ledger، invoice register، Moyasar transaction log |
| Status | **OPERATIONAL** — Moyasar في test mode (founder flip required) |
| KPIs | كل engagement مدفوع ≥ 1 capital asset، capital reconciliation أسبوعي |

### 1.6 ADOPTION OS — onboarding وتتبع الاستخدام

| الحقل | القيمة |
|---|---|
| Canonical module | `auto_client_acquisition/adoption_os/` |
| Public API | `adoption_score`, `adoption_band`, `wave2_retainer_eligibility`, `adoption_retainer_readiness_passes`, `FrictionEvent` |
| Routers | `api/routers/customer_success.py`, `api/routers/customer_usage.py`, `api/routers/adoption*.py` |
| Registries | Adoption dashboard، onboarding phases، training products، NPS log |
| Status | **OPERATIONAL** |
| KPIs | Adoption band ≥ "B" قبل عرض retainer، NPS log أسبوعي |

### 1.7 CLIENT OS — العزل multi-tenant ومنصة العميل

| الحقل | القيمة |
|---|---|
| Canonical module | `auto_client_acquisition/client_os/` |
| Public API | `client_health_score`, `agent_transparency_card_valid`, `client_expansion_recommendation`, `build_empty_monthly_value_report`, `build_empty_monthly_governance_report` |
| Routers | `api/routers/customer_company_portal.py`, `api/routers/admin_tenants.py`, `api/routers/customer_brain.py` |
| Registries | Tenant theme، client health score، capability dashboard، agent transparency cards |
| Status | **OPERATIONAL** |
| KPIs | Tenant isolation 100%, monthly value + governance reports تُولَّد آلياً |

### 1.8 SALES OS — توليد العروض وقَنوات الإقناع

| الحقل | القيمة |
|---|---|
| Canonical module | `auto_client_acquisition/sales_os/` |
| Public API | `icp_score`, `client_risk_score`, `qualify_opportunity`, `build_proposal_skeleton`, `render_scope_bullets` |
| Routers | `api/routers/sales.py`, `api/routers/proposals.py`, `api/routers/commercial_engagements.py` |
| Registries | Pipeline، proposals، outreach drafts (DRAFT-ONLY) |
| Status | **OPERATIONAL** — كل send معلَّق بانتظار founder approval |
| KPIs | proposal turnaround ≤ 24h من إكمال qualification، 0 sends بدون approval |

### 1.9 REVENUE INTELLIGENCE OS — تقارير CEO وحلقات التعلّم

| الحقل | القيمة |
|---|---|
| Canonical modules | `auto_client_acquisition/revenue_os/`, `revenue_intelligence_founder_hooks.py`, `executive_pack_v2/`, `executive_reporting/` |
| Public API | تقارير أسبوعية، KPIs، CEO dashboard، unit economics، capability factory metrics |
| Routers | `api/routers/executive_pack.py`, `api/routers/revenue_*.py`, `api/routers/business.py` |
| Registries | Weekly executive pack، CEO scorecard، unit economics ledger |
| Status | **OPERATIONAL** |
| KPIs | CEO weekly pack يُولَّد كل أحد، unit economics مُحدَّثة كل أسبوع |

---

## 2. الحلقات الذاتية الأربع / The 4 Autonomous Loops

كل حلقة لها سكربت واحد قابل للاستدعاء، وكلها مُغلَّفة في `auto_client_acquisition/autonomous_distribution/loops.py` لتشغيل موحد. لا حلقة ترسل send خارجي بدون approval gate.

### 2.1 Daily Morning Loop — 6:00 AM AST

**الأهداف:**
- pipeline refresh (سحب inbound forms, Calendly, demo signups)
- lead scoring (ICP × risk × DQ)
- draft outreach queue (DRAFT-ONLY)
- war-room snapshot
- founder digest (markdown bilingual)

**Implementation:** `scripts/run_dealix_daily_ops.py` + `dealix/autonomous_distribution/loops.py::morning_loop()`

**Outputs:**
- `data/founder_briefs/YYYY-MM-DD-morning.md`
- `data/war_room_today.json`
- `data/draft_outreach_queue/YYYY-MM-DD.jsonl`

**Approval gates:** أي draft outreach يدخل approval_center، لا يخرج تلقائياً.

### 2.2 Daily Evening Loop — 8:00 PM AST

**الأهداف:**
- KPI refresh (revenue, leads, pipeline conversion)
- friction log review
- tomorrow's priority queue (top-4 actions)
- evidence sync (proof_os + capital_os)

**Implementation:** `scripts/dealix_pm_daily.py` + `dealix/autonomous_distribution/loops.py::evening_loop()`

**Outputs:**
- `data/daily_brief/YYYY-MM-DD.md` (top-4 priority actions)
- `data/founder_briefs/YYYY-MM-DD-evening.md`

### 2.3 Weekly Loop — Sunday 6:00 PM AST

**الأهداف:**
- retainer eligibility check (`adoption_os.wave2_retainer_eligibility`)
- capital reconciliation (Moyasar txns ↔ capital_ledger)
- weekly executive pack (`executive_pack_v2`)
- capability factory cycle (`scripts/generate_weekly_operating_proof_pack.py`)

**Implementation:** `scripts/founder_weekly_loop.sh` + `dealix/autonomous_distribution/loops.py::weekly_loop()`

**Outputs:**
- `data/exec_pack/YYYY-WW.md`
- `data/capital_reconciliation/YYYY-WW.json`
- `data/proof_pack_weekly/YYYY-WW.md`

### 2.4 Monthly Loop — Day 1 of month

**الأهداف:**
- 30/60/90 milestone reviews
- gate re-assessment (live_charge / whatsapp_live_send / email_live_send / linkedin_and_scraping)
- world-class readiness audit (`scripts/dealix_full_ops_productization_verify.sh`)

**Implementation:** `dealix/autonomous_distribution/loops.py::monthly_loop()`

**Outputs:**
- `data/monthly_review/YYYY-MM.md`
- `data/gate_audit/YYYY-MM.json`

---

## 3. رحلة العميل الكاملة / Customer Journey End-to-End

```
[Lead intake] ──► [DQ + Source Passport] ──► [ICP × Risk score] ──► [Governance gate]
      ▼                    ▼                          ▼                    ▼
   data_os            data_os.dq                sales_os.icp_score    governance_os.policy_check
      ▼
[BANT qualify] ──► [Decision Passport] ──► [Proposal render] ──► [Founder approval]
      ▼                    ▼                          ▼                    ▼
   sales_os.qualify   decision_passport      sales_os.proposal     approval_center
      ▼
[Send (queued draft)] ──► [Demo] ──► [Sprint kickoff] ──► [Delivery factory]
      ▼                       ▼              ▼                    ▼
   safe_send_gateway       calendly      sprint_runner         delivery_factory
      ▼
[Proof Pack] ──► [Invoice (Moyasar)] ──► [Payment confirm] ──► [Onboarding]
      ▼                  ▼                          ▼                    ▼
   proof_os         payments router            webhook hook          adoption_os
      ▼
[Retainer eligibility] ──► [Renewal / upsell]
      ▼                              ▼
adoption_os.wave2          client_os.expansion_engine
```

كل خطوة:
- تكتب event في الـ ledger المخصص (source_passport / decision_passport / proof_pack / capital_ledger / value_ledger / friction_log)
- تحترم 11 non-negotiables (تُتحقَّق برمجياً في `tests/test_no_*`)
- تنتج output قابل للقياس (يدخل KPI dashboard)

---

## 4. Integration Map

| Integration | Status | Use | Approval gate |
|---|---|---|---|
| Moyasar | TEST mode | invoices + paid charges | founder flip لـ live cutover |
| Gmail (OAuth) | configured / fallback | email drafts + transactional confirmations | external sends تمرّ عبر safe_send_gateway |
| Calendly | inbound | demo + sprint kickoff bookings | ingest فقط |
| PostHog | configured | product analytics | event taxonomy ثابت |
| Sentry | configured | error tracking | لا PII في الأخطاء |
| HubSpot | optional adapter | CRM sync (draft) | لا cold sends |
| LinkedIn | drafts only | content drafts | لا automation، لا scraping |
| WhatsApp Business | configured | WhatsApp drafts | لا cold sends، approval_center فقط |

---

## 5. Approval Gates — متى يتدخل المؤسس

| Gate | Why | Default state |
|---|---|---|
| Outreach send (Email / WhatsApp / LinkedIn) | PDPL + brand discipline | BLOCKED بدون founder approve |
| Live Moyasar charge | Real money | BLOCKED حتى founder flip mode |
| Proof Pack publication | Reputation | BLOCKED حتى founder approves draft |
| Capital asset registration | Audit chain | DRAFT حتى founder confirms |
| Retainer offer | Right-sizing | BLOCKED حتى adoption_band ≥ B |
| Doctrine override | Never | Permanently BLOCKED |

---

## 6. SLAs لكل خطوة

| Step | SLA |
|---|---|
| Lead → DQ score | ≤ 5 minutes |
| DQ → Decision Passport | ≤ 10 minutes |
| Decision Passport → Draft proposal | ≤ 4 hours |
| Founder approve → Send | ≤ 24 hours |
| Payment confirmed → Onboarding start | ≤ 24 hours |
| Sprint kickoff → Proof Pack | ≤ 7 days |
| Proof Pack → Capital asset | ≤ 48 hours after delivery |
| Capital asset → Retainer offer | ≤ 7 days |

---

## 7. KPIs لكل لايير

| Layer | Primary KPI | Target by Day 90 |
|---|---|---|
| DATA OS | DQ avg score | ≥ 75 |
| GOVERNANCE OS | Doctrine violations | 0 |
| PROOF OS | Proof Pack avg score | ≥ 70 |
| VALUE OS | Confirmed value (SAR) | ≥ 30,000 |
| CAPITAL OS | Capital assets registered | ≥ 5 |
| ADOPTION OS | Adoption band ≥ B clients | ≥ 3 |
| CLIENT OS | Tenant health avg | ≥ 70 |
| SALES OS | Qualified opportunities | ≥ 15 |
| REVENUE INTEL | Weekly exec pack consistency | 12/12 weeks |

---

## 8. 30 / 60 / 90 Day Milestones

### Day 0–30 (Activation)
- Moyasar live cutover (founder action)
- 5 free diagnostics delivered → 2 Sprint conversions
- First Proof Pack score ≥ 70
- Daily morning/evening loops running
- 1 paid invoice in Moyasar

### Day 31–60 (Expansion)
- 3 Sprints delivered → 1 Data Pack upgrade
- First Managed Revenue Ops retainer signed
- 2 Capital Assets registered
- Weekly executive pack reliably generated
- Founder time per sprint ≤ 5h

### Day 61–90 (Compounding)
- 8-15K SAR MRR live
- 30-40K SAR one-time cumulative
- 3 active retainers
- 5 Capital Assets registered
- 1 case-safe summary published

If revenue < 25K SAR by day 60 → halt new offer dev, double down on sales motion (warm-list, content cadence, price tests).

---

## 9. Rollback Plans

| Scenario | Rollback |
|---|---|
| Moyasar live charge fails | Revert env `MOYASAR_MODE=test`، notify founder، dispute via Moyasar dashboard |
| Outreach send misfired | Email recall (Gmail), founder apology template، add friction event |
| Proof Pack score drops < 70 | Pause publication، re-run evidence audit، block new sprint sells |
| Doctrine violation detected | Block branch merge، open friction event severity=high، notify founder within 1h |
| Adoption_band drops < B for any active retainer | Block expansion engine، intervene with founder call |

---

## 10. Decision Rules (auto-enforced)

- **If revenue ≥ 40K cumulative + 3 retainers active by day 90 →** propose Wave 3 (Enterprise Trust).
- **If revenue < 25K SAR by day 60 →** stop building, focus sales.
- **If founder time per sprint > 5h after customer 5 →** halt new sales، automate.
- **If any non-negotiable would be violated →** refuse and propose safe alternative.

---

## 11. Anti-patterns الممنوعة (Doctrine Reinforcement)

1. لا scraping من أي مصدر.
2. لا cold WhatsApp automation.
3. لا LinkedIn automation.
4. لا fake / un-sourced claims.
5. لا guaranteed sales outcomes.
6. لا PII in logs.
7. لا source-less knowledge answers.
8. لا external action without approval.
9. لا agent without identity.
10. لا project without Proof Pack.
11. لا project without Capital Asset.

كل واحد منهم محمي بـ guard test تحت `tests/test_no_*`.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
