# Dealix Managed Revenue Ops Subscription Agreement
# اتفاقية اشتراك Managed Revenue Ops

> Monthly subscription contract template. Covers Starter (999),
> Growth (2,999), Scale (7,999 SAR/mo) tiers. Founder + Customer
> both sign before activation.

---

## Merge fields

`{{customer_company_name}}`, `{{customer_signatory_name}}`,
`{{tier_name}}` (Starter/Growth/Scale), `{{monthly_amount_sar}}`,
`{{subscription_start_date}}`, `{{contract_id}}`, `{{founder_name}}`.

---

## Arabic

### اتفاقية اشتراك Managed Revenue Ops

**رقم العقد:** {{contract_id}}
**الطبقة:** {{tier_name}} ({{monthly_amount_sar}} ر.س/شهر)

#### 1. نطاق الخدمة الشهري

- Approval queue يومي مع SLA ٢٤ ساعة
- Weekly Proof Pack (٤ أحداث L4+ متوقعة)
- Monthly review video call (٤٥ دقيقة)
- Bilingual reporting (AR + EN)
- Cockpit access (دائم)

تفاصيل لكل طبقة في `docs/playbooks/FAQ.md` § Pricing.

#### 2. شروط الدفع المتكررة

- **الدورة:** شهري، تجديد تلقائي
- **طريقة الدفع:** Moyasar (subscription)
- **توقيت الـ charge:** نفس تاريخ بدء الاشتراك من كل شهر
- **الفاتورة:** ZATCA Phase 2 compliant، تُصدر تلقائيًا

#### 3. سياسة الإلغاء

- **شهر ١:** قابل للإلغاء أي وقت، استرجاع كامل
- **شهر ٢-٣:** إشعار ٧ أيام، استرجاع نسبي
- **بعد ٣ شهور (auto-mode):** إشعار ١٤ يوم، لا استرجاع للـ cycle
  الحالي

التفاصيل: `docs/contributing/REFUND_POLICY.md`

#### 4. حماية البيانات + Doctrine

كما في Sprint contract — كل البنود تنطبق.

#### 5. شروط الـ SLA

- وقت الرد على inquiries: ٣٠ دقيقة في ساعات العمل
- وقت معالجة أي حالة طارئة: ٢٤ ساعة
- وقت الـ Monthly Proof Pack: قبل ٧ أيام من نهاية الشهر
- وقت الـ Weekly Proof Pack: قبل ٢٤ ساعة من نهاية الأسبوع

#### 6. التغييرات في الطبقة

- Upgrade (Starter → Growth): فوري، prorated
- Downgrade: عند نهاية الـ cycle الحالي
- Pause: ٣٠ يوم max، يُحفظ الـ proof_ledger

#### 7. التوقيع

[نفس بلوك التوقيع في Sprint contract]

---

## English

### Managed Revenue Ops Subscription Agreement

**Contract ID:** {{contract_id}}
**Tier:** {{tier_name}} ({{monthly_amount_sar}} SAR/mo)

#### 1. Monthly scope

- Daily approval queue, 24h SLA
- Weekly Proof Pack (4 L4+ events expected)
- Monthly review video call (45 min)
- Bilingual reporting (AR + EN)
- Cockpit access (always-on)

Tier details in `docs/playbooks/FAQ.md` § Pricing.

#### 2. Recurring payment

- **Cycle:** monthly, auto-renew
- **Method:** Moyasar (subscription)
- **Charge timing:** same date as subscription start, monthly
- **Invoice:** ZATCA Phase 2 compliant, auto-issued

#### 3. Cancellation policy

- **Month 1:** cancel anytime, full refund
- **Months 2-3:** 7-day notice, prorated refund
- **After 3 months (auto-mode):** 14-day notice, no refund on
  current cycle

Details: `docs/contributing/REFUND_POLICY.md`

#### 4. Data protection + Doctrine

Same as Sprint contract — all clauses apply.

#### 5. SLA terms

- Response to inquiries: 30 min in business hours
- Emergency handling: 24 hours
- Monthly Proof Pack: ≥ 7 days before month-end
- Weekly Proof Pack: ≥ 24h before week-end

#### 6. Tier changes

- Upgrade (Starter → Growth): immediate, prorated
- Downgrade: at end of current cycle
- Pause: 30 days max, proof_ledger preserved

#### 7. Signatures

[Standard signature block]

---

## Internal review checklist

- [ ] Tier name + monthly amount confirmed
- [ ] Customer billing address + VAT ID captured
- [ ] Auto-renew acknowledgment explicit
- [ ] Cancellation policy linked
- [ ] DPA + Doctrine attestation acknowledged
- [ ] Founder signed before customer
