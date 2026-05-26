# Dealix/Hermes Ultimate File Audit

Generated: 2026-05-26 14:11:15

- Present: 68/70
- Weighted readiness score: 98.6%
- Verdict: PASS

## Missing Files

- `docs/launch/DEALIX_LOCAL_PRODUCTION_OPERATING_MANUAL_AR.md`
- `docs/hermes/HERMES_CORE_V1_OPERATING_MANUAL_AR.md`

## Full Matrix

| Group | File | Present | Weight |
|---|---|---|---:|
| 01_core_runtime | `dealix.py` | True | 5 |
| 01_core_runtime | `dealix_local_ai.py` | True | 5 |
| 01_core_runtime | `local_ai/local_ai_config.json` | True | 5 |
| 01_core_runtime | `scripts/dealix-local-ai-env.ps1` | True | 5 |
| 01_core_runtime | `scripts/verify_local_ai.py` | True | 5 |
| 01_core_runtime | `scripts/dealix-operator-day.ps1` | True | 5 |
| 01_core_runtime | `scripts/dealix-launch-mode.ps1` | True | 5 |
| 02_quality_governance_safety | `scripts/score_local_output.py` | True | 5 |
| 02_quality_governance_safety | `scripts/local_generate_score_check.py` | True | 5 |
| 02_quality_governance_safety | `scripts/ledger_guard.py` | True | 5 |
| 02_quality_governance_safety | `scripts/backup_ledgers.py` | True | 5 |
| 02_quality_governance_safety | `scripts/runtime_snapshot.py` | True | 5 |
| 02_quality_governance_safety | `scripts/restore_latest_snapshot.py` | True | 5 |
| 02_quality_governance_safety | `scripts/pipeline_status_machine.py` | True | 5 |
| 02_quality_governance_safety | `docs/trust/HERMES_TRUST_MODEL_AR.md` | True | 5 |
| 03_sales_execution | `data/ledgers/prospects.json` | True | 5 |
| 03_sales_execution | `scripts/build_manual_send_queue.py` | True | 5 |
| 03_sales_execution | `scripts/build_followup_queue.py` | True | 5 |
| 03_sales_execution | `scripts/triage_reply.py` | True | 5 |
| 03_sales_execution | `scripts/lead_status_report.py` | True | 5 |
| 03_sales_execution | `scripts/ceo_close_report.py` | True | 5 |
| 03_sales_execution | `docs/ops/APPROVED_OUTREACH_TEMPLATES_AR.md` | True | 5 |
| 03_sales_execution | `docs/sales/APPROVED_REPLY_LIBRARY_AR.md` | True | 5 |
| 03_sales_execution | `docs/sales/FOLLOW_UP_LIBRARY_AR.md` | True | 5 |
| 04_revenue_payment | `scripts/proposal_from_lead.py` | True | 4 |
| 04_revenue_payment | `scripts/payment_request.py` | True | 4 |
| 04_revenue_payment | `scripts/start_paid_delivery.ps1` | True | 4 |
| 04_revenue_payment | `scripts/confirm_payment.ps1` | True | 4 |
| 04_revenue_payment | `scripts/revenue_ledger.py` | True | 4 |
| 04_revenue_payment | `data/ledgers/revenue_ledger.json` | True | 4 |
| 05_delivery_proof_retainer | `scripts/new_client_intake.py` | True | 4 |
| 05_delivery_proof_retainer | `scripts/delivery_tracker.py` | True | 4 |
| 05_delivery_proof_retainer | `scripts/generate_ai_trust_report.py` | True | 4 |
| 05_delivery_proof_retainer | `scripts/generate_delivery_accuracy_report.py` | True | 4 |
| 05_delivery_proof_retainer | `scripts/proof_from_lead.py` | True | 4 |
| 05_delivery_proof_retainer | `scripts/retainer_offer.py` | True | 4 |
| 05_delivery_proof_retainer | `scripts/complete_delivery.ps1` | True | 4 |
| 05_delivery_proof_retainer | `data/ledgers/delivery_ledger.json` | True | 4 |
| 06_hermes_core | `scripts/hermes_safe_init.py` | True | 4 |
| 06_hermes_core | `scripts/hermes_founder_brief.py` | True | 4 |
| 06_hermes_core | `scripts/hermes_opportunity_radar.py` | True | 4 |
| 06_hermes_core | `scripts/hermes_score.py` | True | 4 |
| 06_hermes_core | `scripts/hermes_capture_signal.py` | True | 4 |
| 06_hermes_core | `scripts/hermes_decision_memo.py` | True | 4 |
| 06_hermes_core | `scripts/hermes_deal_room.py` | True | 4 |
| 06_hermes_core | `scripts/hermes_compound_input.py` | True | 4 |
| 06_hermes_core | `scripts/hermes_log_outcome.py` | True | 4 |
| 06_hermes_core | `scripts/hermes_trust_pack.py` | True | 4 |
| 06_hermes_core | `scripts/hermes_weekly_review.py` | True | 4 |
| 06_hermes_core | `scripts/hermes-core-run.ps1` | True | 4 |
| 07_hermes_partner_productization | `scripts/hermes_partner_init.py` | True | 3 |
| 07_hermes_partner_productization | `scripts/hermes_partner_os.py` | True | 3 |
| 07_hermes_partner_productization | `scripts/hermes_partner_pack.py` | True | 3 |
| 07_hermes_partner_productization | `scripts/hermes_case_study.py` | True | 3 |
| 07_hermes_partner_productization | `scripts/hermes_productization_gate.py` | True | 3 |
| 07_hermes_partner_productization | `scripts/hermes-partner-product-run.ps1` | True | 3 |
| 07_hermes_partner_productization | `docs/partners/HERMES_PARTNER_OS_AR.md` | True | 3 |
| 07_hermes_partner_productization | `docs/productization/HERMES_PRODUCTIZATION_RULES_AR.md` | True | 3 |
| 08_key_ledgers | `data/ledgers/hermes_signals.json` | True | 4 |
| 08_key_ledgers | `data/ledgers/hermes_opportunities.json` | True | 4 |
| 08_key_ledgers | `data/ledgers/hermes_outcomes.json` | True | 4 |
| 08_key_ledgers | `data/ledgers/hermes_assets.json` | True | 4 |
| 08_key_ledgers | `data/ledgers/hermes_deal_rooms.json` | True | 4 |
| 08_key_ledgers | `data/ledgers/hermes_partners.json` | True | 4 |
| 08_key_ledgers | `data/ledgers/hermes_productization.json` | True | 4 |
| 09_manuals | `docs/launch/DEALIX_LOCAL_PRODUCTION_OPERATING_MANUAL_AR.md` | False | 2 |
| 09_manuals | `docs/hermes/HERMES_CORE_V1_OPERATING_MANUAL_AR.md` | False | 2 |
| 09_manuals | `docs/trust/HERMES_TRUST_MODEL_AR.md` | True | 2 |
| 09_manuals | `docs/partners/HERMES_PARTNER_OS_AR.md` | True | 2 |
| 09_manuals | `docs/productization/HERMES_PRODUCTIZATION_RULES_AR.md` | True | 2 |

## Interpretation

- 90%+ = system is operationally complete enough to sell and deliver.
- Missing core runtime or safety files must be fixed before launch.
- Missing partner/productization files is acceptable before first partner conversation, but should be completed soon.