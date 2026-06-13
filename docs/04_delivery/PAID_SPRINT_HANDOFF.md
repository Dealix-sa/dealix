<!-- Wave 6 | Owner: Founder | Arabic-first -->

# Paid Sprint Handoff — تسليم العميل المدفوع

**Trigger / المُطلِق:** `payment_status = paid` في `data/revenue/payments.jsonl`.

> الإيراد يُحتسب فقط بعد دليل دفع موثّق. لا تبدأ التسليم قبل الدفع.

---

## Steps / الخطوات

بمجرد تأكيد الدفع:

1. **Create customer workspace / أنشئ مساحة العميل**
   ```
   python scripts/create_customer_workspace.py --name "company-name"
   ```
2. **Create intake checklist / قائمة الاستلام** → `customers/<name>/00_intake.md`.
3. **Set Day 1 delivery task / مهمة اليوم الأول** → Intake + Company Intelligence.
4. **Create proof pack skeleton / هيكل Proof Pack** → `customers/<name>/10_proof_pack.md`
   (يرجع إلى القالب `docs/delivery/PROOF_PACK_TEMPLATE.md`).
5. **Create upsell recommendation placeholder / مكان توصية التوسعة** →
   `customers/<name>/11_upsell_recommendation.md`.

---

## Customer workspace structure / هيكل مساحة العميل
```
customers/company-name/
  00_intake.md
  01_company_intelligence.md
  02_diagnostic_summary.md
  03_command_sprint_scope.md
  04_revenue_map.md
  05_proof_register.md
  06_approval_register.md
  07_next_action_board.md
  08_executive_command_brief.md
  09_delivery_log.md
  10_proof_pack.md
  11_upsell_recommendation.md
```

## After handoff / بعد التسليم
- حدّث المرحلة إلى `delivery_started` وأضف الشركة إلى `reports/delivery/active_sprints.md`.
- تابع يوميًا عبر `docs/04_delivery/DELIVERY_DAILY_RHYTHM.md` و `reports/delivery/daily_delivery_brief.md`.

> لا بيانات عميل لتدريب نماذج · كل إرسال خارجي بموافقة · لا حالة نجاح بدون إذن.
