# Dealix — طبقة الثقة — Trust Layer
<!-- PHASE 3 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> هذه **صفحة مبيعات** بقدر ما هي صفحة حوكمة — الثقة ميزة تجارية، لا التزام
> قانوني فقط. انظر أيضاً
> [`MARKET_INTELLIGENCE_TRUST_SECURITY_MATRIX_AR.md`](MARKET_INTELLIGENCE_TRUST_SECURITY_MATRIX_AR.md).

---

## 1. وعد الثقة — The Dealix Trust Promise

- No spam automation — لا أتمتة سبام.
- No scraping — لا استخراج بيانات.
- No cold WhatsApp — لا واتساب بارد.
- No fake proof — لا أدلة ملفّقة.
- No guaranteed revenue claims — لا ادعاءات إيراد مضمونة.
- No source-less answers — لا إجابة بلا مصدر.
- Human approval for external actions — موافقة بشرية لكل فعل خارجي.
- Audit logs for sensitive actions — سجلّ تدقيق للأفعال الحسّاسة.
- Proof packs for every project — Proof Pack لكل مشروع.

**الجملة:**

> Dealix لا يؤتمت الفوضى. Dealix يحكم الـworkflow قبل الأتمتة.
>
> Dealix doesn't automate chaos — it governs the workflow before automating.

---

## 2. الـ11 غير القابلة للتفاوض — The 11 Non-Negotiables

محكومة في الكود، كل واحدة باختبار يمرّ. المصدر الرسمي
[`docs/00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md)
و [`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) §3:

| # | القاعدة | الاختبار |
|---|---------|----------|
| 1 | `no_live_send` | `tests/test_no_live_send.py` |
| 2 | `no_live_charge` | `tests/test_no_live_charge.py` |
| 3 | `no_cold_whatsapp` | `tests/test_no_cold_whatsapp.py` |
| 4 | `no_scraping` | `tests/test_no_scraping.py` |
| 5 | `no_fake_proof` | `tests/test_no_fake_proof.py` |
| 6 | `no_unconsented_data` | `tests/test_no_unconsented_data.py` |
| 7 | `no_unverified_outcomes` | `tests/test_no_unverified_outcomes.py` |
| 8 | `no_hidden_pricing` | `tests/test_no_hidden_pricing.py` |
| 9 | `no_silent_failures` | `tests/test_no_silent_failures.py` |
| 10 | `no_unbounded_agents` | `tests/governance/test_agent_boundaries.py` |
| 11 | `no_unaudited_changes` | `tests/governance/test_audit_chain.py` |

إذا فشل أي منها في CI — **لا تدمج**. حقّق في السبب الجذري وأصلحه.

---

## 3. الثقة كإطار — Trust as a Framework

الثقة مستمرة (continuous assurance)، لا شهادة ثابتة لمرّة واحدة. تُبنى من
إشارات قابلة للتجميع: أدلة، سجلّات تدقيق، وموافقات — متوافقة مع منطق
NIST AI RMF وإطار الحوكمة في طبقة `05_governance_os`.

كل فعل خارجي = approval-first. كل فعل حسّاس = audit log. كل ادعاء = مصدر أو
truth label.

---

*Estimated outcomes are not guaranteed outcomes — النتائج التقديرية ليست
نتائج مضمونة.*
