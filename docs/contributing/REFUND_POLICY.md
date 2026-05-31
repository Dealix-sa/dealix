# Refund + Cancellation Policy · سياسة الاسترجاع والإلغاء

> Public-facing. Bilingual. Doctrine-aligned (transparent, no hidden
> terms — Doctrine #7).
>
> **Effective:** 2026-06-01. Supersedes any prior verbal commitments.

---

## Arabic — العربية

### 1. ضمان الـ Sprint السبع أيام (٤٩٩ ر.س — pilot_managed)

نرد ٤٩٩ ر.س كاملة لو:
- Sprint اكتمل بدون أي proof event مسجّل في الـ ledger (L3 أو أعلى)
- لم نقدم Top-10 prospects أو DQ Report ضمن ٧ أيام من kickoff
- اكتشف الـ DPA أن بياناتكم لم تكن usable بالأصل (نعيد قبل بدء أي
  outreach)

كيفية المطالبة: WhatsApp مباشر مع الفاوندر أو email
`refunds@dealix.me`. الرد خلال ٤٨ ساعة. الـ refund يصل خلال ٧
أيام بنكية.

### 2. الاشتراكات الشهرية (Starter ٩٩٩، Growth ٢٩٩٩، Scale ٧٩٩٩ ر.س/شهر)

- **شهر ١:** قابل للإلغاء أي وقت، استرجاع كامل خلال ٧ أيام من أول
  charge.
- **شهر ٢-٣:** إلغاء بإشعار ٧ أيام، استرجاع نسبي حسب أيام
  الاستخدام المتبقية في الـ cycle.
- **بعد ٣ شهور (auto-charge mode):** إلغاء بإشعار ١٤ يوم، لا استرجاع
  على الـ cycle الحالي.

كيفية الإلغاء: `cancel@dealix.me` أو من `/[locale]/customer-portal`
زر "Manage subscription". لا حاجة لمكالمة retention.

### 3. تجربة بريال واحد (pilot_1sar — ١ ر.س)

غير قابل للاسترجاع — هي transaction smoke test. القيمة تأتي من
التحقق أن الـ Moyasar loop يعمل قبل التزام أكبر.

### 4. Custom AI engagement (٥-٢٥ ألف ر.س)

شروط الـ refund تُحدد في عقد الـ engagement الفردي. القاعدة الافتراضية:
- Milestone-based payment (٣٠٪ kickoff، ٤٠٪ midway، ٣٠٪ delivery)
- استرجاع للـ milestone غير المكتمل
- لا استرجاع للـ milestone الذي وقّع عليه العميل

### 5. حالات لا نسترجع فيها

- لو العميل خرق DPA (مثل: رفض بيانات suppression list)
- لو طلب يخالف doctrine الـ ١١ (autonomous send، scraping، إلخ) —
  هذه طلبات نرفضها من البداية، لا تصل لمرحلة الـ refund.
- لو الـ proof events قُدّمت لكن العميل رفضها بسبب "لا نوافق على
  الـ messaging" — الموافقة على outreach drafts هي مسؤولية العميل.

### 6. التزامات إضافية

- كل refund decision مسجّل في `proof_ledger`.
- لو رفضنا refund، نشرح السبب كتابيًا في ٤٨ ساعة.
- لا charge مرة ثانية لنفس الـ subscription بعد إلغاء حتى لو نسيت
  الـ system.
- بيانات العميل تُحذف تلقائيًا بعد ٩٠ يوم من إنهاء العلاقة، إلا لو
  وقّع explicit retention agreement.

---

## English

### 1. Sprint guarantee (499 SAR — pilot_managed)

Full 499 SAR refund if:
- Sprint completes with zero proof events recorded in the ledger
  (L3 or higher)
- We failed to deliver Top-10 prospects or DQ Report within 7 days
  of kickoff
- DPA discovers your data was unusable to begin with (refund before
  any outreach)

How to claim: direct WhatsApp with the founder or
`refunds@dealix.me`. Response within 48h. Refund lands in 7 business
days.

### 2. Monthly subscriptions (Starter 999, Growth 2,999, Scale 7,999 SAR/mo)

- **Month 1:** cancel anytime, full refund within 7 days of first
  charge.
- **Months 2-3:** cancel with 7-day notice, prorated refund based on
  unused days in the cycle.
- **After 3 months (auto-charge mode):** cancel with 14-day notice,
  no refund on the current cycle.

How to cancel: `cancel@dealix.me` or from
`/[locale]/customer-portal` "Manage subscription" button. No
retention call required.

### 3. 1-SAR pilot

Non-refundable — it's a transaction smoke test. Value comes from
verifying the Moyasar loop works before bigger commitment.

### 4. Custom AI engagement (5-25K SAR)

Refund terms defined in each engagement contract. Default:
- Milestone-based payment (30% kickoff, 40% midway, 30% delivery)
- Refund for incomplete milestones
- No refund for milestones customer signed off on

### 5. Cases where we do not refund

- Customer violated the DPA (e.g. rejected the suppression list)
- Request violates the 11 doctrine non-negotiables (autonomous
  send, scraping, etc.) — we refuse these upfront, never reach the
  refund stage.
- Proof events were delivered but customer rejected the messaging —
  approving outreach drafts is the customer's responsibility.

### 6. Additional commitments

- Every refund decision logged in `proof_ledger`.
- If we refuse a refund we explain why in writing within 48h.
- No re-charging the same subscription after cancellation even if
  the system "forgets".
- Customer data auto-deletes 90 days after engagement ends, unless
  an explicit retention agreement is signed.

---

## Internal review

This policy is reviewed quarterly. Last revision: 2026-06-01.
Next review: 2026-09-01.

**Doctrine references:**
- #5 NO_UNCONSENTED_DATA — refund triggered if DPA wasn't honored
- #7 NO_HIDDEN_PRICING — this policy is the only pricing source
- #8 NO_SILENT_FAILURES — every refund logged + reason given
- #10 NO_UNAUDITED_CHANGES — policy changes require founder sign-off
  + 30-day notice to existing subscribers
