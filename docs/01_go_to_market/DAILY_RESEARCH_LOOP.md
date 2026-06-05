# Daily Research Loop — الحلقة اليومية للبحث

> يُشغّلها: [`scripts/research_targeting_os.py`](../../scripts/research_targeting_os.py) ·
> جدولة: [`.github/workflows/daily-targeting-os.yml`](../../.github/workflows/daily-targeting-os.yml)

## الإيقاع اليومي

1. **Query Factory** يبني queries من `sectors.yml × cities.yml` + `queries.txt`.
2. **Discovery / Seed** يجمع المرشحين (الاكتشاف معطّل افتراضيًا؛ seed المؤسس يكفي).
3. **Normalizer + Dedupe** يوحّد الدومين/القطاع ويحذف التكرار.
4. **Compliance Gate** يرفض المصادر الممنوعة ويعلّم ما يحتاج مراجعة.
5. **Scoring + Routing** يعطي كل شركة score/grade وعرض Dealix المناسب.
6. **Founder Shortlist** يختار A/A+ المعتمدة فقط.
7. **Draft Generator** يبني درافتات `needs_approval` نظيفة فقط.
8. **Daily Brief + Tomorrow Plan** يلخّص ويوجّه الغد.

## KPIs اليومية

| KPI | الهدف |
|---|---|
| Raw candidates | 300–400 |
| Clean companies | 200+ |
| A/B targets | 40+ |
| Founder shortlist | 10–20 |
| Drafts | 5–10 |
| Manual sends | 3–5 |

## KPIs أسبوعية

| KPI | الهدف |
|---|---|
| Manual sends | 20–25 |
| Replies | 5–8 |
| Diagnostics | 2–4 |
| Paid sprint offers | 1–2 |
| Paid sprint closed | 0.5–1 |
| Learning insights | 5 |

## منهج المراحل (Rollout)

| المرحلة | المدة | القطاعات |
|---|---|---|
| 1 | أسبوعان | b2b consulting · training · marketing agencies · software/IT |
| 2 | بعد أول ردود | recruitment · accounting/advisory · facility mgmt · logistics |
| 3 | بعد proof | mid-market services · partner channels · enterprise pilots |

تُضبط المراحل عبر حقل `phase` في `sectors.yml` و`cities.yml`، ويُمرّر `--phase`.

## Learning Loop

كل إرسال يدوي يُسجَّل (target, score, draft_sent, reply, call_booked, reason,
next_adjustment). بعد أسبوع يلخّص النظام: أفضل قطاع للردود، أفضل angle، أضعف
angle، أفضل/أسوأ CTA — لضبط الاستهداف القادم.

## روابط

- [Market Intelligence OS](MARKET_INTELLIGENCE_OS.md)
- [Sector Query Library](SECTOR_QUERY_LIBRARY.md)
