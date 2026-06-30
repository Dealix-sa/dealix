# Dealix Research & Targeting OS — نظام الاستخبارات والاستهداف اليومي

> **EN:** A repeatable, governed daily loop that turns seeds + allowlisted research
> into a scored, evidence-backed **target pool** — not an outbound blaster. Quality
> over volume. No external send without founder approval.
>
> **AR:** نظام يومي قابل للتكرار وخاضع للحوكمة، يحوّل البذور + البحث المسموح إلى
> **قائمة أهداف مُقيّمة ومدعومة بالأدلة** — وليس آلة إرسال جماعي. الجودة قبل الحجم.
> لا إرسال خارجي بدون موافقة المؤسس.

Engine: [`scripts/research_targeting_os.py`](../../scripts/research_targeting_os.py) ·
Tests: [`tests/test_research_targeting_os.py`](../../tests/test_research_targeting_os.py) ·
Policy: [PROSPECT_RESEARCH_COMPLIANCE_POLICY](../governance/PROSPECT_RESEARCH_COMPLIANCE_POLICY.md) ·
Playbook: [DAILY_400_TARGETING_PLAYBOOK](DAILY_400_TARGETING_PLAYBOOK.md)

---

## 1. What it does — ماذا يفعل

The daily loop, in order:

1. **Collect** companies from seeds + (optional) allowlisted discovery + open data.
2. **Normalize** names and domains (AR/EN aware).
3. **De-duplicate** by domain identity, falling back to normalized name; merge evidence.
4. **Attach evidence** per company (allowlisted sources only).
5. **Score** each company on a 100-point firmographic / targeting model.
6. **Infer the weakness** most likely present, and the Dealix OS that addresses it.
7. **Recommend an offer** rung: Command Sprint / Diagnostic / Nurture.
8. Emit a **raw pool** (up to 400/day — an *analysis* budget, not a send count).
9. Narrow to **40–80 A/B targets**.
10. Surface a **10–20 founder shortlist**.
11. Build **5–10 review-only drafts** — never auto-sent.

> The number 400 is a **research and analysis** pool, not 400 messages.

---

## 2. The scoring model — نظام السكور (100 نقطة)

| Axis | Points | Meaning |
| --- | --- | --- |
| ICP Fit | 35 | هل الشركة مناسبة لـ Dealix؟ (sector + identity + research surface) |
| Pain Signal | 25 | هل يظهر ألم متابعة / عروض / تسليم / إثبات؟ |
| Intent / Timing | 20 | توسع، توظيف، إطلاق، شراكات، نشاط |
| Access | 10 | قناة وصول نظيفة أو warm path |
| Evidence Confidence | 10 | كم مصدر مسموح يدعم القرار (≥2 = كامل) |
| Risk Penalty | −20 | مصدر ضعيف، قطاع حساس، بيانات ناقصة، مخاطرة امتثال |

Grades — التقييم:

| Grade | Action | المعنى |
| --- | --- | --- |
| A+ | `engage_today` | تراجع اليوم |
| A | `strong_target` | هدف قوي |
| B | `research_more` | يحتاج بحث إضافي |
| C | `nurture` | رعاية |
| D | `do_not_target_now` | لا يُستهدف الآن |

### The golden rule — القاعدة الذهبية

> **EN:** Never target a company unless you have **either** two clear pain evidences
> **or** a warm path. Otherwise: *research more*.
>
> **AR:** لا تستهدف شركة إلا إذا توفّر **أحد** أمرين: دليلان واضحان على الألم، **أو**
> علاقة دافئة / warm path. غير ذلك: ابحث أكثر.

Enforced in code: a not-ready candidate **cannot grade above B**
(`evaluate()` caps the grade and routes the offer to a free Diagnostic).

---

## 3. Weakness → Dealix OS mapping — خريطة الضعف

| Signal | Likely weakness | Dealix OS |
| --- | --- | --- |
| Many services, no visible case studies | Proof weakness | **Proof OS** |
| Contact/WhatsApp but no funnel | Follow-up leakage | **Revenue OS** |
| Projects / implementation work | Delivery visibility | **Delivery OS** |
| Recurring support / customer load | Support recurrence | **Support OS** |
| Expansion + hiring activity | Executive decision fog | **Command OS** |
| Scattered / ungoverned data | Data fragmentation | **Data OS** |

Each becomes a **manual, evidence-anchored draft** for review — never a claim.

---

## 4. Outputs — المخرجات

Written under `--out` (default `data/targeting/out/`):

| File | Contents |
| --- | --- |
| `ranked_targets.csv` | Every evaluated company, full score breakdown. |
| `ranked_targets.jsonl` | Same, machine-readable, with `score_breakdown`. |
| `daily_targeting_brief.md` | Funnel + founder shortlist + tomorrow's direction. |
| `drafts_for_review.md` | 5–10 review-only drafts (AR+EN), evidence attached. |
| `weakness_map.md` | Companies grouped by weakness → Dealix OS. |

Ideal day — مخرجات اليوم المثالية:

```
400 raw candidates        → analysis pool
250–350 clean companies   → after dedupe + source policy
40–80 A/B targets
10–20 founder shortlist
5–10 drafts for review
3–5 manual sends only     → founder decides
```

Strong in research, conservative in contact. This protects reputation and raises quality.

---

## 5. How to run — كيف تشغّله

Seed-only (the safe default):

```bash
python scripts/research_targeting_os.py \
  --seed data/targeting/company_seed_template.csv \
  --out data/targeting/out \
  --top 50
```

Allowlisted discovery (needs Google Programmable Search keys):

```bash
export GOOGLE_SEARCH_API_KEY="..."
export GOOGLE_SEARCH_CX="..."
python scripts/research_targeting_os.py \
  --discover \
  --queries-file data/targeting/queries.txt \
  --seed data/targeting/company_seed_template.csv \
  --out data/targeting/out \
  --top 50
```

> Google Custom Search JSON API needs a Programmable Search Engine + API key and
> returns JSON (≈100 free queries/day). If your keys work, the OS uses them; if
> not, it runs **seed-only** and degrades gracefully. The provider can later be
> swapped (Vertex AI Search / SerpAPI / Tavily / Brave) without changing the engine.

Daily automation: [`.github/workflows/daily-targeting-os.yml`](../../.github/workflows/daily-targeting-os.yml)
(05:00 UTC = 08:00 Riyadh; uploads artifacts; never sends).

---

## 6. Governance — الحوكمة (non-negotiable)

The engine reuses the canonical doctrine guard
[`auto_client_acquisition.safe_send_gateway`](../../auto_client_acquisition/safe_send_gateway/doctrine.py)
and the claim-safety auditor
[`auto_client_acquisition.governance_os.claim_safety`](../../auto_client_acquisition/governance_os/claim_safety.py).

Forbidden — ممنوع:

- No scraping behind login · no robots.txt bypass · no CAPTCHA bypass.
- No LinkedIn automation · no cold/bulk WhatsApp · no mass email.
- No autonomous external sends — **drafts only**, founder approves.
- No personal phone numbers · no claim without evidence.

Allowed sources are pinned in
[`data/targeting/source_allowlist.json`](../../data/targeting/source_allowlist.json)
(blocked sources are hard-rejected and logged). Full policy:
[PROSPECT_RESEARCH_COMPLIANCE_POLICY](../governance/PROSPECT_RESEARCH_COMPLIANCE_POLICY.md).

---

## 7. Tomorrow's targeting direction — اتجاه الغد

At the end of each run the brief reports: best sector, best city, best source, most
common weakness, data gaps, and a one-line recommendation for where to deepen
tomorrow — e.g.:

> Deepen targeting around B2B consulting in Riyadh (highest average score). Add a
> second evidence source from company websites, contact, and case-study pages
> before drafting.

This turns Dealix from "searching for companies" into a **repeatable, measurable
daily Targeting OS**.
