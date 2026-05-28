# Post 12 — ZATCA Phase 2 receipts for B2B SaaS · إيصالات ZATCA Phase 2 لـ B2B SaaS

**Cluster:** Technical Proof
**Best day:** Tuesday 09:00 KSA
**Expected length:** AR 600 words · EN 450 words

> **Status:** outline ready. Founder reviews ZATCA Phase 2 status
> against their own production setup before publishing.

---

## Arabic outline

**القاعدة:** أي شركة SaaS تأخذ payment من شركة سعودية في ٢٠٢٤+ تحت
ZATCA Phase 2 = e-invoicing مفروض.

**الـ requirements:**
- XML invoice بصيغة UBL 2.1 + Saudi extensions
- QR code يحوي 7 fields (seller name, VAT, timestamp, total, VAT
  total, hash, signature)
- CSID + private key للتوقيع
- ربط مع Fatoora portal (sandbox أولًا، ثم production)

**ما نراه في السوق:**
- ٦٠٪ من SaaS B2B الناشئة لا تفرّق بين Phase 1 (basic e-invoicing)
  و Phase 2 (clearance integration).
- ٤٠٪ تنتظر "حتى يطلب العميل" — وهذا late.

**في Dealix:**
- كل Moyasar transaction → ZATCA-compliant receipt تلقائيًا.
- Sandbox UUID في الـ pilot، production UUID بعد ZATCA sign-off.
- Customer يحصل على invoice في WhatsApp + Email.

**القاعدة الذهبية:** ابدأ ZATCA Phase 2 sandbox قبل أول SAR — ليس
بعدها.

---

## English outline

**Rule:** any SaaS taking payment from a Saudi company in 2024+
under ZATCA Phase 2 = e-invoicing is mandatory.

**Requirements:**
- XML invoice in UBL 2.1 + Saudi extensions
- QR code with 7 fields (seller name, VAT, timestamp, total, VAT
  total, hash, signature)
- CSID + private key for signing
- Fatoora portal integration (sandbox first, then production)

**What we see in market:**
- 60% of emerging B2B SaaS don't distinguish Phase 1 (basic
  e-invoicing) from Phase 2 (clearance integration).
- 40% wait "until customer asks" — too late.

**At Dealix:**
- Every Moyasar transaction → ZATCA-compliant receipt automatically.
- Sandbox UUID during pilot, production UUID after ZATCA sign-off.
- Customer gets invoice via WhatsApp + Email.

**Golden rule:** start ZATCA Phase 2 sandbox before your first
SAR — not after.

(Founder: link to ZATCA portal docs + your own implementation in
`integrations/zatca.py` before publishing.)
