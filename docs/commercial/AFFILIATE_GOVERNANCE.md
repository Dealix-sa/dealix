# Dealix — حوكمة المسوّقين بالعمولة — Affiliate Governance
<!-- PHASE 3 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> ابدأ **مغلقاً، لا عاماً**. 5–10 مسوّقين موثوقين فقط، بمراجعة يدوية وإفصاح
> إلزامي.

---

## 1. القواعد — The Rules

- 5–10 trusted affiliates فقط.
- Approved scripts only — لا نص غير معتمد.
- Manual review لكل copy.
- Mandatory disclosure — إفصاح إلزامي عن العلاقة التسويقية.
- العمولة بعد `invoice_paid` فقط.

---

## 2. سير العمل — The Workflow

```
affiliate_submits_copy
   → compliance_review
      → approved / edit_required / blocked
         → tracking link
            → lead submitted
               → qualified
                  → invoice_paid
                     → commission_eligible
```

لا تُحتسب عمولة قبل `invoice_paid` — يحمي اختبار `no_unverified_outcomes`.

---

## 3. ممنوع — Prohibited

- ROI مضمون — guaranteed ROI.
- compliance مضمون.
- Dealix يرسل تلقائياً — أي إرسال خارجي بلا موافقة.
- spam · cold WhatsApp.
- fake proof.
- no disclosure — تسويق بلا إفصاح.
- ادعاءات غير معتمدة.

---

## 4. المواءمة مع الـ11 غير القابلة للتفاوض — The 11 Non-Negotiables

برنامج العمولة محكوم بنفس الـ11 المُختبَرة في الكود — المصدر
[`docs/00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md)
و [`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) §3:

`no_live_send` · `no_live_charge` · `no_cold_whatsapp` · `no_scraping` ·
`no_fake_proof` · `no_unconsented_data` · `no_unverified_outcomes` ·
`no_hidden_pricing` · `no_silent_failures` · `no_unbounded_agents` ·
`no_unaudited_changes`.

أي copy من مسوّق يخالف واحدة منها = `blocked` في مرحلة `compliance_review`.

---

*No fake proof · No guaranteed claims — النتائج التقديرية ليست نتائج مضمونة.*
