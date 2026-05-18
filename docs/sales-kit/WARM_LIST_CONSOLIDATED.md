# Consolidated Warm List — القائمة الدافئة الموحّدة

> **Status:** Founder reference. Single source of truth for the warm-list motion.
> This file merges and deduplicates `WARM_LIST_WORKFLOW.md`, `dealix_leads_20_real.md`,
> and `dealix_leads_50_expanded.md` into one prioritized list.
>
> **Canonical narrative — must conform.** Dealix is an approval-first revenue
> operations radar for Saudi B2B companies: it reads the customer's pipeline, ranks
> opportunities, and drafts Gulf-Arabic outreach. Every external action is
> **draft-only** — Dealix never sends on the customer's behalf without explicit
> human approval. No auto-booking, no binding auto-qualification. Entry is a free
> diagnostic; the first paid offer is the **499 SAR 7-Day Revenue Proof Sprint**.
> Outcomes are evidenced opportunities, not guaranteed results. Full statement:
> `docs/ops/launch_content_queue.md` → "Canonical positioning".

---

## 0. How this list was built — كيف بُنيت القائمة

- **Sources merged:** the 20-real list, the 50-expanded list, and the warm-list
  workflow's "20 named personal contacts" doctrine.
- **Deduplicated:** Salla, Foodics, Lucidya, BRKZ, Lean, Zid, Sary, Retailo,
  Rekaz, Mozn, Mnzil, Logexa appeared in both lead files — each kept once.
- **Drift removed.** The source lead files contained narrative now retired:
  cold WhatsApp blasts, "1 SAR pilot", "45-second response", BANT auto-qualify,
  Apollo/Hunter scraping tools, and a 24-hour 50-message sprint. **None of that
  carries into this list.** This list is a *warm* list only — every row is a
  named contact or a named-introduction target, contacted on the channel the
  relationship already uses, one human message at a time, draft-only.
- **The 50-expanded "cold outreach", "paid ads", and "scraping tool" tiers are
  excluded by design** — they violate the non-negotiables. Only the warm and
  named-founder rows survive the merge.

### ICP-fit scoring — conceptual

Each lead is ranked against the five ICP dimensions used by
`auto_client_acquisition/sales_os/icp_score.py` (`ICPDimensions`):

| Dimension | What it measures here |
|---|---|
| `b2b_service_fit` | Is this a Saudi B2B company with a real pipeline Dealix can read? |
| `data_maturity` | Does it already hold structured pipeline / lead / CRM data? |
| `governance_posture` | Does it value approval-first, evidence-trailed operations? |
| `budget_signal` | Visible funding / revenue / willingness for a 499 SAR sprint? |
| `decision_velocity` | Founder reachable + able to say yes without a long committee? |

`icp_score` averages the five (0–100). Ranks below are **conceptual estimates**
for founder prioritization, not verified scores — they are recomputed once a real
intake exists. Rank bands: **A = 80+**, **B = 60–79**, **C = < 60**.

---

## 1. The consolidated list — القائمة

| # | Name | Company | Segment | City | Why warm | ICP-fit rank | Pain hypothesis | Channel | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Abdullah Al-Assiri | Lucidya | Enterprise CXM SaaS | Riyadh | Surname affinity — genuine personal opener; warm-list-eligible as a named-introduction basis | A (~84) | BDR team spends hours on first-touch triage; opportunities cool before they are ranked | LinkedIn (founder's own account, single message) | NOT_CONTACTED |
| 2 | Ahmad Al-Zaini | Foodics | Restaurant POS SaaS | Riyadh | Series C milestone — natural, true congratulations opener | A (~82) | Geographic expansion means multi-dialect follow-up; restaurant onboarding leads leak without organized follow-up | LinkedIn | NOT_CONTACTED |
| 3 | Hisham Al-Falih | Lean Technologies | Open-banking / fintech infra | Riyadh | Founder studied Lean's API craft — honest, specific opener | A (~81) | Long fintech sales cycle; opportunities cool before solutions-engineering capacity reaches them | LinkedIn | NOT_CONTACTED |
| 4 | Ibrahim Manna | BRKZ | Construction-tech marketplace | Riyadh | $30M debt round is a true, public, specific opener | B (~78) | Inside-sales team splits the day across quotes and follow-ups; large contractor opportunities go un-ranked | LinkedIn | NOT_CONTACTED |
| 5 | Nawaf Hariri | Salla | E-commerce platform | Jeddah | Possible app-store / partner angle; approach as a partnership exploration, not a cold pitch | B (~76) | Merchant-facing pipeline is large but un-prioritized; partner add-on idea needs evidenced proof first | LinkedIn or X (whichever relationship channel exists) | NOT_CONTACTED |
| 6 | Sultan Mofarreh | Zid | E-commerce platform | Riyadh | Same merchant-enablement thesis as Salla | B (~72) | Supplier/merchant opportunities cool without organized follow-up | LinkedIn | NOT_CONTACTED |
| 7 | Mohammed Aldossary | Sary | B2B SMB marketplace | Riyadh | B2B marketplace = clean Dealix fit; supplier accounts are a real pipeline | B (~71) | Supplier-account follow-up is unstructured; opportunities go cold | LinkedIn | NOT_CONTACTED |
| 8 | Talha Ansari | Retailo | B2B retail marketplace | Riyadh | Same B2B-marketplace fit as Sary | B (~68) | Retailer-account opportunities un-ranked before follow-up | LinkedIn | NOT_CONTACTED |
| 9 | Founder (to confirm) | Mozn | AI / ML platform | Riyadh | An AI company already values governed AI — short education cycle | B (~67) | Sales pipeline lacks an approval-first follow-up layer; recognizes the governance value fast | LinkedIn (confirm named founder before any contact) | NOT_CONTACTED |
| 10 | Founder (to confirm) | Rekaz | SMB SaaS (booking + CRM) | Riyadh | Sells to small owners — Arabic-first drafting is high value | B (~64) | Small-owner pipeline; owners need natural-Arabic follow-up drafts | LinkedIn (confirm named founder) | NOT_CONTACTED |
| 11 | Founder (to confirm) | Mnzil | Proptech | Riyadh | Series A from a named fund — visible budget signal | B (~62) | Broker pipeline cools fast; needs ranked opportunities + drafts | LinkedIn (confirm named founder) | NOT_CONTACTED |
| 12 | Founder (to confirm) | Logexa | Logistics platform | Riyadh / Dammam | B2B logistics contracts have long follow-up tails | C (~58) | B2B contract opportunities un-tracked; small commercial team | LinkedIn (confirm named founder) | NOT_CONTACTED |
| 13 | Commercial lead (to confirm) | Merit Incentives | HR-tech | Riyadh | B2B HR sales cycle is a fit; needs a named, warm contact first | C (~56) | HR-tech B2B opportunities lack organized follow-up | Named introduction only | NOT_CONTACTED |
| 14 | Commercial lead (to confirm) | Bayzat (Saudi) | HR SaaS | Riyadh | Saudi expansion needs local-dialect follow-up drafting | C (~55) | Expansion pipeline; multi-dialect follow-up gap | Named introduction only | NOT_CONTACTED |

> Rows 9–14 are **not yet contactable** — they need a named founder/contact and a
> genuine warm basis (a relationship met at least once, or a named introduction)
> before they enter the outreach queue. Until then they sit at `NOT_CONTACTED`
> and are research targets, not message targets.

---

## 2. Founder's personal warm contacts — معارف المؤسس الشخصية

The `WARM_LIST_WORKFLOW.md` doctrine is built on **20 named personal contacts the
founder has met at least once**. Those names are personal and live only in the
founder's own engagement record — they are **not** listed in this repository file.

**Action for the founder:** before running the 14-day cadence, fill the table
below in a private copy with the real names. Each row must carry a true
`relationship_basis` (the consent record), per `WARM_LIST_WORKFLOW.md` §3.

| # | Name | Relationship basis (consent record) | Channel relationship uses | Segment of their company / network | Status |
|---|---|---|---|---|---|
| P1 | _____ | e.g. "met at Biban 2024" | WhatsApp / email | _____ | NOT_CONTACTED |
| P2 | _____ | _____ | _____ | _____ | NOT_CONTACTED |
| ... | (up to 20) | _____ | _____ | _____ | NOT_CONTACTED |

The named-company rows (1–14 above) are the **introduction-target** layer:
the founder asks personal contacts P1–P20 for a warm introduction to them.
No company in section 1 is contacted cold.

---

## 3. Top 5 ranked leads — أعلى 5 أولوية

1. **Abdullah Al-Assiri — Lucidya** (A, ~84) — surname affinity gives the highest
   genuine-opener probability; enterprise CXM is a clean pipeline fit.
2. **Ahmad Al-Zaini — Foodics** (A, ~82) — true Series-C congratulations opener;
   multi-dialect expansion pain maps directly onto Dealix's drafting layer.
3. **Hisham Al-Falih — Lean Technologies** (A, ~81) — long fintech sales cycle is
   exactly the "opportunities cool before SE capacity" pain Dealix ranks.
4. **Ibrahim Manna — BRKZ** (B, ~78) — public $30M-debt opener; inside-sales
   quote/follow-up split is a strong, specific pain hypothesis.
5. **Nawaf Hariri — Salla** (B, ~76) — partnership-exploration angle; large
   merchant pipeline, but approach as an evidenced partner conversation only.

---

## 4. What this list refuses — ما ترفضه هذه القائمة

- **No cold outreach.** Every row is a named warm contact or a named-introduction
  target. The 50-expanded file's cold-outreach, paid-ads, and scraping tiers are
  deliberately excluded.
- **No automation.** One human message per contact, on the existing relationship
  channel. No bulk send, no LinkedIn automation, no cold WhatsApp.
- **No auto-qualification.** A reply triggers the founder-run qualification gate
  (`FIRST_3_DIAGNOSTIC_SCRIPT.md` rubric); the qualification is advisory, not
  binding.
- **No guaranteed outcomes.** The offer is a free diagnostic then a 499 SAR
  sprint. Outcomes are evidenced opportunities, not guaranteed results.

---

## 5. Where this list feeds — إلى أين تذهب هذه القائمة

1. **Daily cadence:** `docs/distribution-os/14_DAY_SPRINT.md` — Day 2 onward
   draws its 10 then 50 War Room targets from this list.
2. **Scorecard:** `scripts/war_room_scorecard.py` builds the daily War Room row.
3. **Outreach drafts:** `docs/sales-kit/OUTREACH_DRAFTS_QUEUED.md` holds the
   founder-approval drafts for the top rows.
4. **Reply handling:** `docs/sales-kit/WARM_LIST_WORKFLOW.md` §4–5 governs the
   five-decision qualification gate.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
