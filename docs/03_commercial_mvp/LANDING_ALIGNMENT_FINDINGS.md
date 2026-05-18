# Landing Alignment Findings — مراجعة محاذاة صفحات الهبوط

> Audience: founder ops. Review date: 2026-05-18. Reviewer: Machine M4 (Content & Promotion).
> Scope: `landing/` pages vs. the canonical 7-offer registry (`landing/assets/data/services-catalog.json`) and the 5-step conversion funnel.
>
> Cross-link: [services-catalog.json](../../landing/assets/data/services-catalog.json), [SPRINT_DELIVERY_PLAYBOOK.md](./SPRINT_DELIVERY_PLAYBOOK.md), [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md).

---

## 1. Summary — الملخص

The canonical source of truth is `services-catalog.json` (generated from `auto_client_acquisition/service_catalog/registry.py`, schema_version 1.0). It defines **7 offers** at a clean ladder: **0 / 499 / 1,500 / 2,999 / 1,500 / 7,500 SAR** plus one custom partner offer.

`services.html` matches the registry exactly and should be treated as the reference page. Three other pages — `pricing.html`, `compare.html`, `annual-pricing.html` — carry a **different, fabricated pricing ladder** (999 / 7,999 / 12,000 / 5,000 SAR) and tier names that do not exist in the registry. This is an Article 11 (single source of truth) violation and must be reconciled before launch.

No non-negotiable claim violation was found that required an in-place HTML fix. The pricing mismatch is a consistency defect, not a forbidden-claim defect — so per the M4 brief, this document is the fix-list; the HTML is left for the founder to reconcile, except where noted in section 4.

`services.html` يطابق السجل المرجعي تماماً. ثلاث صفحات (`pricing.html`، `compare.html`، `annual-pricing.html`) تحمل سلّم تسعير مختلفاً غير موجود في السجل — وهذا تعارض يجب حسمه قبل الإطلاق.

---

## 2. Canonical 7-offer registry — السجل المرجعي

| # | Offer ID | EN name | Price SAR | Unit | Funnel stage |
|---|---|---|---|---|---|
| 1 | `free_mini_diagnostic` | Free Mini Diagnostic | 0 | one-time | discovery |
| 2 | `revenue_proof_sprint_499` | 499 SAR Revenue Proof Sprint | 499 | one-time | first_paid |
| 3 | `data_to_revenue_pack_1500` | Data-to-Revenue Pack | 1,500 | one-time | expansion |
| 4 | `growth_ops_monthly_2999` | Growth Ops Monthly | 2,999 | per_month | monthly |
| 5 | `support_os_addon_1500` | Support OS Add-on | 1,500 | per_month | support_addon |
| 6 | `executive_command_center_7500` | Executive Command Center | 7,500 | per_month | executive |
| 7 | `agency_partner_os` | Agency Partner OS | custom | custom | channel |

The brief's stated price band — **499 / 1,500 / 2,999–4,999 SAR** — is consistent with offers 2–4. Note: the registry sets the top managed tier at **7,500**, not 4,999; the "2,999–4,999" band in the brief appears to reference Growth Ops only. **Recommendation:** confirm with the founder whether the managed band ceiling is 2,999 (Growth Ops) or 7,500 (Executive Command Center), and lock one number into all copy.

---

## 3. Findings — fix list / قائمة الإصلاح

### F1 — `pricing.html`: fabricated ladder (HIGH)
The page shows a **6-tier ladder** with prices and names absent from the registry:
- "Executive Command Center — 12,000 ريال/شهر" — registry says **7,500**.
- "Scale OS — 7,999 ريال/شهر" — **no such offer** in the registry.
- "Growth OS — 2,999" — correct, but labeled "Growth OS" not "Growth Ops Monthly".
- "Revenue Proof Sprint — 499" — correct.
- "Data Pack — 1,500" — correct.
- "Mini Diagnostic — free" — correct.
- "Enterprise — تواصل" — not in the registry (acceptable as a contact-only tier, but should be marked clearly as out-of-registry custom).
- The page also omits **Support OS Add-on (1,500/mo)** entirely.

**Fix:** rebuild `pricing.html` tiers from `services-catalog.json`. Remove "Scale OS 7,999". Correct Executive Command Center to 7,500. Add Support OS Add-on. Use the registry `name_ar` / `name_en` strings verbatim.

### F2 — `pricing.html`: comparison table references non-existent plans (HIGH)
The "مقارنة سريعة" table columns are: "Pilot 1 ريال", "Starter 999", "Growth 2,999", "Scale 7,999". Three of four (**Pilot 1 SAR, Starter 999, Scale 7,999**) do not exist in the registry. The "1 ري' pilot" also conflicts with the 499 SAR sprint as the first paid step.

**Fix:** replace the comparison table columns with registry offers: Free Mini Diagnostic / Revenue Proof Sprint 499 / Growth Ops 2,999 / Executive Command Center 7,500.

### F3 — `compare.html`: wrong sprint and managed prices (HIGH)
Line ~178 states: `✓ 5,000 SAR sprint (refundable) · 12,000 SAR/mo Managed Partner`. Registry says the sprint is **499**, and the top managed tier is **7,500** (or 2,999 for Growth Ops). The "5,000 SAR sprint" figure is wrong by an order of magnitude and would mislead a comparison-stage prospect.

**Fix:** change to `499 SAR Revenue Proof Sprint (full refund within 14 days) · 2,999 SAR/mo Growth Ops`. Keep the refund wording consistent with the registry `refund_policy_*` fields.

### F4 — `annual-pricing.html`: annual figures derived from fabricated monthly prices (HIGH)
The annual page computes 12-month totals from 999 / 2,999 / 7,999. Two of three base prices are wrong (999 and 7,999 are not registry offers). Only the 2,999 → annual figure is defensible.

**Fix:** rebuild annual figures from registry monthly offers only: Growth Ops 2,999/mo and Executive Command Center 7,500/mo. Remove the 999 and 7,999 columns. Keep the "~17% / two months free" framing only if it is an actual approved discount — confirm with the founder; if not approved, remove the discount claim.

### F5 — Tier naming drift (MEDIUM)
"Growth OS", "Scale OS", "Starter", "Pilot" appear across pages as informal names. The registry names are **Free Mini Diagnostic / 499 SAR Revenue Proof Sprint / Data-to-Revenue Pack / Growth Ops Monthly / Support OS Add-on / Executive Command Center / Agency Partner OS**.

**Fix:** standardize on registry `name_ar` / `name_en` across all landing pages. Pick one display name per offer and use it everywhere.

### F6 — `start.html` / `pricing.html` "Pilot" vs "Sprint" language (MEDIUM)
`start.html` is internally consistent at 499 SAR but uses "7-Day Pilot" / "Managed Pilot". The registry, the case studies, and the LinkedIn posts all use "Revenue (Intelligence/Proof) Sprint". "Pilot" and "Sprint" being used for the same 499 SAR offer is a naming inconsistency, not a price one.

**Fix:** pick one term. Recommended: **"Revenue Proof Sprint"** (matches the registry offer ID and `name_en`). Apply across `start.html`, `pricing.html`, `diagnostic.html`.

### F7 — Funnel chain gap (MEDIUM)
The intended 5-step funnel is `lead-score-calculator → compare → diagnostic → start → managed`. Observed:
- `lead-score-calculator.html` CTAs point to `/diagnostic-real-estate.html` and `/start.html` — it **skips `compare.html`**.
- `diagnostic.html` CTA points correctly to `/start.html`.
- No reviewed page links forward from `start.html` to a "managed" page (`pricing.html` Growth Ops or a dedicated managed page).

**Fix:** add a `compare.html` link in the lead-score-calculator result block ("قارن خياراتك"), and add a "next step after the sprint → Growth Ops Monthly" link from the `start.html` success state. This closes the funnel end to end.

### F8 — `services.html` line 338 custom-tier price range (LOW)
`services.html` shows a tier at "5,000–25,000 ر.س setup + 1,000/mo". This sits next to `agency_partner_os` (registry price: custom). A visible "5,000–25,000" range on an otherwise registry-faithful page risks reintroducing the fabricated 5,000 figure seen in F3.

**Fix:** confirm whether this is the Agency Partner OS or a separate bespoke tier. If it is the partner offer, replace the visible range with "Custom — contact" to match the registry `price_unit: custom`. If it is a genuine separate bespoke service, add it to the registry first (Article 11), then display it.

---

## 4. Non-negotiable claim check — فحص المحظورات

All reviewed pages were checked against the 11 non-negotiables. Results:

- **No scraping / cold WhatsApp / LinkedIn automation offered as a service** — PASS. `compare.html` explicitly states "NO scraping / NO cold WhatsApp (PDPL-safe)" as a differentiator.
- **No guaranteed sales / ROI as fact** — PASS. `pricing.html` carries a "التزامات لا وعود" (commitments not promises) block and "لا وعود مبيعات". The Data Pack card carries the estimate disclaimer.
- **No autonomous external sending implied** — PASS on reviewed landing pages (`start.html` says "كلّ قرار خارجي بموافقتك"). **NOTE:** the *email/WhatsApp welcome templates* did imply autonomous sending ("AI auto-send للسهل") — this was fixed by M4 in `templates/first_customer_welcome.eml` and `.txt`, not a landing-page issue.
- **No PII, no fake customers** — PASS on reviewed pages.

**No landing HTML required an in-place claim fix.** All HIGH/MEDIUM findings above are pricing/naming/funnel consistency defects, left for the founder to reconcile against the registry per the M4 brief.

KPI commitment language in the registry (offers 2, 3, 4, 5, 6) uses "if not reached, we work for free until reached" / "X free months". This is a **conditional service commitment, not a sales guarantee**, and is acceptable — but the founder should confirm it is operationally honorable before launch, since an unhonored commitment becomes a false claim.

---

## 5. Recommended order of work — ترتيب العمل الموصى به

1. Founder decision: confirm the managed-tier ceiling (2,999 vs 7,500) and whether "Scale OS" / "Starter" / annual discount are real offers. If real, add to the registry first.
2. Rebuild `pricing.html`, `compare.html`, `annual-pricing.html` tiers and tables from `services-catalog.json` (fixes F1–F4).
3. Standardize offer names and the "Sprint" term across all pages (F5, F6).
4. Close the funnel chain links (F7).
5. Resolve the `services.html` custom-tier range (F8).

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
