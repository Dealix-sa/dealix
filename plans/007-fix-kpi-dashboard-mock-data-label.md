# 007 — Fix kpi_dashboard.py's misleading "mock data" docstring

- **Finding:** `api/routers/kpi_dashboard.py:181` docstring claims "Uses
  realistic mock data when the live DB is unavailable" (implying a DB-backed
  path exists with a fallback), but `kpi_summary()` (lines 176-224) has
  **no DB call anywhere in the function** — every field (`leads_total.value:
  84`, `conversion_rate.value_pct: 18.4`, `churn_rate.value_pct: 3.2`,
  `arpa.value_sar: 2_200`, lines 202-217) is a literal hardcoded constant.
  The "fallback" framing is false: there is no live path, only the mock.
  If this endpoint is ever surfaced to a prospect during a sales demo or a
  technical buyer's due diligence, the fixed numbers (which look like real
  business metrics — MRR, conversion rate, churn) would be discovered as
  fake, directly undermining the "No fake data" non-negotiable in spirit,
  even though this is sample/demo UI rather than an external claim.
- **Category:** correctness / doctrine
- **Wave:** maintenance
- **Effort:** S   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read api/routers/kpi_dashboard.py before editing
```

## Context (inlined)
- File in scope: `api/routers/kpi_dashboard.py`
- Current state (`api/routers/kpi_dashboard.py:176-224`):
    ```python
    @router.get("/summary")
    async def kpi_summary() -> dict[str, Any]:
        """Overall company KPIs: MRR, ARR, leads, conversion rates.

        Returns bilingual labels and a governance_decision field.
        Uses realistic mock data when the live DB is unavailable.
        """
        history = _mock_mrr_history(12)
        current = history[-1]
        previous = history[-2]
        mrr_growth_pct = round((current["mrr_sar"] - previous["mrr_sar"]) / previous["mrr_sar"] * 100, 1)

        return {
            "governance_decision": _GOV,
            "generated_at": _NOW.isoformat(),
            "metrics": {
                "mrr": {...},
                "arr": {...},
                "leads_total": {"value": 84, "qualified": 31, "label": _label("leads_total")},
                "conversion_rate": {"value_pct": 18.4, "label": _label("conversion_rate")},
                "churn_rate": {"value_pct": 3.2, "label": _label("churn_rate")},
                "arpa": {"value_sar": 2_200, "label": _label("arpa")},
                "customer_count": {"active": 12, "churned_ytd": 2},
            },
            "mrr_history": history[-6:],
        }
    ```
- This is a docs/labeling fix, not a request to build a real DB-backed KPI
  pipeline (that's a much larger effort and out of scope here).

## Steps
1. Fix the docstring to state the actual behavior — this endpoint is always
   sample/demo data, not a fallback:
    ```python
    """Overall company KPIs: MRR, ARR, leads, conversion rates.

    Returns bilingual labels and a governance_decision field.
    DEMO DATA ONLY — every value below is a fixed illustrative sample for
    UI development and sales demos. There is no live DB-backed path yet;
    do not present this endpoint's output as real company metrics.
    """
    ```
   **Gate:** `grep -n "DEMO DATA ONLY" api/routers/kpi_dashboard.py` → prints the new line.
2. Add an explicit `"data_source": "demo_sample"` field to the returned
   dict (top level, alongside `governance_decision`) so any consumer
   (frontend, API client, sales demo script) can programmatically detect
   this is not live data.
   **Gate:** `python3 -c "import asyncio; from api.routers.kpi_dashboard import kpi_summary; print(asyncio.run(kpi_summary())['data_source'])"` → prints `demo_sample`.
3. Search for any other router with the same "mock data when unavailable"
   docstring pattern that has zero DB calls (same false-fallback framing),
   and apply the same fix if found:
   `grep -rln "mock data when" api/routers/`
   **Gate:** for each match, confirm no `AsyncSession|get_db|select(` usage exists in the file before relabeling; leave alone any file that does have a real DB path.

## Done criteria (machine-checkable)
- [ ] `grep -n "DEMO DATA ONLY" api/routers/kpi_dashboard.py` → 1 match
- [ ] `python3 -m compileall -q api` → exit 0
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not implement a real DB-backed KPI pipeline in this plan — that's a
  separate, much larger feature (a future Wave item, not a doc/label fix).
- Do not change `_mock_mrr_history()`'s actual numbers.
- Do not touch any router that already has a real `AsyncSession`/`select()`
  path with a genuine fallback — only relabel routers with zero DB code.

## STOP conditions
- If `kpi_summary()` no longer matches the excerpt above (e.g. a DB path
  was added since) → STOP, re-run drift check; the false-fallback framing
  may no longer apply.
- If the frontend (`apps/web`) hard-depends on the exact response shape and
  adding `data_source` breaks a strict schema check → STOP, report instead
  of removing the field from other consumers.
