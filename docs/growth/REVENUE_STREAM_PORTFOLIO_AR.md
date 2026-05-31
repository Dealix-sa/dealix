# Revenue Stream Portfolio — محفظة مصادر الإيراد

> Sections 44–45. RevenueStreamCard، 7 قرارات، 5 buckets / 25+ stream، و3 funnels نموذجيّة.
> Module path: `dealix/growth_os/streams/`

---

## مقدّمة — Introduction

محفظة الإيراد ليست قائمة عروض. هي مصفوفة قرارات. كل stream له بطاقة، حالة، قرار شهري، ومسار توسعة أو إيقاف.

The revenue portfolio is not a product list. It is a decision matrix — each stream has a card, status, monthly decision, and an expansion or shutdown path.

---

## RevenueStreamCard Schema

```json
{
  "stream_id": "STR-GOV-SNAP-001",
  "name_ar": "Governance Snapshot",
  "name_en": "Governance Snapshot",
  "bucket": "fast",
  "icp_primary": "agencies",
  "offer_id": "OFF-GOV-SNAP-001",
  "price_band_sar": {"min": 5000, "max": 12000},
  "delivery_window_days": 14,
  "revenue_type": "one_off",
  "margin_band_pct": {"min": 60, "max": 80},
  "deals_last_90_days": "<TBD: founder fill>",
  "revenue_last_90_days_sar": "<TBD>",
  "quality_score_avg": "<TBD>",
  "decision_this_month": "scale",
  "decision_reason": "Conversion rate stable, margin healthy.",
  "decision_history": [
    {"month": "2026-04", "decision": "optimize"},
    {"month": "2026-03", "decision": "scale"}
  ],
  "expansion_path": "Snapshot → Pilot → Quarterly Retainer",
  "owner": "founder",
  "disclosures": ["All figures are estimated until reconciled."]
}
```

---

## القرارات السبعة — 7 Stream Decisions

| Decision | متى | الإجراء |
|---|---|---|
| `scale` | conversion + margin + quality صحيّة | زِد investment + capacity |
| `optimize` | margin أو conversion يتذبذب | اختبر متغيّر واحد (price / message / channel) |
| `reprice` | margin منخفض رغم demand | ارفع السعر تجريبياً |
| `bundle` | عرض ضعيف منفرد، قويّ مع غيره | اضمم لـ bundle موثَّق |
| `partner_led` | تسليم Dealix محدود، الطلب يفوق | حوّل لـ white-label |
| `pause` | إشارات مختلطة، نحتاج بيانات | أوقف الترويج 30 يوم، استمر بالتسليم |
| `kill` | margin < 40% أو يخالف Constitution | إيقاف نهائي + توثيق السبب |

---

## المحفظة الكاملة — Full Portfolio (5 Buckets / 25+ Streams)

### Bucket 1 — Fast (7–21 يوم)

| # | Stream | ICP | Price Band SAR | Decision |
|---|---|---|---|---|
| 1 | Governance Snapshot | Agencies, AI users | 5K–12K | scale |
| 2 | Claim-Safety Audit (Mini) | Agencies | 3K–6K | optimize |
| 3 | AI Offer Diagnostic | Founders | 2K–5K | scale |
| 4 | PDPL Quick Map | SMB | 4K–8K | optimize |
| 5 | Proposal Rescue (single proposal review) | Consultants | 1K–3K | bundle |

### Bucket 2 — Monthly (Retainer)

| # | Stream | ICP | Price Band SAR/mo | Decision |
|---|---|---|---|---|
| 6 | Governance Retainer | Agencies, SMB | 6K–15K | scale |
| 7 | Revenue Intelligence Retainer | SMB | 8K–20K | scale |
| 8 | Founder Advisory Retainer | Founders | 4K–10K | optimize |
| 9 | Claim Ledger Retainer | AI users | 5K–12K | scale |
| 10 | Content-to-Revenue Retainer | Agencies | 7K–18K | optimize |

### Bucket 3 — Partner (White-label / Referral)

| # | Stream | Partner Type | Commission | Decision |
|---|---|---|---|---|
| 11 | White-label Governance Snapshot | Agencies | `<TBD>`% | scale |
| 12 | White-label Claim-Safety Audit | Agencies | `<TBD>`% | optimize |
| 13 | Consultant Toolkit License | Independent Consultants | revenue share | pause |
| 14 | Training Partner Co-brand | Training providers | flat + per-seat | optimize |
| 15 | Referral-only Partner Tier | Boutique consultants | finder's fee | scale |

### Bucket 4 — Enterprise

| # | Stream | ICP | Price Band SAR | Decision |
|---|---|---|---|---|
| 16 | Enterprise AI Operating Layer Pilot | Enterprise | 80K–250K | optimize |
| 17 | Annual Platform License | Enterprise | 250K–800K | scale |
| 18 | Enterprise AI Audit (Quarterly) | Enterprise | 40K–120K | optimize |
| 19 | Board Briefing Pack | Enterprise C-suite | 25K–60K | scale |
| 20 | Custom Governance Build | Enterprise | project-based | bundle |

### Bucket 5 — Platform (Self-serve / Productized)

| # | Stream | ICP | Price Band SAR | Decision |
|---|---|---|---|---|
| 21 | Dealix Academy License (Single seat) | Individuals | 600–1,500 | scale |
| 22 | Dealix Academy License (Team) | SMB | 8K–25K | scale |
| 23 | ProofPack Template Library | Agencies, Consultants | 1K–4K | optimize |
| 24 | Signal Radar Subscription | Marketers, Founders | 200–800/mo | pause |
| 25 | Hermes Sandbox Access | Founders, Developers | freemium → tiered | optimize |
| 26 | Quarterly Sector Report Sub | All ICPs | 1K–3K/yr | scale |

> الأرقام أعلاه نطاقات تقديريّة. القيم الفعليّة في `OfferCard` المعتمد.

---

## ثلاث Funnels نموذجيّة — Section 45

### Funnel A — Revenue Hunter (B2B SMB)

| Stage | Asset | Conversion Target |
|---|---|---|
| Awareness | GEO page `/revenue-intelligence-saudi-smb` | visit → meeting_request |
| Consideration | Sector Report download | download → meeting |
| Decision | Revenue Intelligence Sprint proposal | meeting → signature ≥ 30% |
| Expansion | Monthly Retainer (Bucket 2 #7) | sprint → retainer ≥ 40% |

### Funnel B — AI Trust Kit (AI Users / Agencies)

| Stage | Asset | Conversion Target |
|---|---|---|
| Awareness | Trust Pack page (`docs/14_trust_os/`) | visit → trust_kit_download |
| Consideration | Claim-Safety Audit Mini | download → mini_audit_purchase |
| Decision | Governance Snapshot | mini → snapshot ≥ 35% |
| Expansion | Governance Retainer | snapshot → retainer ≥ 50% |

### Funnel C — Agency White-label

| Stage | Asset | Conversion Target |
|---|---|---|
| Awareness | Partner page + Partner Content | visit → application |
| Consideration | Partner onboarding call | application → onboarding ≥ 60% |
| Decision | First white-label deal (with Dealix delivery support) | onboarded → first deal ≤ 45 يوم |
| Expansion | 3+ deals → Tier upgrade | first → 3rd deal ≤ 120 يوم |

---

## مراجعة المحفظة الشهريّة — Monthly Portfolio Review

كل شهر، كل stream يأخذ قرار من السبعة. التغيير ≥ scale/optimize/kill يحتاج evidence من `ExperimentCard` أو `RevenueRecord` aggregate.

---

## How to verify

```bash
bash scripts/growth_os_master_verify.sh
```

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
