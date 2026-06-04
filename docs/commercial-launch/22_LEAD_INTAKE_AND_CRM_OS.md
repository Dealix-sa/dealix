# Lead Intake and CRM OS — استلام العملاء ونظام CRM

How leads enter the pipeline and move through stages. The system ranks and drafts; the founder moves stages and sends manually.

## CRM stages — مراحل CRM

| Stage | Meaning — المعنى |
|---|---|
| `new` | Lead added, not yet researched — عميل مُضاف، لم يُبحَث بعد |
| `researched` | Context gathered — جُمع السياق |
| `draft_generated` | AI prepared a draft — أُعدّت مسودة |
| `founder_review` | Awaiting founder approval — بانتظار موافقة المؤسس |
| `manually_contacted` | Founder sent by hand — أرسل المؤسس يدويًا |
| `replied_positive` | Positive reply — رد إيجابي |
| `replied_negative` | Negative reply — رد سلبي |
| `diagnostic_booked` | Discovery/diagnostic scheduled — حُجزت جلسة |
| `diagnostic_sold` | Audit sold — بيع التدقيق |
| `pilot_proposed` | Pilot proposed — اقتُرحت التجربة |
| `pilot_sold` | Pilot sold — بيعت التجربة |
| `retainer` | On a retainer — على اشتراك |
| `disqualified` | Not a fit — غير مناسب |
| `suppressed` | Do not contact — لا تتواصل |

## Flow — التدفق

**English.** new → researched → draft_generated → founder_review → manually_contacted → replied_positive/negative. Positive replies progress to diagnostic and beyond. Negative replies move to disqualified or suppressed.

**عربي.** new ← researched ← draft_generated ← founder_review ← manually_contacted ← replied_positive/negative. الردود الإيجابية تتقدّم للتشخيص فما بعده. السلبية تنتقل إلى disqualified أو suppressed.

## Suppression rules — قواعد الكبت

**English.** Any opt-out, "no thanks", or do-not-contact request moves the lead to `suppressed` immediately and permanently. Suppressed leads are never re-contacted.

**عربي.** أي إلغاء اشتراك أو "غير مهتم" أو طلب عدم التواصل ينقل العميل إلى `suppressed` فورًا ودائمًا. لا يُعاد التواصل مع المكبوتين أبدًا.

## Intake rules — قواعد الاستلام

- No scraped contacts. No purchased lists framed as "from our database".
- Source of each lead is recorded.
- No PII beyond what the founder needs to make contact.

لا جهات مكشوطة. لا قوائم مشتراة تُوصَف بأنها "من قاعدة بياناتنا". مصدر كل عميل مُسجَّل. لا بيانات شخصية زائدة.

## Cross-links — روابط

- [06_FOUNDER_DAILY_REVIEW.md](06_FOUNDER_DAILY_REVIEW.md)
- [23_LEAD_OPS_FINAL_QA.md](23_LEAD_OPS_FINAL_QA.md)
- [05_CHANNEL_POLICY.md](05_CHANNEL_POLICY.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
