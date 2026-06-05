# Dealix — Platform Source of Truth

> **Status:** CANONICAL · **Owner:** Founder · **Last reviewed:** 2026-06-05
>
> This is the single source of truth for what Dealix *is*, what is *sellable now*,
> and what is *future platform*. If any other document, README, deck, or website
> page conflicts with this file, **this file wins** and the other document must be
> corrected. Do not overclaim. Do not invent status.

---

## 1. Identity (one line)

**English:** Dealix — Saudi AI Business Operating System.

**العربية:** Dealix — نظام تشغيل الأعمال بالذكاء الاصطناعي للشركات السعودية والخليجية.

Revenue is **not** the identity. Revenue OS is the **first commercial wedge** we
use to enter a company. The platform is broader.

---

## 2. The official sentence

Dealix turns a company's scattered WhatsApp threads, Excel files, documents,
meetings, proposals, and uncounted follow-ups into **one operating system** that
knows:

- What is happening?
- What should happen next?
- Who approves it?
- What is the evidence?
- What is the next decision?

بالعربي: Dealix يحوّل الشركة من واتساب، Excel، ملفات، اجتماعات، عروض، وقرارات
مشتتة إلى نظام تشغيل واحد يعرف: ماذا يحدث؟ ماذا يجب أن يحدث؟ من يوافق؟ ما الدليل؟
وما القرار القادم؟

---

## 3. The platform map

```
Dealix Business OS
├─ Command OS      — executive decision rhythm
├─ Revenue OS      — leads, pipeline, follow-up, proposals (first wedge)
├─ Client OS       — account memory
├─ Delivery OS     — execution & SLA
├─ Support OS      — customer support intelligence
├─ Finance OS      — pricing, MRR, margin (ZATCA-aware)
├─ Data OS         — intake, normalization, consent, retention (PDPL-aware)
├─ Governance OS   — human approval, audit, no-overclaim, access control
├─ Proof OS        — evidence ledger, proof packs, claim validation
├─ Knowledge OS    — SOPs, playbooks, decision history
├─ Agent OS        — agent registry, contracts, permissions, logs
├─ Partner OS      — referrals, channels, co-delivery
├─ Academy OS      — adoption, AI literacy, onboarding
└─ Venture OS      — productization, verticals, licensing
```

---

## 4. The commercial wedge

We do **not** sell the whole vision at once.

| Level | Message |
|---|---|
| Vision | Dealix AI Business Operating System |
| Market entry | Dealix Command Sprint |
| First paid product | Command + Revenue + Proof + Governance Lite |
| Expansion | Client + Delivery + Support |
| Enterprise | Finance + Governance + Data |
| Ecosystem | Partner + Academy + Venture |

**The rule:** Widen the vision, narrow the execution, sell the first wedge, then
expand from inside the customer.

القاعدة: وسّع الرؤية، ضيّق التنفيذ، بع أول wedge، ثم وسّع من داخل العميل.

---

## 5. What is sellable now vs future platform

| Layer | Reality today | Sell today? |
|---|---|---|
| Command Sprint (7-day paid engagement) | Deliverable as a founder-led service | ✅ Yes |
| Revenue OS | Live/Beta engines + service delivery | ✅ Yes (as a service, not self-serve SaaS) |
| Proof OS | Beta — evidence registers + proof pack templates | ✅ Yes (as part of Sprint) |
| Governance OS | Beta — approval policy, claims register, audit concepts | ✅ Yes (as a trust feature) |
| Client OS / Delivery OS | Internal / Lite | ⚠️ Only as "Lite" inside Sprint |
| Finance OS | Docs-only / Beta | ❌ Not as a billing provider |
| Support / Knowledge / Academy | Internal / Docs-only | ❌ Roadmap |
| Partner OS / Venture OS | Future | ❌ Roadmap |

Authoritative per-module status: see [`MODULE_STATUS_MAP.md`](MODULE_STATUS_MAP.md).

---

## 6. Non-negotiables (the 11 doctrine rules)

1. Do **not** overpromise full automation.
2. **No** cold outreach, **no** scraping, **no** auto-send.
3. **No** financial / legal / security external actions without explicit human approval + log.
4. Human approval is required for any external customer-facing action.
5. Distinguish status honestly: LIVE / BETA / INTERNAL / DOCS_ONLY / DEPRECATED / BLOCKED / FUTURE.
6. Saudi-Arabic-first positioning.
7. No public claim without evidence in the claims register.
8. No case study without customer approval.
9. No data deletion without a logged record.
10. No pricing change without the Price Authority document.
11. Keep the repo commercially coherent **and** operationally verifiable.

---

## 7. Market context (why "Operating System" is the right language)

Saudi Arabia is moving clearly toward AI platforms and AI operating systems
(e.g. PIF-backed HUMAIN announcing "Humain One" as an AI operating system, with
expansion across data, models, and data centers). This validates the *language*
of an "AI Operating System" as aligned with the Saudi market direction —
**provided Dealix is operational and governed, not a claim.** That proviso is the
entire point of this document.

---

## 8. Document hierarchy

1. `PLATFORM_SOURCE_OF_TRUTH.md` (this file) — what Dealix is.
2. `DEALIX_BUSINESS_OS_ARCHITECTURE.md` — how the systems fit together.
3. `PRODUCT_FAMILY_MAP.md` — what we sell and the offer ladder.
4. `MODULE_STATUS_MAP.md` — the honest status of every module.
5. `PUBLIC_POSITIONING.md` — what we say publicly and what we never say.

Go-to-market, governance, operating-system specs, delivery, and founder rhythm
live under `docs/01_*` through `docs/05_*`.

---

## 9. Verification gates (must pass before any launch)

```bash
make env-check
python scripts/security_smoke.py
python -c "import api.main; print('api import OK')"
make prod-verify
```

A launch is **No-Go** if any gate fails and the failure is not documented as an
accepted blocker.
