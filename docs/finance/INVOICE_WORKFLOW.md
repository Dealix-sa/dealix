---
title: Invoice Workflow
owner: Founder (Bassam)
status: active
last_review: 2026-05-23
---

# Invoice Workflow — تدفق الفواتير

## Purpose
End-to-end path of an invoice: draft → approve → send → track → reconcile. Designed for a small team; assumes founder reviews each invoice until volume justifies a finance hire.

## States

| State | Trigger | Owner |
|---|---|---|
| Draft | Trigger met per `BILLING_POLICY.md` | Delivery analyst or founder |
| Approved | Founder review and sign-off | Founder |
| Sent | E-invoice issued via ZATCA-compliant provider | Founder |
| Outstanding | Sent, not yet paid | Founder watches |
| Paid | Funds cleared and reconciled | Founder |
| Disputed | Client raises dispute | Founder |
| Written-off | Aged > 90 days, no recovery path | Founder (A2 written) |

## Steps
1. **Draft.** Analyst or founder creates draft with: client legal name, VAT number, line items, proof-of-delivery link, due date (Net 14 default).
2. **Approve.** Founder reviews against the trigger and proof; approves or sends back for fix.
3. **Send.** ZATCA-compliant e-invoice issued; PDF attached to send email; logged in invoice register with a unique INV-YYYY-NNN id.
4. **Track.** Outstanding aging buckets reviewed weekly: 0–14, 15–30, 31–60, 60+.
5. **Reconcile.** When payment lands, match by reference; record paid date; receipt issued.
6. **Disputes.** Pause aging clock during a dispute; resolve in writing; restart clock from resolution date.
7. **Write-off.** Past 90 days with no resolution path: founder writes A2 approval, marks written-off, logs lesson.

## Rules
- Default payment terms: Net 14. Net 30 only for enterprise contracts and only if signed in SOW.
- Reminder cadence on outstanding invoices: friendly note day 7, formal note day 15, escalation day 30.
- No re-issue under a new number to "reset the clock". Original aging persists.
- VAT lines correct and reconciled monthly.

## Operations
- Invoice register lives in finance system; export reconciled monthly to `docs/finance/registers/YYYY-MM.md` (folder created on first cycle).
- Weekly: founder reviews outstanding aging.

## Evidence
- Each row links: proposal, proof of delivery, sent email, paid receipt, dispute notes if any.

## Owner & cadence
- Owner: Founder.
- Cadence: per invoice; weekly aging review; monthly reconciliation.

## Cross-links
- [`BILLING_POLICY.md`](BILLING_POLICY.md)
- [`PAYMENT_RULES.md`](PAYMENT_RULES.md)
- [`FINANCIAL_DASHBOARD.md`](FINANCIAL_DASHBOARD.md)

---

## القسم العربي

**الحالات:** مسودة، معتمدة، مُرسلة، معلقة، مدفوعة، مُتنازَع عليها، مشطوبة.

**الخطوات:** صياغة، موافقة المؤسس، إصدار e-invoice متوافق مع ZATCA، تتبع المُسنّ الأسبوعي بفئات (0–14، 15–30، 31–60، 60+)، مطابقة عند الدفع، إيقاف العدّاد خلال النزاع، شطب بعد 90 يومًا بموافقة A2.

**القواعد:** Net 14 افتراضيًا، Net 30 للمؤسسات بنص SOW فقط. تذكير: يوم 7، يوم 15، يوم 30. لا إعادة إصدار برقم جديد لتصفير العدّاد.

**المالك:** المؤسس. **الإيقاع:** أسبوعي للمسنّ، شهري للمطابقة.
