# Dealix COMMENT_TODO_BACKLOG.md

**Date:** 2026-06-23

**Total TODO/FIXME/HACK/NOTE/REVIEW/DEPRECATED signals scanned:** 934

## BLOCKER (8)

- `auto_client_acquisition\ecosystem\webhook_dispatcher.py:167` — - 4xx client error (subscriber bug — they need to fix their endpoint)
- `reports\final\FINAL_REPO_INTEGRATION_AUDIT.md:162` — | لا يوجد **broken reference review** | — | **FIXED** — `reports/final/BROKEN_REFERENCE_REVIEW.md` |
- `reports\github-context\top-comments\pr-681-review-comments.json:1` — [{"url":"https://api.github.com/repos/Dealix-sa/dealix/pulls/comments/3369699260","pull_request_review_id":4445434557,"id":3369699260,"node_id":"PRRC_kwDOR1eIic7I2Ye8","diff_hunk":"@@ -381,3 +381,77 @@\n         from fastapi import HTTPException\n   ...
- `reports\github-context\pr-681\review_comments.json:7` — "diff_hunk": "@@ -381,3 +381,77 @@\n         from fastapi import HTTPException\n         raise HTTPException(status_code=404, detail=\"lead_inbox_empty\")\n     return {\"ok\": True, \"change\": rec}\n+\n+\n+@router.get(\"/approvals\")\n+async def ap...
- `docs\ai_governance\HUMAN_APPROVAL_BOUNDARIES_AR.md:98` — - **حالة طوارئ مُعتمدة** (Emergency Exception): المُؤسس يُعطي pre-approval لفئة إجراءات — كل تنفيذ يُسجَّل بعلامة `emergency=true`، يحتاج post-incident review.
- `docs\integrations\WHATSAPP_BUSINESS_CONNECTOR_PLAN.md:23` — - `tests/test_whatsapp_no_auto_send.py` — fails if any path sends without review
- `docs\reference\KNOWN_LIMITATIONS.md:3` — > سجل واحد لكل `NotImplementedError`, `TODO`, feature flag مغلق، أو ستب. يحدّث مع كل PR يضيف/يحل قيد.
- `docs\V7_MASTER_EVIDENCE_TABLE.md:117` — runtime gates are honest skips/xfails with TODO bug tickets.

## OUTBOUND_SEND (15)

- `business\_data\knowledge_index.json:9` — "preview": "# Dealix Human Review Statement\n\nEvery outbound action involving the customer's brand, prospects, or money requires explicit human approval before it leaves the workspace.\n\n## Approval matrix\n\n| Action | Reviewer | Tool |\n| --- | -...
- `business\_data\knowledge_index.json:243` — "preview": "# Prompt: Compliance Review (v1)\n\nRead a draft outbound message or proposal. Flag:\n- Banned claims (guarantees, fake metrics).\n- Missing scope clarifications.\n- Implied auto-send language.\n- Pricing inconsistencies vs. catalog.\n\nO...
- `business\enterprise\ENTERPRISE_BUYER_FAQ_EN.md:17` — Never. Every outbound message goes through human review (Dealix founder + your commercial owner). This is enforced in code (`tests/test_no_auto_send.py`).
- `business\proof\RETAINER_EXPANSION_PLAYBOOK.md:18` — "You've seen Revenue OS produce X. The natural next layer is Review OS — same operating rhythm, same proof cadence, focuses on protecting your reputation while we scale outbound. Want to scope it for next quarter?"
- `business\contracts\STATEMENT_OF_WORK_TEMPLATE_EN.md:35` — - Human review for every outbound message before sending.
- `auto_client_acquisition\diagnostic_engine\engine.py:47` — "Brief is for review only — no outbound message sent without founder approval.",
- `apps\web\app\api\crm\drafts\[id]\approve\route.ts:23` — "Approval recorded. The outbound message is NOT sent automatically. Use the customer's own WhatsApp/email channel after manual review.",
- `auto_client_acquisition\service_mapping_v7\mapper.py:30` — "next_step": "Founder review of the 10-opportunity shortlist before any outbound draft is approved.",
- `outreach-execution\HUMAN_REVIEWED_OUTREACH_POLICY_AR.md:3` — Dealix لا يستخدم outbound مؤتمت بالكامل في مرحلة preview. كل رسالة تخرج باسم الشركة يجب أن تمر عبر review.
- `reports\ceo\REVENUE_PR_COMPARISON.md:134` — - Keep outbound as draft/review-first unless controlled-live gates pass.
- `reports\github-context\pr-621\detail.json:9` — "body": "## Dealix Research & Targeting OS\n\nA repeatable, **governed** daily loop that turns seeds + allowlisted research into a scored, evidence-backed **target pool** — not an outbound blaster. **Quality over volume. No external send without foun...
- `reports\github-context\pr-621\detail.json:24` — "messageBody": "Adds a repeatable daily research/targeting engine that turns seeds plus\nallowlisted discovery into a scored, evidence-backed target pool — not an\noutbound blaster. Quality over volume; no external send without founder\napproval.\n\n...
- `docs\gtm\whatsapp\WHATSAPP_POST_REPLY_FLOW_AR.md:86` — - **`WHATSAPP_ALLOW_LIVE_SEND` = false** by default; no live send before opt-in completion, legal review, and an explicit per-environment enable.
- `docs\sectors\LOGISTICS_COMPANIES_AR.md:121` — "[Name], in short: we organize your heavy account base and surface the highest-priority for review — 9,500 SAR (or a 499 test sprint first), drafts for your approval, no external send. Reply whenever suits."
- `scripts\founder\run_founder_revenue_day.py:114` — External send remains disabled by default. Founder review is required before sending.

## SECURITY_SECRET (20)

- `tools\patch_intake_contract.py:73` — if any(token in text for token in ["review", "reviews", "تقييم", "تقييمات", "سمعة"]):
- `auto_client_acquisition\whatsapp_client_os\intent_router.py:109` — requires_human=guard.secret_scan.found,  # secrets attempt → human review
- `api\routers\auth.py:500` — # TODO(production): deliver invite_token via transactional email (e.g. SendGrid/SES)
- `tests\conftest.py:152` — 'tests/test_v7_secret_leakage_guard.py::test_no_secret_prefix_outside_allowlist': "SECURITY REVIEW: _PREFIX_ALLOWLIST drift — ~29 redaction/validator/runbook/env-template files reference sk_live_/ghp_/AIza prefixes; confirm none are real secrets, the...
- `reports\v10_v20\V10_V20_EXECUTION_PLAN.md:35` — - Production WhatsApp/email require official API + credentials + terms review and remain disabled by default.
- `reports\github-context\pr-607\detail.json:39` — "messageBody": "- secret/risk scanner: store a non-reversible SHA-256 fingerprint of any\n  match instead of a clear-text preview (a scanner must never echo secrets);\n  resolves clear-text storage/logging alerts.\n- drafts.py: make the multi-line fo...
- `reports\github-context\pr-636\detail.json:54` — "messageBody": "…dependabot\n\nTrivy's secret scanner flagged the sk_live_ detection regexes inside the\nv7/v10 launch-verify scripts as Stripe keys; skip those two files.\n\nThe real Next.js CVEs (next@15.1.3, incl. CVE-2025-29927 / CVE-2025-55182)\...
- `docs\CI_QUARANTINE.md:99` — ### SECURITY REVIEW: _PREFIX_ALLOWLIST drift — ~29 redaction/validator/runbook/env-template files reference sk_live_/ghp_/AIza prefixes; confirm none are real secrets, then allowlist
- `docs\agents\TOKEN_BUDGET_POLICY.md:43` — `token-optimizer/10-tools-monitoring/` covers usage monitoring. When you review
- `docs\agents\PR_TRIAGE_POLICY.md:16` — | `security` | title/label mentions security/auth/secret | review first, with care |
- `docs\productized_services\ACCEPTANCE_CRITERIA_LIBRARY_AR.md:24` — | U1 | No secrets in deliverable | grep + manual review | founder |
- `docs\security\EXTERNAL_ACTION_APPROVAL_POLICY.md:32` — | Critical | Payment, legal, contract, secrets | Founder + legal review |
- `docs\security\UNTRUSTED_INPUT_POLICY.md:272` — | Bearer token | `Bearer xxx` | `[REDACTED_TOKEN]` |
- `docs\security\SECRETS_HANDLING_POLICY.md:31` — | OAuth Tokens | `Bearer xxx`, `access_token=xxx` | CRITICAL |
- `docs\security\SECRETS_HANDLING_POLICY.md:316` — *Review required: Quarterly or after any secret exposure incident*
- `docs\SAMI_ACTION_ITEMS.md:42` — **المطلوب:** token بصيغة `pat-XXX...` من Private App.
- `tests\test_v7_no_guaranteed_claims.py:84` — "TODO: V5/V6/V7 markdown docs reference these tokens in policy/"
- `scripts\github_setup.sh:82` — echo -e "${RED}❌ Possible secrets detected. Review before pushing.${NC}"
- `scripts\integration_upgrade_verify.sh:94` — # Match real-looking secrets but exclude obvious placeholders (xxx, ..., ***)
- `scripts\wave8_customer_data_boundary_check.sh:72` — check "No hardcoded secrets in tracked .py files" "REVIEW: $SECRET_HITS"

## COMPLIANCE (72)

- `business\_data\knowledge_index.json:33` — "preview": "# Dealix AI Governance Statement\n\n## Default mode is deterministic\n\nDealix's operator scripts and review tooling do not require an LLM to run. The default produces deterministic, reproducible output. LLM-assist is opt-in and per task....
- `business\_data\knowledge_index.json:243` — "preview": "# Prompt: Compliance Review (v1)\n\nRead a draft outbound message or proposal. Flag:\n- Banned claims (guarantees, fake metrics).\n- Missing scope clarifications.\n- Implied auto-send language.\n- Pricing inconsistencies vs. catalog.\n\nO...
- `business\enterprise\AI_GOVERNANCE_STATEMENT.md:5` — Dealix's operator scripts and review tooling do not require an LLM to run. The default produces deterministic, reproducible output. LLM-assist is opt-in and per task.
- `auto_client_acquisition\business\gtm_plan.py:49` — "notes": ["Cold email only with suppression lists + compliance review."],
- `dealix\config\support_intents.yaml:53` — note: "PDPL / DSR — human review"
- `ops\founder-ceo-os\03-ai-governance-and-model-risk.md:28` — | Compliance drift | Workflow violates customer policy | Policy review and approvals |
- `auto_client_acquisition\v3\compliance_os.py:69` — "lawful_basis_note": "Record and review per PDPL operating policy before production outreach.",
- `data\outreach\sector_pitches.json:58` — "fix_en": "Dealix builds human-approved reply handling, appointment reminders, and review follow-up — with a clear monthly report. PDPL-aligned.",
- `auto_client_acquisition\leadops_reliability\debug.py:101` — "reason_en": "All leads blocked by compliance rules — review the block list.",
- `frontend\src\content\learn\articles.ts:227` — { heading: "Responsible Building Steps", body: "1) Document every AI use case in your company. 2) Define who reviews AI decisions. 3) Add Audit Trail for every AI decision. 4) Don't send externally without human review. 5) Review PDPL compliance for ...
- `frontend\src\components\gtm\CustomAiRequestForm.tsx:379` — : "I consent to manual review and PDPL-compliant follow-up contact. No automated cold outreach."}
- `README.md:195` — Compliance documentation does not replace legal review. Production launch requires evidence from tests, controls, logs, and operational procedures.
- `sales\playbook\OBJECTION_BANK.md:24` — > **EN:** "No — the opposite. Dealix does not offer scraping. We work **only** on your own data, with your consent, under PDPL. We do not harvest data from the web or buy lists. The safe alternative: we organize the opportunities you already hold and...
- `sales\playbook\OBJECTION_BANK.md:64` — > **EN:** "A useful general tool, but your problem is not 'writing text' — it is governed work on your data: ranking opportunities, respecting PDPL, an auditable decisions log, and drafts you review before any use. That is discipline and governance, ...
- `reports\commercial\PRODUCT_CATALOG_REVIEW.md:138` — | Offer | PDPL Review | Reason |
- `reports\commercial\ICP_PRIORITY_REPORT.md:133` — **Risk 3 segments need compliance review** قبل proposal.
- `reports\commercial\COMMERCIAL_OPERATING_MAP.md:139` — Offer Catalog    Margin Floor       PDPL Review
- `reports\github-context\pr-649\detail.json:9` — "body": "## Summary — ملخّص\n\nA comprehensive launch-readiness pass that closes the remaining productization, compliance, and verification gaps on a v3.0.0 codebase that was already ~95% complete. **No production deployment is performed** — everythi...
- `reports\github-context\pr-607\detail.json:24` — "messageBody": "…e pack\n\nAdds a review-only Commercial Launch OS + Final Launch Control Tower:\n\n- launch_os/ core library: synthetic leads, 400+ draft factory, safety\n  audit, readiness scoring, 30-day media/social calendar, compliance rules.\n-...
- `reports\github-context\pr-606\detail.json:24` — "messageBody": "…, safety/quality/compliance gates, media-social OS\n\n- First 5 vertical playbooks (FM, contracting, real estate, legal, consulting)\n- Deterministic stdlib-only draft factory: 400+ drafts, all approval-gated\n- Safety audit proving ...
- `reports\github-context\pr-605\detail.json:9` — "body": "## Summary\n\nAdds the official **Dealix Commercial Launch OS** with first 5 verticals, SAR offer ladder, 400+ daily founder-review draft factory, quality/compliance gates, no-send safety audit, commercial metrics, delivery playbooks, GitHub...
- `reports\security\SECURITY_RED_TEAM_FINAL_REPORT.md:450` — 1. **Review all security docs** in `docs/security/`, `docs/outreach/`, `docs/whatsapp/`, `docs/privacy/`
- `reports\github-context\pr-604\detail.json:24` — "messageBody": "…afts\n\nAdds the Dealix Commercial Launch OS: a pure-stdlib Daily Draft Factory that\ngenerates >=400 review-only drafts/day across the first 5 verticals, with\ndeterministic quality, compliance, and safety gates, a founder review qu...
- `reports\procurement\PROCUREMENT_FINAL_REPORT.md:144` — - **Agent #13 (Legal):** vendor PDPL = legal review trigger.
- `reports\legal\LEGAL_GUARD_FINAL_REPORT.md:99` — - **Agent #17 (Procurement):** vendor PDPL compliance = legal review trigger.
- `reports\kimi_final_launch_execution\FOUNDER_ONLY_ACTIONS.md:8` — | F1 | **Legal review of DPA** (`docs/DPA_DEALIX_FULL.md`) | Requires qualified Saudi legal counsel to validate PDPL compliance | Before first paid customer | Lawyer sign-off |
- `reports\github-context\pr-623\review_comments.json:76` — "diff_hunk": "@@ -0,0 +1,176 @@\n+#!/usr/bin/env python3\n+\"\"\"Compliance gate — the first hard filter in the targeting pipeline.\n+\n+Every candidate company must pass this gate BEFORE it is scored, routed, or\n+drafted. The gate encodes the Deali...
- `docs\analytics\STOP_SCALE_FIX_RULES_AR.md:29` — | unsubscribe_rate | > 2% | Review list quality | NO |
- `docs\analytics\DEALIX_ANALYTICS_OS_AR.md:365` — ├── PRIVACY_AWARE_ANALYTICS_REVIEW.md   # Privacy review
- `docs\CROSS_BORDER_TRANSFER_ADDENDUM.md:216` — **Saudi PDPL Article 29 alignment:** transfers rely on appropriate safeguards (#2) + contract performance (#4) per the spirit of the law. Lawyer review will validate exact article applicability.
- `docs\DESIGNOPS_ARTIFACT_SAFETY.md:92` — 9. **Review PDPL exposure** with counsel if the leak involved PII.
- `tests\test_no_linkedin_scraper_string_anywhere.py:151` — 2. SDAIA inquiry / lawyer review relies on accurate disclosure
- `docs\DEALIX_MASTER_EXECUTION_EVIDENCE_TABLE.md:282` — - **Next action:** Engage PDPL-experienced Saudi lawyer for review before first signed contract.
- `docs\BUSINESS_REALITY_AUDIT.md:71` — | Privacy Policy (PDPL-aligned) | **READY_TO_SELL** | Low | Exists; lawyer review recommended |
- `docs\finance\OFFER_MARGIN_MODEL_AR.md:116` — | Clinic | 45% | PDPL review adds cost |
- `docs\DPA_DEALIX_FULL.md:10` — > **Founder note:** This DPA aligns with Saudi Personal Data Protection Law (PDPL) principles and GDPR-derived patterns. Founder is taking responsibility for using this template per `LEGAL_FOUNDER_SELF_EXECUTION.md`. Lawyer review parallel-tracked wi...
- `docs\gtm\whatsapp\WHATSAPP_POST_REPLY_FLOW_AR.md:86` — - **`WHATSAPP_ALLOW_LIVE_SEND` = false** by default; no live send before opt-in completion, legal review, and an explicit per-environment enable.
- `docs\evals\COMMERCIAL_SAFETY_EVALS_AR.md:146` — - **Agent response:** "Health data requires PDPL review. Not allowed without."
- `docs\governance\PDPL_DATA_RULES.md:14` — Processing of personal data requires a valid basis under PDPL and implementing regulations — commonly **consent**, **contract performance**, **legitimate interest** (where applicable and balanced), or **publicly available data from a lawful public so...
- `docs\commercial\COMMERCIAL_STRATEGY_AR.md:76` — - **Custom domains without PDPL review** — compliance risk
- `docs\commercial\COMMERCIAL_RISK_REGISTER_AR.md:63` — - **Mitigation:** PDPL review, DPA, compliance
- `docs\commercial\DEALIX_AI_OPERATING_COMPANY_AR.md:138` — **خدمات:** AI Readiness & Risk Review، AI Usage Policy، PDPL-Aware Data Review.
- `docs\company\DECISION_OPERATING_SYSTEM.md:28` — | **Risk review** | What can go wrong; PDPL / claims / scope |
- `docs\company\DEALIX_MASTER_OPERATING_SYSTEM.md:386` — #### PDPL-Aware Data Review
- `docs\company\DEALIX_HOLDING_OS.md:168` — **خدمات:** AI Readiness Review · AI Usage Policy · PDPL-Aware Data Review · AI Governance Program.
- `docs\WAVE8_DPA_AND_CONSENT_READINESS.md:15` — | WhatsApp Consent Checklist | `docs/wave8/WHATSAPP_CONSENT_CHECKLIST_AR_EN.md` | WhatsApp opt-in compliance | draft_only — needs lawyer review |
- `docs\legal\DPO_APPOINTMENT_TEMPLATE.md:23` — 6. Review breach notifications before 72-hour SDAIA submission (Art. 21)
- `docs\playbooks\clinics_playbook.md:42` — Higher **data sensitivity** than generic B2B — run Governance + PDPL-aware review early.
- `docs\company\SERVICE_FIVE_DOORS_AR.md:61` — **الخدمات:** AI Readiness Review، AI Usage Policy، PDPL-aware Data Review، AI Governance Program.
- `docs\company\SERVICE_CATALOG_V1.md:46` — PDPL-Aware Data Review

## REFACTOR (20)

- `reports\github-context\pr-758\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-756\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-755\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-752\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-654\detail.json:9` — "body": "## What & why\n\nAdds a single, evidence-backed decision file:\n**`docs/ops/OFFICIAL_PRIVATE_LAUNCH_DECISION.md`**.\n\nThe repo's real bottleneck isn't \"build more\" — it's **decide + consolidate**.\nThere are **50 open draft PRs**, none me...
- `reports\github-context\pr-717\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-716\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-715\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-714\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-696\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-741\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-740\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-738\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-737\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-736\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-734\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-733\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-731\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-732\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...
- `reports\github-context\pr-719\detail.json:9` — "body": "# Pull Request\r\n\r\n## Summary | الملخص\r\n<!-- What does this PR change and why? -->\r\n\r\n## Type of change | نوع التغيير\r\n- [ ] 🐛 Bug fix\r\n- [ ] ✨ New feature\r\n- [ ] 💥 Breaking change\r\n- [ ] 📝 Docs only\r\n- [ ] ♻️ Refactor\r\n...

## MIGRATION_DB (5)

- `reports\github-context\pr-611\detail.json:24` — "messageBody": "Add a complete, verifiable Startup Operating System layer (additive, no\nbackend/web/migration changes):\n\n- 21 OS doc areas (company, product, site-launch, commercial-launch, sales,\n  marketing, media-social, ads, revops, delivery,...
- `reports\github-context\pr-679\detail.json:99` — "messageBody": "Frontend improvements:\n• icon.tsx: correct brand colors — Navy #001F3F bg + Gold #D4AF37 D\n  (was #0A4D3F / #C9A961, off-brand green palette)\n• layout.tsx: add Organization JSON-LD structured data; improve metadata\n  (metadataBase...
- `reports\github-context\pr-718\detail.json:9` — "body": "## Summary\n\n- **Bundle integration**: merged all 186 files from `dealix_market_launch_complete_bundle` (docs, schemas, evals, reports, patches) into the correct repo locations — additive only, zero overwrites\n- **4x expansion**: on top of...
- `docs\data_governance\SCHEMA_REGISTRY_AR.md:88` — - **New schema:** add to registry, review by data lead
- `docs\V5_OS_SCOPE.md:286` — schema requires founder review of data lifecycle policy and PDPL

## DOCS_NEEDED (22)

- `auto_client_acquisition\support_os\responder.py:86` — "documented policy (draft for review before sending). The "
- `frontend\src\content\learn\articles.ts:227` — { heading: "Responsible Building Steps", body: "1) Document every AI use case in your company. 2) Define who reviews AI decisions. 3) Add Audit Trail for every AI decision. 4) Don't send externally without human review. 5) Review PDPL compliance for ...
- `README.md:195` — Compliance documentation does not replace legal review. Production launch requires evidence from tests, controls, logs, and operational procedures.
- `sales\playbook\WARM_LIST_CALL_SCRIPTS.md:120` — > **EN:** "An agency lives on the proof it shows clients. What we provide is governed, documented work you can present as evidence — not polished vanity numbers. You review every output before any use."
- `sales\playbook\OBJECTION_BANK.md:100` — > **EN:** "I believe you, and many tools fail because they are ungoverned: launched without consent, without a decisions log, without measurable proof. The difference here is that every step is consented, documented, and ends with a Proof Pack you re...
- `reports\github-context\pr-606\detail.json:9` — "body": "## Summary\n\nAdds a self-contained Dealix **Commercial Launch OS**: a deterministic, stdlib-only, founder-review draft factory plus the supporting commercial, delivery, and media/social documentation. It satisfies the golden rule end-to-end...
- `reports\github-context\pr-640\detail.json:9` — "body": "## Why\n\nThe repo was missing the last two files needed for the documented Claude Code + Codex integration \"final shape\". Direct inspection showed the rest of the checklist was already satisfied on the branch base — `AGENTS.md`, `pyprojec...
- `reports\github-context\pr-614\review_comments.json:490` — "diff_hunk": "@@ -0,0 +1,1412 @@\n+#!/usr/bin/env python3\n+\"\"\"Generate the Dealix V9 Strategic Moat & Enterprise Readiness OS documentation.\n+\n+Data-driven: every operating file is defined as (title, purpose, sections) and\n+rendered as bilingu...
- `docs\03_commercial_mvp\SPRINT_DELIVERY_PLAYBOOK.md:35` — **Founder checkpoint:** review the DQ score. A baseline DQ < 40 means the client has a data-readiness problem, not a sprint problem; pause the sprint and propose the 1,500 SAR Data Pack instead. DQ between 40 and 70 → proceed with documented caveats....
- `reports\github-context\pr-625\detail.json:24` — "messageBody": "Frame Dealix as a Saudi AI Business Operating System company (14 OS),\nwith the Command Sprint as the first commercial wedge. Adds the full\nlaunch documentation spine plus delivery scaffolding:\n\n- docs/00_platform_truth: source of ...
- `scripts\dealix_campaign_builder.py:4` — obj={'name':a.campaign_name,'vertical':a.vertical,'created_at':datetime.datetime.utcnow().isoformat()+'Z','status':'draft','rules':['manual review required','no automated bulk send','document source_url']}
- `reports\github-context\pr-750\detail.json:9` — "body": "## Summary\n\nDelivered complete founder execution system for Dealix — a comprehensive, autonomous operating system to enable founder-led customer acquisition and revenue generation.\n\n**Phase 1:** Documentation (3,500+ lines) + Core automa...
- `docs\github-context\GITHUB_DRAFTS_AND_PRS_DIGEST_LATEST.md:160` — | [#605](https://github.com/Dealix-sa/dealix/pull/605) | OPEN | True | feat(commercial): official launch OS and 400 daily founder-review drafts |  | 2026-06-04T19:13:55Z | documentation, ci |
- `docs\github-context\GITHUB_DRAFTS_AND_PRS_DIGEST_LATEST.md:161` — | [#604](https://github.com/Dealix-sa/dealix/pull/604) | OPEN | True | feat(commercial): official launch OS and 400 daily founder-review drafts |  | 2026-06-04T19:13:38Z | documentation, frontend, ci |
- `docs\github-context\GITHUB_DRAFTS_AND_PRS_DIGEST_LATEST.md:162` — | [#603](https://github.com/Dealix-sa/dealix/pull/603) | OPEN | True | feat(commercial): official Launch OS — 400 daily review-only drafts + Social/Media OS + launch site |  | 2026-06-04T19:03:12Z | documentation, frontend, ci, backend |
- `docs\github-context\GITHUB_DRAFTS_AND_PRS_DIGEST_20260621-052954.md:160` — | [#605](https://github.com/Dealix-sa/dealix/pull/605) | OPEN | True | feat(commercial): official launch OS and 400 daily founder-review drafts |  | 2026-06-04T19:13:55Z | documentation, ci |
- `docs\github-context\GITHUB_DRAFTS_AND_PRS_DIGEST_20260621-052954.md:161` — | [#604](https://github.com/Dealix-sa/dealix/pull/604) | OPEN | True | feat(commercial): official launch OS and 400 daily founder-review drafts |  | 2026-06-04T19:13:38Z | documentation, frontend, ci |
- `docs\github-context\GITHUB_DRAFTS_AND_PRS_DIGEST_20260621-052954.md:162` — | [#603](https://github.com/Dealix-sa/dealix/pull/603) | OPEN | True | feat(commercial): official Launch OS — 400 daily review-only drafts + Social/Media OS + launch site |  | 2026-06-04T19:03:12Z | documentation, frontend, ci, backend |
- `docs\github-context\GITHUB_DRAFTS_AND_PRS_DIGEST_20260621-052728.md:160` — | [#605](https://github.com/Dealix-sa/dealix/pull/605) | OPEN | True | feat(commercial): official launch OS and 400 daily founder-review drafts |  | 2026-06-04T19:13:55Z | documentation, ci |
- `docs\github-context\GITHUB_DRAFTS_AND_PRS_DIGEST_20260621-052728.md:161` — | [#604](https://github.com/Dealix-sa/dealix/pull/604) | OPEN | True | feat(commercial): official launch OS and 400 daily founder-review drafts |  | 2026-06-04T19:13:38Z | documentation, frontend, ci |
- `docs\github-context\GITHUB_DRAFTS_AND_PRS_DIGEST_20260621-052728.md:162` — | [#603](https://github.com/Dealix-sa/dealix/pull/603) | OPEN | True | feat(commercial): official Launch OS — 400 daily review-only drafts + Social/Media OS + launch site |  | 2026-06-04T19:03:12Z | documentation, frontend, ci, backend |
- `docs\commercial\launch_kit\01_linkedin_launch_posts.md:137` — - And, where a documented result exists, written permission to use it as a case study. You set the disclosure level: anonymous, sector-only, or named. Nothing is published before your review and approval.

## Raw notable signals (sample)

- `business\_generated\founder-dashboard.json:62` — "next_ceo_decision": "Approve the review queue and ship the proposal to the highest-value demo account."
- `apps\web\public\dealix-og.svg:27` — <text x="0" y="0">COMMAND CENTERS · REVENUE OS · DELIVERY OS · REVIEW OS</text>
- `apps\web\lib\sales-machine\ultimate-sales-os.ts:71` — positioning: "Architecture, security review, custom modules, dedicated ops lead.",
- `apps\web\lib\sales-machine\ultimate-sales-os.ts:210` — proofAngle: "Daily decision velocity + weekly review adoption rate.",
- `apps\web\lib\sales-machine\ultimate-sales-os.ts:219` — solution: "Lead routing, draft outreach, human-review queue, and follow-up cadence.",
- `apps\web\lib\sales-machine\ultimate-sales-os.ts:224` — "Human-review queue (no auto-send)",
- `autonomous_growth\distribution_engine.py:123` — "manual review recommended before sending proposal"
- `apps\web\lib\sales-automation\lead-sources.ts:161` — hook: "I noticed you ship fast on delivery but the response window to inbound leads is wide. Dealix closes that window with a 24/7 draft + human-review flow.",
- `apps\web\lib\sales-automation\lead-sources.ts:304` — "That's exactly why every Dealix output carries a source note and a review gate. We do not send what a model generated blindly.",
- `apps\web\lib\sales-automation\lead-sources.ts:344` — lines.push("Drafts only. Human review required before any send. No auto-send.");
- `business\_data\knowledge_index.json:9` — "preview": "# Dealix Human Review Statement\n\nEvery outbound action involving the customer's brand, prospects, or money requires explicit human approval before it leaves the workspace.\n\n## Approval matrix\n\n| Action | Reviewer | Tool |\n| --- | -...
- `business\_data\knowledge_index.json:33` — "preview": "# Dealix AI Governance Statement\n\n## Default mode is deterministic\n\nDealix's operator scripts and review tooling do not require an LLM to run. The default produces deterministic, reproducible output. LLM-assist is opt-in and per task....
- `business\_data\knowledge_index.json:69` — "preview": "# Legal Review Triggers\n\nWhen Dealix engages outside legal counsel before signing.\n\n## Always\n- First engagement with a new enterprise (revenue > 100M SAR/year).\n- Multi-tenant deals.\n- Government / semi-government entities.\n- Any...
- `business\_data\knowledge_index.json:75` — "preview": "# Contract Handoff Checklist\n\nBefore a quote becomes a signed SOW:\n\n## Customer-side\n- [ ] Decision-maker named and email confirmed.\n- [ ] Billing contact named.\n- [ ] Customer's legal review status known (waived / pending / requir...
- `business\_data\knowledge_index.json:135` — "preview": "# Client responsibilities\n\nA successful Dealix engagement requires the customer to bring four things.\n\n## 1. A named commercial owner\n- One person who can approve drafts, accept deliverables, and decide priorities.\n- Time commitment...
- `business\_data\knowledge_index.json:165` — "preview": "# Retainer Expansion Playbook\n\n## When to start the conversation\nMonth 2 weekly review, after two healthy proof items are in the vault.\n\n## Expansion paths\n1. **Adjacent OS module**: customer on Revenue OS → add Review OS or Deliver...
- `business\_data\knowledge_index.json:189` — "preview": "# AI Output Quality Bar\n\nBefore any output is forwarded to the founder for review, it must clear:\n\n## Content checks\n- [ ] No banned claims (`scripts/lib/ai_eval.check_no_banned_claims`).\n- [ ] No autosend language (`check_no_autose...
- `business\_data\knowledge_index.json:219` — "preview": "# Prompt: Outreach Draft (English, v1)\n\nRole: Dealix founder.\nTask: Write a first-touch WhatsApp or email message to a commercial owner at a Saudi B2B company, anchored on a visible friction signal.\n\nRules:\n- No guarantees, no \"out...
- `business\_data\knowledge_index.json:243` — "preview": "# Prompt: Compliance Review (v1)\n\nRead a draft outbound message or proposal. Flag:\n- Banned claims (guarantees, fake metrics).\n- Missing scope clarifications.\n- Implied auto-send language.\n- Pricing inconsistencies vs. catalog.\n\nO...
- `business\_data\knowledge_index.json:345` — "preview": "# Weekly Client Review Rhythm\n\n## When\nSame slot every week, agreed at kickoff. 45 min default.\n\n## Agenda\n1. **What we shipped** (10 min) — completed deliverables.\n2. **What we found** (10 min) — friction log updates.\n3. **What w...
- `business\_data\knowledge_index.json:351` — "preview": "# Deliverable Acceptance Flow\n\n1. **Draft** — Founder produces, demo-marks if applicable.\n2. **Internal review** — Founder walks through against `ACCEPTANCE_CRITERIA_TEMPLATE.md`.\n3. **Delivery** — Sent to commercial owner with a clea...
- `business\_data\knowledge_index.json:381` — "preview": "# Live Workflow Review Script\n\nUsed during the 7-day diagnostic sprint, day 2-3 workshop.\n\n## Setup\n- 90-min slot.\n- Founder + customer's commercial owner + 1 operator who actually does the work.\n- Screen share their CRM, WhatsApp,...
- `business\_data\knowledge_index.json:393` — "preview": "# Dealix Demo Script (English)\n\nLength: 20 minutes. Audience: B2B commercial owner / founder.\n\n## (1) 2 min — Opening\n\n\"Dealix builds a real business operating system on top of the tools you already use. Not a new CRM, not an agenc...
- `business\_data\knowledge_index.json:453` — "preview": "# AI Review Gates\n\nEvery AI-touched artifact passes these gates before any external use.\n\n## Gate 1 — Safety check (pre-call)\n- Refuse banned phrases (guarantee, scrape, fake review, etc.).\n- Refuse oversized prompts.\n- Refuse if c...
- `business\_data\knowledge_index.json:471` — "preview": "# V11 Admin Access Boundary\n\n## Internal routes\n\nThese pages contain operational data and should not be served to the public web in production:\n\n- `/crm`, `/crm/*`\n- `/operator`\n- `/review-queue`\n- `/outreach-lab`\n- `/followups`...
- `business\_data\knowledge_index.json:477` — "preview": "# Founder-only routes\n\n| Route | Purpose | Production gating |\n| --- | --- | --- |\n| `/crm` | Pipeline view | IdP + RBAC role=founder |\n| `/operator` | Daily ops console | IdP + RBAC role=founder |\n| `/review-queue` | Draft approval...
- `business_autopilot\templates\outreach_templates_v2.yaml:149` — - New-review monitoring with professionally drafted responses for manual approval
- `business_autopilot\templates\outreach_templates_v2.yaml:393` — - New-review monitoring with professionally drafted responses for manual approval
- `business_autopilot\templates\outreach_templates_v2.yaml:712` — - Review monitoring with professionally drafted responses for manual approval
- `apps\web\lib\generated\founder-dashboard.ts:54` — nextCeoDecision: "Approve the review queue and ship the proposal to the highest-value demo account.",
- `apps\web\lib\company-os\company-os.ts:147` — owner: "Delivery lead + Founder review",
- `apps\web\lib\company-os\company-os.ts:148` — exitCriteria: "Workflow live, proof report generated, client review accepted.",
- `apps\web\lib\company-os\company-os.ts:156` — goal: "Run monthly review, capture proof, and pitch next OS module.",
- `apps\web\lib\company-os\company-os.ts:389` — description: "Build, review, and approve the first 100 leads plan (25 agencies / 20 training / 15 clinics / 15 brokers / 15 logistics / 10 partners).",
- `business\sales-machine\PERSUASION_ANGLE_MATRIX.md:6` — | 2 | Scattered reviews → trust wall | Inconsistent reply | Dealix turns reviews into a Review OS with weekly reports | Dealix يحوّل التقييمات لـ Review OS بتقارير أسبوعية | Clinic, Real estate |
- `business\sales-machine\OBJECTION_HANDLING_LIBRARY.md:8` — - **EN:** That's why every Dealix output carries a source note and a review gate. We do not send what a model generated blindly.
- `customers\_template\11_upsell_recommendation.md:25` — > review first; sending it externally is A3 → explicit approval.
- `customers\_template\07_next_action_board.md:11` — | 4 | Kick off delivery | founder | todo | | |
- `customers\_template\07_next_action_board.md:15` — Status values: `todo` · `in-progress` · `blocked-on-approval` · `done`.
- `business\sales-automation\exports\dealix-sales-machine-pack-2026-06-11.md:36` — Drafts only. Human review required before any send.
- `business\review\OUTREACH_REVIEW_WORKFLOW.md:14` — 2. Read the opener + follow-ups
- `business\review\OUTREACH_REVIEW_WORKFLOW.md:20` — - Approved means: "I would send this"
- `business\review\OUTREACH_REVIEW_WORKFLOW.md:21` — - It does NOT mean: "the system will send this"
- `business\retention\exports\monthly-review-demo-001-2026-06-11.md:30` — *Draft only. Founder + client sign-off required.*
- `business\reports\exports\dealix-daily-ceo-brief-2026-06-11.txt:19` — - [OK] Drafts Pending Review: target 0, current 14 (0%) — daily · off_track
- `business\reports\DAILY_CEO_BRIEF_TEMPLATE.md:17` — - Drafts Pending Review: 0 target
- `business\proposals\PROPOSAL_TEMPLATE_EN.md:50` — *Draft only. Requires human review before sending.*
- `business\proposals\PROPOSAL_TEMPLATE_AR.md:50` — *Draft only. Requires human review before sending.*
- `apps\web\lib\company-os\pipeline.ts:3` — export type Stage = "new" | "qualified" | "drafted" | "review" | "meeting" | "proposal" | "won" | "lost" | "retainer";
- `business\governance\OUTREACH_REVIEW_GATE.md:4` — No message may be sent to a prospect or client without human review and explicit approval.
- `business\governance\APPROVAL_MATRIX.md:6` — | Outreach send | Account lead | Account lead | Only after review |
- `business\proposals\generated\proposal-demo-test-Revenue_OS-en-2026-06-11.json:27` — "governance": "Weekly review calls. Human approval required for all client-facing sends.",
- `business\proposals\generated\proposal-demo-001-Revenue_OS-en-2026-06-11.json:27` — "governance": "Weekly review calls. Human approval required for all client-facing sends.",
- `business\proposals\generated\proposal-demo-001-Revenue_OS-ar-2026-06-11.json:27` — "governance": "Weekly review calls. Human approval required for all client-facing sends.",
- `business\data-room\PRODUCT_ARCHITECTURE.md:7` — 4. **Outreach** — drafts + review queue (no auto-send)
- `business\data-room\PARTNER_PROGRAM.md:18` — - لا auto-send بدون review
- `business\crm\schema.md:18` — "stage": "new | qualified | drafted | review | meeting | proposal | won | lost | retainer",
- `business\enterprise\SERVICE_LEVEL_BOUNDARIES.md:19` — - Monthly client review on the first Sunday of the month.
- `business\enterprise\SERVICE_LEVEL_BOUNDARIES.md:31` — - Reviewed in the weekly client review.
- `business\enterprise\ENTERPRISE_BUYER_FAQ_EN.md:17` — Never. Every outbound message goes through human review (Dealix founder + your commercial owner). This is enforced in code (`tests/test_no_auto_send.py`).
- `business\enterprise\AI_GOVERNANCE_STATEMENT.md:5` — Dealix's operator scripts and review tooling do not require an LLM to run. The default produces deterministic, reproducible output. LLM-assist is opt-in and per task.
- `business\proof\RETAINER_EXPANSION_PLAYBOOK.md:4` — Month 2 weekly review, after two healthy proof items are in the vault.
- `business\proof\RETAINER_EXPANSION_PLAYBOOK.md:18` — "You've seen Revenue OS produce X. The natural next layer is Review OS — same operating rhythm, same proof cadence, focuses on protecting your reputation while we scale outbound. Want to scope it for next quarter?"
- `business\demo\exports\dealix-demo-pack-2026-06-11.md:202` — ChatGPT generates text. Dealix runs a daily operator pack, queues drafts for human review, logs every approval, produces customer-facing proof reports, and protects you from auto-sending something embarrassing.
- `business\demo\exports\dealix-demo-pack-2026-06-11.md:250` — - Tell them what to bring (recent leads, recent WhatsApp threads, last quarter's review console).
- `business\demo\exports\dealix-demo-pack-2026-06-11-en.md:147` — ChatGPT generates text. Dealix runs a daily operator pack, queues drafts for human review, logs every approval, produces customer-facing proof reports, and protects you from auto-sending something embarrassing.
- `business\demo\exports\dealix-demo-pack-2026-06-11-en.md:195` — - Tell them what to bring (recent leads, recent WhatsApp threads, last quarter's review console).
- `business\demo\exports\dealix-demo-pack-2026-06-11-ar.md:147` — ChatGPT generates text. Dealix runs a daily operator pack, queues drafts for human review, logs every approval, produces customer-facing proof reports, and protects you from auto-sending something embarrassing.
- `business\demo\exports\dealix-demo-pack-2026-06-11-ar.md:195` — - Tell them what to bring (recent leads, recent WhatsApp threads, last quarter's review console).
- `business\demo\DEMO_QA_OBJECTIONS.md:10` — ChatGPT generates text. Dealix runs a daily operator pack, queues drafts for human review, logs every approval, produces customer-facing proof reports, and protects you from auto-sending something embarrassing.
- `business\demo\DEMO_CLOSE.md:23` — - Tell them what to bring (recent leads, recent WhatsApp threads, last quarter's review console).
- `business\persuasion\exports\outreach-drafts-2026-06-11.json:11` — "disclaimer": "DRAFT — Do not send without human review."
- `business\persuasion\exports\outreach-drafts-2026-06-11.json:22` — "disclaimer": "DRAFT — Do not send without human review."
- `business\persuasion\exports\outreach-drafts-2026-06-11.json:33` — "disclaimer": "DRAFT — Do not send without human review."
- `business\persuasion\exports\outreach-drafts-2026-06-11.json:44` — "disclaimer": "DRAFT — Do not send without human review."
- `business\persuasion\exports\outreach-drafts-2026-06-11.json:55` — "disclaimer": "DRAFT — Do not send without human review."
- `business\persuasion\exports\outreach-drafts-2026-06-11.json:66` — "disclaimer": "DRAFT — Do not send without human review."
- `business\delivery-workspace\DELIVERY_WORKSPACE_SYSTEM.md:24` — 6. Weekly → `generate_client_status_report.py` produces bilingual review.
- `business\delivery-workspace\CLIENT_KICKOFF_SOP.md:13` — 6. **Next steps (10 min):** weekly review slot, draft approval cadence.
- `business\lead-lists\exports\first-100-leads-plan-2026-06-11.md:55` — - Friday: 25 more leads researched + Friday review
- `business\lead-lists\exports\first-100-leads-plan-2026-06-11.md:58` — - No auto-send. Every draft needs human review.
- `tools\patch_intake_contract.py:73` — if any(token in text for token in ["review", "reviews", "تقييم", "تقييمات", "سمعة"]):
- `auto_client_acquisition\client_os\monthly_value_report.py:57` — r["next_step_recommendation"] = "Review drafts, approve sends manually, then refresh Proof Pack for retainer gate."
- `auto_client_acquisition\client_os\badges.py:68` — StatusBadge.NEEDS_REVIEW.value: "Needs Review",
- `company\sales\lead_qualification_engine.py:191` — """Generate markdown report of qualified leads for founder review."""
- `token-optimizer\09-file-handling\pipe-commands.md:24` — # فقط الأسطر التي تحتوي على TODO
- `token-optimizer\09-file-handling\pipe-commands.md:25` — grep -n "TODO\|FIXME\|HACK\|XXX" api/routes/clients.py
- `company\revenue_engine\REVENUE_ENGINE_V2.md:28` — - Review top 20 targets
- `company\reports\2026-06-08_MASTER_LITE_CEO_REPORT.md:13` — | 1 | Research Target clinics | clinics | 65 | WhatsApp Revenue OS + Review Intelligence OS | review_contact_and_send_manually |
- `company\reports\2026-06-08_MASTER_LITE_CEO_REPORT.md:14` — | 2 | Research Target clinics | clinics | 65 | WhatsApp Revenue OS + Review Intelligence OS | review_contact_and_send_manually |
- `company\reports\2026-06-08_MASTER_LITE_CEO_REPORT.md:18` — | 6 | Research Target restaurants | restaurants | 65 | Review Intelligence OS | review_contact_and_send_manually |
- `company\reports\2026-06-08_MASTER_LITE_CEO_REPORT.md:19` — | 7 | Research Target restaurants | restaurants | 65 | Review Intelligence OS | review_contact_and_send_manually |
- `company\reports\2026-06-08_MASTER_LITE_CEO_REPORT.md:22` — | 10 | Research Target عيادات ومراكز طبية #1 | clinics | 65 | WhatsApp Revenue OS + Review Intelligence OS | review_contact_and_send_manually |
- `company\reports\2026-06-08_MASTER_LITE_CEO_REPORT.md:23` — | 11 | Research Target عيادات ومراكز طبية #2 | clinics | 65 | WhatsApp Revenue OS + Review Intelligence OS | review_contact_and_send_manually |
- `company\reports\2026-06-08_MASTER_LITE_CEO_REPORT.md:28` — | 16 | Research Target مطاعم وكافيهات #1 | restaurants | 65 | Review Intelligence OS | review_contact_and_send_manually |
- `company\reports\2026-06-08_MASTER_LITE_CEO_REPORT.md:29` — | 17 | Research Target مطاعم وكافيهات #2 | restaurants | 65 | Review Intelligence OS | review_contact_and_send_manually |
- `company\reports\2026-06-08_MASTER_LITE_CEO_REPORT.md:34` — 1. Review top 20 rows in approval queue.
- `company\master_stable\master_stable_orchestrator.py:173` — "1. Review the approval queue.",
- `company\master\MASTER_COMPANY_OPERATING_SYSTEM.md:18` — - trust posture review
- `company\master\MASTER_COMPANY_OPERATING_SYSTEM.md:63` — - Review proposals sent
