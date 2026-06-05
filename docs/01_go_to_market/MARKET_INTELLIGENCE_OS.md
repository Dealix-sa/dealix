# Dealix Intelligence-to-Revenue-to-Delivery OS

> نظام الاستخبارات → الإيراد → التسليم
> The company-wide machine: research → target → score → weakness → offer → draft →
> approval → diagnostic → payment → delivery → proof → upsell → learning.

This is **not** a targeting script. It is the daily operating machine of Dealix,
connecting the first moment we look at a company to the last point of renewal and
expansion. It serves every Dealix layer (Command, Market Intelligence, Revenue,
Proof, Delivery, Client, Governance, Finance, Partner, Venture).

---

## 1. The full path

```
Market Discovery
  → Company Intelligence
    → Compliance Filter
      → Scoring Engine
        → Weakness Mapping
          → Offer Routing
            → Draft Lab  (founder approval — never auto-send)
              → Manual Outreach
                → Diagnostic
                  → Proposal → Payment
                    → Delivery Handoff
                      → Proof Pack
                        → Upsell / Renewal
                          → Learning Loop  ⟲ feeds tomorrow's targeting
```

Every company that enters the system exits with exactly **one of three verdicts**:

1. **Target now** — scored A/A+, routed, drafted, queued for the founder.
2. **Nurture later** — scored B/C, needs more evidence or timing.
3. **Reject (with a reason)** — fails compliance or scores D.

Every company that **pays** exits delivery with: **Delivery Pack + Proof Pack +
Upsell Decision**.

---

## 2. The pipeline scripts

| Stage | Script | Output |
|-------|--------|--------|
| Query factory | `scripts/targeting_query_factory.py` | `out/research_queries.md` (run by hand) |
| Discovery | `scripts/targeting_discovery.py` | `out/raw_candidates.jsonl` |
| Normalize / dedupe | `scripts/targeting_normalizer.py` | `data/targeting/company_master.jsonl` |
| Compliance gate | `scripts/targeting_compliance_gate.py` | `out/approved_research_pool.csv`, `out/rejected_targets.csv` |
| Scoring | `scripts/targeting_scorecard.py` | `out/ranked_targets.csv` |
| Weakness mapping | `scripts/targeting_weakness_mapper.py` | (in-memory) |
| Offer routing | `scripts/targeting_offer_router.py` | (in-memory) |
| Draft Lab | `scripts/targeting_draft_lab.py` | `out/drafts_for_review.md` |
| Daily brief | `scripts/targeting_daily_brief.py` | `out/founder_shortlist.md`, `out/daily_targeting_brief.md`, `out/tomorrow_targeting_plan.md` |
| Delivery handoff | `scripts/targeting_delivery_handoff.py` | `customers/{slug}/…` |
| Learning loop | `scripts/targeting_learning_loop.py` | `out/weekly_targeting_retrospective.md` |

All scripts are **offline, deterministic, stdlib + PyYAML** — no network, no LLM,
no scraping — so every output is reviewable and reproducible.

---

## 3. Daily volume targets

| Metric | Target |
|--------|--------|
| Raw candidates researched | 300–400 |
| Clean companies after dedupe | 250–350 |
| Scored companies | ~80 |
| Founder shortlist (review today) | ~20 |
| Drafts for review | ~10 |
| Manual sends | 3–5 |
| Diagnostics | ~2 |
| Offers | ~1 |
| Paid sprints (over time) | 0.2–0.5/day |

> **400 researched, not 400 sent.** Dealix is strong on intelligence, strict on
> filtering, precise in messaging, and respectful in channels.

---

## 4. The daily company rhythm

| Time | Step |
|------|------|
| 08:00 | Research run → 400 raw candidates, normalize + dedupe |
| 08:30 | Scoring → ~80 ranked companies |
| 09:00 | Founder Brief → top 20, best sector, best angle, biggest risk |
| 09:30 | Draft review → 10 drafts |
| 10:00 | Manual outreach → 3–5 messages (manual send only) |
| 13:00 | Diagnostics → handle replies, book calls |
| 17:00 | Delivery / Proof → ship to current customers, update proof |
| 18:00 | Learning log → what worked, what to stop, tomorrow's targets |

---

## 5. Run it

```bash
# One-shot daily brief (compliance → score → weakness → offer → drafts)
python scripts/targeting_daily_brief.py \
  --in data/targeting/company_master.jsonl --out data/targeting/out

# After a company pays:
python scripts/targeting_delivery_handoff.py --company "Company Name"

# Weekly:
python scripts/targeting_learning_loop.py --out data/targeting/out
```

---

## 6. Hard rules (non-negotiables)

- No messages sent automatically.
- No scraping behind login; respect `robots.txt` and source terms.
- No personal phone numbers; no cold WhatsApp automation.
- No claims without evidence; every target carries evidence.
- Every draft requires founder approval.
- Every paid target creates a delivery handoff.
- Every delivery produces a proof pack.

See `docs/03_governance/` for the enforceable policies.

---

## 7. Related docs

- [DAILY_400_RESEARCH_LOOP.md](DAILY_400_RESEARCH_LOOP.md)
- [TARGETING_SCORECARD.md](TARGETING_SCORECARD.md)
- [WEAKNESS_MAPPING_SYSTEM.md](WEAKNESS_MAPPING_SYSTEM.md)
- [OFFER_ROUTING_SYSTEM.md](OFFER_ROUTING_SYSTEM.md)
- [OUTREACH_DRAFT_LAB.md](OUTREACH_DRAFT_LAB.md)
- [FOUNDER_SHORTLIST_RULES.md](FOUNDER_SHORTLIST_RULES.md)
- [TARGETING_TO_DELIVERY_HANDOFF.md](TARGETING_TO_DELIVERY_HANDOFF.md)
- [WEEKLY_TARGETING_RETROSPECTIVE.md](WEEKLY_TARGETING_RETROSPECTIVE.md)
