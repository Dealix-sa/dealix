# Dealix — Claims Register / سجل الادّعاءات

**Status:** canonical · **Owner:** Founder · **Updated:** 2026-06-06
**Purpose:** every claim Dealix makes about itself is registered here with its
evidence basis and an allowed/forbidden phrasing. If a claim is not in this
register, it does not go on a customer-facing surface.

> **Governing rule:** Proof before claim / الـ Proof قبل الادّعاء.
> Estimated outcomes are not guaranteed outcomes /
> النتائج التقديرية ليست نتائج مضمونة.

---

## 1. Claim classes / أصناف الادّعاء

| Class | Meaning | Marker |
|---|---|---|
| `MEASURED` | observed from a real event/ledger | plain number + source |
| `ESTIMATE` | projected / illustrative | `~` prefix + disclaimer |
| `CAPABILITY` | "the system can do X" — backed by a PRODUCTION_READY module | link to Module Status Map |
| `FORBIDDEN` | must never be said | — |

---

## 2. Allowed claims / الادّعاءات المسموحة

| # | Claim (EN) | Claim (AR) | Class | Evidence basis |
|---|---|---|---|---|
| A1 | "We surface evidenced revenue opportunities for review" | «نُظهر فرص إيراد مدعومة بالدليل للمراجعة» | CAPABILITY | Qualification + Routing (PRODUCTION_READY) |
| A2 | "We assemble a bilingual Proof Pack with consent + approval" | «نجمّع حزمة إثبات ثنائية اللغة بموافقة واعتماد» | CAPABILITY | Proof OS + `PROOF_PACK_V6_STANDARD.md` |
| A3 | "We clean and score your data across 6 quality dimensions" | «ننظّف بياناتك ونحسب جودتها على 6 أبعاد» | CAPABILITY | Data OS (PRODUCTION_READY) |
| A4 | "~X hours/week of manual prep saved (estimated)" | «~X ساعة أسبوعياً من العمل اليدوي (تقديري)» | ESTIMATE | requires `~` + disclaimer |
| A5 | "Every external message is drafted for your approval" | «كل رسالة خارجية تُصاغ لاعتمادك» | CAPABILITY | Governance OS + Human Approval Policy |
| A6 | "Your data stays yours — declared via a Source Passport" | «بياناتك تبقى ملكك — تُعلَن عبر Source Passport» | CAPABILITY | Source Passport requirement |

---

## 3. Forbidden claims / الادّعاءات المرفوضة

| # | Never say (EN) | Never say (AR) | Why |
|---|---|---|---|
| F1 | "Guaranteed revenue / guaranteed sales" | «نضمن زيادة المبيعات / إيراد مضمون» | no guarantees — non-negotiable |
| F2 | "Auto-sends WhatsApp/email for you" | «يرسل واتساب/إيميل تلقائياً» | no auto-send |
| F3 | "Cold WhatsApp / LinkedIn automation at scale" | «واتساب بارد / أتمتة لينكدإن بالجملة» | no cold/bulk outreach |
| F4 | "We scrape leads for you" | «نسحب العملاء (scraping)» | no scraping |
| F5 | "Proven X% uplift" (no consented evidence) | «إثبات زيادة X%» (بلا دليل بموافقة) | no fake proof |
| F6 | "Fully autonomous — no human needed" | «مستقل بالكامل بلا بشر» | human approval is mandatory |
| F7 | "[Planned/Roadmap module] is live today" | «وحدة مستقبلية متاحة الآن» | module-status honesty |

---

## 4. Estimate convention / اصطلاح التقديرات

- Every projected number carries a leading `~`.
- The disclaimer line accompanies it on the same surface.
- Source of the estimate (method) is linkable on request.

---

## 5. Enforcement

- `scripts/verify_dealix_positioning.py` scans customer-facing surfaces for the
  forbidden patterns in §3 (negated/"no auto-send" mentions are allowed).
- New claims are added here **before** appearing anywhere else.
- Companion: [`HUMAN_APPROVAL_POLICY.md`](HUMAN_APPROVAL_POLICY.md),
  [`../PROOF_PACK_V6_STANDARD.md`](../PROOF_PACK_V6_STANDARD.md).
