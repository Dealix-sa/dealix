# Daily 400 Targeting Playbook — دليل التشغيل اليومي

> **EN:** The "400" is a **research pool**, not 400 messages. The daily ritual
> below produces a scored target pool and a tiny set of founder-approved drafts.
> **AR:** الرقم "400" هو **pool بحث وتحليل**، وليس 400 رسالة. الطقس اليومي أدناه
> ينتج قائمة أهداف مُقيّمة ومجموعة صغيرة من المسودات بموافقة المؤسس.

System: [RESEARCH_TARGETING_OS](RESEARCH_TARGETING_OS.md) ·
Engine: [`scripts/research_targeting_os.py`](../../scripts/research_targeting_os.py) ·
Policy: [PROSPECT_RESEARCH_COMPLIANCE_POLICY](../governance/PROSPECT_RESEARCH_COMPLIANCE_POLICY.md)

---

## Daily research loop — الحلقة اليومية

| Time (Riyadh) | Step | Owner |
| --- | --- | --- |
| 08:00 | Run research + collection (seed ± allowlisted discovery) | automation |
| 08:20 | Dedupe + source-policy clean | automation |
| 08:40 | Scoring (100-pt model) | automation |
| 09:00 | `daily_targeting_brief.md` generated | automation |
| 09:15 | Review Top 20 shortlist | founder |
| 09:30 | Pick **5–10 only** | founder |
| 10:00 | Build drafts (review-only) | automation |
| 11:00 | Founder approval | founder |
| after | **Manual send only** (3–5) | founder |

Steps 1–4 + 10 are the script; steps 5, 6, 8 are human judgment. Nothing is sent
automatically at any step.

---

## The funnel — القمع

```
400  raw candidates        (analysis budget — NOT sends)
250–350  clean companies   (after dedupe + source allowlist)
40–80  A/B targets
10–20  founder shortlist (A/A+)
5–10  drafts for review
3–5  manual sends only
```

Strong in research, conservative in contact. Reputation is the moat.

---

## One command — أمر واحد

```bash
python scripts/research_targeting_os.py \
  --seed data/targeting/company_seed_template.csv \
  --out data/targeting/out \
  --top 50
```

Then open:

- `data/targeting/out/daily_targeting_brief.md`
- `data/targeting/out/ranked_targets.csv`
- `data/targeting/out/weakness_map.md`
- `data/targeting/out/drafts_for_review.md`

---

## Filling the seed — تعبئة البذرة

Edit [`data/targeting/company_seed_template.csv`](../../data/targeting/company_seed_template.csv)
with 20–50 companies you know or sectors you want to target. Replace every
`REPLACE:` placeholder row (those are skipped). Key columns:

| Column | Meaning |
| --- | --- |
| `company`, `domain`, `sector`, `city` | Identity + firmographics |
| `source` | Must be on the allowlist (else the row is rejected) |
| `services_count`, `has_case_studies`, `has_contact`, … | Pain/intent signals |
| `expansion_signal`, `hiring_signal`, `launch_signal`, `partnership_signal` | Timing |
| `warm_path` / `relationship` | Access (warm/partner/referral = warm path) |
| `evidence_count`, `evidence_urls` | Evidence confidence (≥2 sources = full) |
| `sensitive_sector`, `data_gap` | Risk penalty inputs |

> Two-evidence rule: a company with `evidence_count < 2` and no warm path cannot
> grade above **B** — the OS routes it to a free Diagnostic, not a Sprint pitch.

---

## Discovery (optional) — التوسّع عبر البحث

With Google Programmable Search keys set:

```bash
export GOOGLE_SEARCH_API_KEY="..."
export GOOGLE_SEARCH_CX="..."
python scripts/research_targeting_os.py \
  --discover --queries-file data/targeting/queries.txt \
  --seed data/targeting/company_seed_template.csv \
  --out data/targeting/out --top 50
```

Discovery reads **public result metadata only** (title/link/snippet). It never
logs in, never bypasses robots.txt, never scrapes page bodies. No keys → seed-only.

Tune queries in [`data/targeting/queries.txt`](../../data/targeting/queries.txt).

---

## What "good" looks like tomorrow — اتجاه الغد

The brief ends with: best sector, best city, best source, most common weakness,
data gaps, and a one-line recommendation. Use it to choose tomorrow's queries and
which second evidence source to gather first.

---

## Forbidden — ممنوع (تذكير)

No scraping behind login · no robots.txt/CAPTCHA bypass · no LinkedIn automation ·
no cold/bulk WhatsApp · no mass email · no auto-send · no claim without evidence ·
no personal phone numbers. See the
[compliance policy](../governance/PROSPECT_RESEARCH_COMPLIANCE_POLICY.md).
