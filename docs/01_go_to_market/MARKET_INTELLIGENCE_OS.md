# Dealix Market Intelligence & Targeting OS

> طبقة: Go-To-Market · الحالة: مُفعّل (offline-first) · يُشغّله: `scripts/research_targeting_os.py`

نظام يومي يعمل كـ **رادار سوق + مصنع قوائم + محلل نقاط ضعف + مولّد درافتات +
بوابة حوكمة**. هدفه ليس إرسال 400 رسالة، بل **الوصول إلى ~400 شركة محتملة كـ
raw research pool**، ثم فلترتها إلى أفضل 40–80 هدفًا، ثم اختيار 10–20 شركة عالية
الجدية، ثم بناء 5–10 درافتات فقط للمراجعة اليدوية.

> القاعدة الكبرى: **نبحث بكثافة، نفلتر بصرامة، نرسل بقلة، ونوثّق كل ادعاء بدليل.**

## القمع اليومي

```
400 raw company candidates
  → 250–350 clean companies
  → 40–80 scored targets
  → 10–20 founder shortlist
  → 5–10 approved outreach drafts
  → 3–5 manual sends only
  → 1–2 diagnostics
  → 1 paid Command Sprint
```

## كيف يخدم طبقات Dealix

| الطبقة | كيف يخدمها |
|---|---|
| Command OS | قرار يومي: من نستهدف؟ ولماذا؟ |
| Revenue OS | يبني pipeline مؤهل |
| Proof OS | يربط كل استهداف بدليل |
| Governance OS | يمنع scraping / spam / overclaim |
| Data OS | ينظف، يدمج، ويحفظ مصادر البيانات |

## المعمارية (Pipeline)

```
Seed Input → Query Factory → Discovery Engine → Compliance Filter
→ Normalizer → Dedupe → Enrichment → Signal Extractor → Scoring Engine
→ Segment Router → Founder Shortlist → Draft Generator → Approval Queue
→ Manual Send Log → Outcome Learning Loop
```

| الطبقة | السكربت |
|---|---|
| Query Factory | [`scripts/targeting_query_factory.py`](../../scripts/targeting_query_factory.py) |
| Normalizer + Dedupe + Enrichment | [`scripts/targeting_enrichment.py`](../../scripts/targeting_enrichment.py) |
| Compliance Filter | [`scripts/targeting_compliance_gate.py`](../../scripts/targeting_compliance_gate.py) |
| Scoring + Routing | [`scripts/targeting_scorecard.py`](../../scripts/targeting_scorecard.py) |
| Draft Generator | [`scripts/targeting_draft_lab.py`](../../scripts/targeting_draft_lab.py) |
| Daily Brief | [`scripts/targeting_daily_brief.py`](../../scripts/targeting_daily_brief.py) |
| Orchestrator | [`scripts/research_targeting_os.py`](../../scripts/research_targeting_os.py) |

## نموذج بيانات الشركة

```json
{
  "company_name": "Example Co",
  "website": "https://example.com",
  "city": "Riyadh",
  "country": "Saudi Arabia",
  "sector": "b2b_consulting",
  "subsector": "Consulting",
  "company_size_signal": "SMB/Mid-market",
  "decision_maker_role": "Founder / GM / Sales Director",
  "source_urls": ["https://example.com/services", "https://example.com/case-studies"],
  "evidence_count": 2,
  "pain_signals": ["generic_services_page", "no_case_studies"],
  "weakness_hypothesis": "Offer and proof clarity gap",
  "recommended_offer": "Command Sprint",
  "targeting_score": 84,
  "grade": "A",
  "risk_flags": [],
  "next_action": "Manual founder review",
  "draft_status": "needs_approval"
}
```

## التشغيل

```bash
# تشغيل القمع كاملًا على ملف seed المؤسس (offline، آمن افتراضيًا)
python scripts/research_targeting_os.py \
  --seed data/targeting/company_seed_template.csv \
  --out data/targeting/out --top 80

# اكتشاف (معطّل افتراضيًا — يحتاج provider مُعتمد + --allow-network)
python scripts/research_targeting_os.py \
  --discover --queries-file data/targeting/queries.txt \
  --out data/targeting/out --top 80
```

المخرجات تحت `--out`: `company_master.jsonl` · `ranked_targets.csv` ·
`daily_targeting_brief.md` · `founder_shortlist.md` · `drafts_for_review.md` ·
`tomorrow_targeting_plan.md`.

## القرار النهائي

> النظام يجمع كثيرًا، ينظف كثيرًا، يرفض كثيرًا، يرتب القليل، يقترح بدقة، يرسل
> يدويًا فقط، ويتعلم من النتائج.

## روابط

- [Targeting Scorecard](TARGETING_SCORECARD.md)
- [Daily Research Loop](DAILY_RESEARCH_LOOP.md)
- [Sector Query Library](SECTOR_QUERY_LIBRARY.md)
- [Outreach Draft Lab](OUTREACH_DRAFT_LAB.md)
- [Founder Shortlist Rules](FOUNDER_SHORTLIST_RULES.md)
- الحوكمة: [Research Source Policy](../03_governance/RESEARCH_SOURCE_POLICY.md) ·
  [Outreach Approval Policy](../03_governance/OUTREACH_APPROVAL_POLICY.md) ·
  [No-Spam Policy](../03_governance/NO_SPAM_POLICY.md) ·
  [Robots & Terms Policy](../03_governance/ROBOTS_AND_TERMS_POLICY.md)
