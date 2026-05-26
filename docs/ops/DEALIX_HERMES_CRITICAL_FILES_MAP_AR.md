# Dealix/Hermes Critical Files Map

## الهدف

هذا الملف يوضح أهم ملفات Dealix/Hermes التي يجب التأكد من وجودها لأنها تعطي أكبر فائدة للمشروع.

## 1. Core Runtime

- `dealix.py`
- `dealix_local_ai.py`
- `local_ai/local_ai_config.json`
- `scripts/verify_local_ai.py`
- `scripts/dealix-operator-day.ps1`
- `scripts/dealix-launch-mode.ps1`

الفائدة: تشغيل محلي، فحص الصحة، تشغيل يومي، launch gate.

## 2. Trust + Safety

- `scripts/score_local_output.py`
- `scripts/local_generate_score_check.py`
- `scripts/ledger_guard.py`
- `scripts/pipeline_status_machine.py`
- `scripts/hermes_trust_pack.py`
- `docs/trust/HERMES_TRUST_MODEL_AR.md`

الفائدة: منع مخرجات ضعيفة أو خطرة، حماية السجلات، ضبط الصلاحيات.

## 3. Sales

- `scripts/build_manual_send_queue.py`
- `scripts/build_followup_queue.py`
- `scripts/triage_reply.py`
- `scripts/proposal_from_lead.py`
- `scripts/payment_request.py`

الفائدة: تحويل lead إلى reply/proposal/payment.

## 4. Revenue + Delivery

- `scripts/revenue_ledger.py`
- `scripts/start_paid_delivery.ps1`
- `scripts/confirm_payment.ps1`
- `scripts/delivery_tracker.py`
- `scripts/generate_ai_trust_report.py`
- `scripts/proof_from_lead.py`
- `scripts/retainer_offer.py`

الفائدة: تحويل البيع إلى تسليم وإثبات وريتينر.

## 5. Hermes Founder Brain

- `scripts/hermes_founder_brief.py`
- `scripts/hermes_opportunity_radar.py`
- `scripts/hermes_score.py`
- `scripts/hermes_deal_room.py`
- `scripts/hermes_log_outcome.py`
- `scripts/hermes_weekly_review.py`

الفائدة: تركيز المؤسس، تقييم الفرص، ذاكرة نتائج.

## 6. Partner + Productization

- `scripts/hermes_partner_os.py`
- `scripts/hermes_partner_pack.py`
- `scripts/hermes_case_study.py`
- `scripts/hermes_productization_gate.py`

الفائدة: توزيع، Case Studies، منع بناء SaaS قبل وجود Proof.

## الأمر النهائي

```powershell
.\scripts\dealix-hermes-readiness.ps1
```

## تفسير النتيجة

* إذا File Audit = PASS وRuntime Check = PASS، النظام جاهز للتشغيل.
* إذا Benefit Map تولد، افتحه لمعرفة أهم إجراء.
* إذا missing files ظهرت، ابدأ بالملفات من Core Runtime ثم Trust ثم Sales.
