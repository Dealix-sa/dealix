# Daily 400 Research Loop

> الهدف: 400 بحث يوميًا — وليس 400 إرسال.

The research loop is the top of the funnel. It is **human-driven collection** from
allowed public sources, consolidated and cleaned by scripts. Dealix never scrapes
or auto-searches.

---

## Phase A — Market Discovery

**Goal:** assemble the market from every *allowed* angle.

**Allowed sources**

- Official company websites (home, services, clients, case-study, careers pages).
- Company news / press.
- Public directories and chambers of commerce.
- Events and exhibitions.
- Lists you enter by hand.
- Google Search API (or equivalent) for *finding public pages* — not scraping.
- Open Data.
- LinkedIn results **viewed manually only** — no automation, no Sales Navigator.

**Not allowed** (see `docs/03_governance/RESEARCH_SOURCE_POLICY.md`)

- Anything behind a login.
- Scraping that ignores `robots.txt` or source terms.
- CAPTCHA bypass.
- Personal phone numbers / leaked datasets / purchased personal lists.

**Output:** `raw_candidates.jsonl` (≈400 rows).

```bash
python scripts/targeting_query_factory.py --per-sector 6   # → out/research_queries.md (run by hand)
python scripts/targeting_discovery.py --seeds data/targeting/company_seed_template.csv \
  --out data/targeting/out/raw_candidates.jsonl
```

---

## Phase B — Company Intelligence

Each company turns from a *name* into an *intelligence profile* with these fields:

```
company_name, website, city, sector, subsector, b2b,
services, contact_channel, proof_visibility, case_study_presence,
growth_signal, hiring_signal, partnership_signal, technology_signal,
decision_maker_likely_role, source_urls, evidence_count
+ pain signals (weak_cta, no_case_studies, fragmented_tools, …)
```

Field definitions live in `data/targeting/signals.yml`.

---

## Phase C — Normalize + dedupe

```bash
python scripts/targeting_normalizer.py \
  --in data/targeting/out/raw_candidates.jsonl \
  --out data/targeting/company_master.jsonl
```

- Coerces field types (CSV strings → bool/list/int).
- Dedupes by website host, else by lowercased name.
- ~400 raw → ~250–350 clean.

---

## Phase D — Compliance + scoring

The normalized master feeds the compliance gate, then the scorecard, then the
daily brief. See [TARGETING_SCORECARD.md](TARGETING_SCORECARD.md).

```bash
python scripts/targeting_daily_brief.py \
  --in data/targeting/company_master.jsonl --out data/targeting/out
```

---

## Acceptance (research)

- [ ] Can produce 300–400 raw candidates/day.
- [ ] Can dedupe cleanly.
- [ ] Rejects non-compliant sources with a reason.
- [ ] Every clean company has `≥ minimum_evidence_count` sources.
