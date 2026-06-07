# Dealix — Day-0 Real Activation · تشغيل اليوم صفر الحقيقي

_Last updated: 2026-06-07_

> This document is the honest, end-to-end answer to: **"stand the company up
> for real, now."** It separates what runs **today on a clean clone** from
> what needs **your inputs** (a real list, API keys, approvals). No inflated
> claims. Every customer-facing artifact carries the bilingual disclaimer.
>
> هذا المستند هو الإجابة الأمينة الكاملة لسؤال: **"شغّل الشركة فعلاً، الآن."**
> يفصل ما يعمل **اليوم على نسخة نظيفة** عمّا يحتاج **مدخلاتك** (قائمة حقيقية،
> مفاتيح API، موافقات). بدون مبالغة.

---

## 1. The one command — أمر واحد

```bash
make day0
# or: python scripts/dealix_day0.py
```

It generates today's **Operator Pack** under `data/day0/<date>/`:

| File | What it is | ما هو |
|---|---|---|
| `OPERATOR_PACK.md` | The index — run it top to bottom | الفهرس — اشتغل عليه بالترتيب |
| `prospects.md` / `.csv` | ICP-scored, ranked prospect shortlist + recommended offer | قائمة المرشّحين مُقيّمة ومرتّبة + العرض المقترح |
| `call_list.md` | Today's prioritized contacts + bilingual talking points | قائمة الاتصال اليوم + نقاط حوار |
| `draft_pack.md` | Pre-screened outreach drafts, queued for **your** approval | مسوّدات تواصل بانتظار موافقتك |
| `scorecard.md` | Founder daily scorecard to fill at 18:00 KSA | السجل اليومي للمؤسس |

**The system sends nothing.** It scores, ranks, drafts, and queues. *You*
approve and contact. This is non-negotiable rung **#8** (no external action
without approval). النظام لا يرسل شيئاً — أنت من يوافق ويتواصل.

---

## 2. What runs today on a clean clone — ما يعمل اليوم

| Capability | Command | Status |
|---|---|---|
| Customer-facing website builds | `make site-build` (`cd frontend && npm run build`) | ✅ builds, all routes |
| Day-0 operator pack | `make day0` | ✅ runs, writes files |
| Deterministic ICP scoring + qualification | `auto_client_acquisition/sales_os/` | ✅ tested |
| Doctrine hard gates | `pytest tests/test_no_*.py tests/test_dealix_day0.py` | ✅ 20 passing |
| Daily founder brief | `make cockpit` | ✅ runs |

The website (`frontend/`) is a full Next.js 15 bilingual app: home, services,
pricing (the 5-rung ladder), trust, agents, ops surfaces, diagnostic, and
checkout. It builds clean.

---

## 3. What needs your input to go fully live — ما يحتاج مدخلاتك

These are **founder-owned** steps. Dealix will not fabricate any of them —
that would violate the no-fake-claims and no-unapproved-action rules.

| # | Input | Why | How |
|---|---|---|---|
| 1 | **Your real prospect list** | The shipped seed is a clearly-labelled SAMPLE | Put real rows in `data/prospects.csv` (same columns as `data/prospects.seed.csv`); re-run `make day0` |
| 2 | **Warm list** (optional, richer drafts) | Relationship-aware outreach | `cp data/warm_list.csv.template data/warm_list.csv`, fill it |
| 3 | **LLM API key** | Live AI synthesis in the API/services | Set `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` in `.env` (see `.env.example`) |
| 4 | **Moyasar live mode** | To actually charge the 499/1,500/… offers | Founder-flipped only — `scripts/moyasar_live_cutover.py` |
| 5 | **Gmail / email OAuth** | Send approved drafts from your address | Configure per `docs/ops/` and re-OAuth |
| 6 | **Calling the entities** | The talking points are ready; the call is human | You dial / DM / email from `call_list.md`. No auto-dialer — by doctrine |
| 7 | **Domain + deploy** | Public website + API | `railway.json` / `docs/ops/DEPLOY_RUNBOOK.md` |

> On "calling entities": the pack hands you the *who*, the *why*, the *offer*,
> and bilingual *talking points*. The act of contacting a person/organization
> is a human, approval-gated step on purpose — Dealix never cold-automates
> outreach (rungs #1–#3, #8). الاتصال خطوة بشرية بموافقتك — بحكم الدكترين.

---

## 4. The daily rhythm — الإيقاع اليومي

```bash
# Morning (09:00 KSA)
make day0                       # generate today's operator pack
open data/day0/$(date -u +%F)/OPERATOR_PACK.md

# Through the day
#   → work call_list.md (5 contacts), send edited drafts yourself
#   → log replies/bookings inline in the checkboxes

# Evening (18:00 KSA)
#   → fill scorecard.md, paste into your daily log
make cockpit                    # single-screen status
```

---

## 5. Doctrine — الدكترين (enforced by tests)

1. No scraping. 2. No cold WhatsApp automation. 3. No LinkedIn automation.
4. No fake / un-sourced claims. 5. No guaranteed sales outcomes. 6. No PII in
logs. 7. No source-less knowledge answers. 8. No external action without
approval. 9. No agent without identity. 10. No project without Proof Pack.
11. No project without Capital Asset.

The 5-rung ladder: **Free Diagnostic → 499 Sprint → 1,500 Data Pack →
2,999–4,999/mo Managed Ops → 5K–25K Custom AI.**

---

_Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج
مضمونة._
