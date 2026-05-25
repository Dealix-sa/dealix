# Hermes — Governed AI Execution Control Plane

Hermes is the Dealix control plane that turns AI execution into a board-grade,
auditable, founder-sovereign operating system. It does not replace Dealix's
`governance/`, `trust/`, or `marketing_factory/` modules; it sits beside them
and adds the cryptographic, situational, and revenue-quality layers required
for Company-Grade and Enterprise-Grade positioning (sections 131–165).

## The Four Promises

1. **Governed AI Execution** — every workflow is signed (`authenticated_workflows/`)
   and every action passes the Pre-Action Governance Reasoning Loop
   (`governance_reasoning/pre_action_loop.py`) layered across global, workspace,
   workflow, agent, and situational rules. Forbidden actions are blocked,
   high-risk actions are escalated, never auto-executed.
2. **Verified Revenue** — `growth/revenue/verified_revenue.py` rejects every
   record lacking an `evidence_pack_id`. Vanity metrics cannot enter the
   ledger; attribution (`growth/attribution/`) inherits the same rule.
3. **Outcome-to-Asset Compounding** — message variants
   (`growth/message_testing.py`), citation assets (`growth/geo/citation_assets.py`),
   and partner claims (`partners/program/approved_claims.py`) all bind to an
   evidence pack so winning outcomes become reusable, signed assets.
4. **Sovereign Control** — `governance_reasoning/situational_rules.py` forces
   escalation whenever sensitivity >= 3. `sovereignty/founder_leverage.py`
   keeps the founder's time leverage measurable. Outreach
   (`growth/direct_outreach.py`) and co-marketing
   (`partners/program/co_marketing.py`) are always drafts that require
   explicit human approval; nothing crosses the network from Hermes.

## Module Tree

```
dealix/hermes/
  authenticated_workflows/   intent + context + tool + data attestations
  governance_reasoning/      PAGRL + escalation ledger
  agent_comms/               delegation, sanitization, provenance, trust, audit
  growth/
    market_signals.py        ingest deal won/lost/demo/churn signals
    icp_registry.py          ICP CRUD + account scoring
    offer_market_fit.py      offer x ICP fit scoring
    campaign_registry.py     draft campaigns linked to offers
    message_testing.py       A/B variants with verified-revenue outcomes
    direct_outreach.py       draft-only outreach queue
    abm_engine.py            account tier matrix
    geo/                     AI visibility, entity consistency, answer pages,
                             citation assets, trust signals, search monitor
    attribution/             channel, campaign, message, asset, agent,
                             partner, geo (every record requires evidence)
    revenue/                 verified revenue, revenue quality,
                             pipeline quality, funnel conversion
  board/                     KPI metrics, investor update, traction, memo,
                             revenue-quality and trust summaries
  sovereignty/founder_leverage.py
  partners/program/          approved claims, tiers, enablement,
                             co-marketing drafts, revenue share,
                             compliance, performance reviews
  ai_visibility_product/     query, mention, citation, trust score,
                             recommendations, revenue linking
```

## Doctrine Anchors

- No external sends: every `outreach` / `publish` / `notify` returns a draft
  with `status="draft"` and `requires_approval=True`. Tests assert no socket
  connection is attempted.
- No vanity metrics: any revenue/attribution write without an
  `evidence_pack_id` raises `ValueError`.
- Founder sovereignty: PAGRL routes `sensitivity >= 3` actions to the
  escalation ledger and returns a pending `approval_id`.
- Delegation rule: `agent_comms/delegation_policy.can_delegate(agent, action)`
  returns `False` if the action is outside the agent's declared capabilities.

## Storage

Hermes uses append-only JSONL ledgers under `data/hermes/` with per-ledger
environment overrides:

- `DEALIX_HERMES_ESCALATION_PATH`
- `DEALIX_HERMES_AGENT_AUDIT_PATH`
- `DEALIX_HERMES_OUTREACH_PATH`
- `DEALIX_HERMES_VERIFIED_REVENUE_PATH`
- `DEALIX_HERMES_SECRET` (HMAC secret for intent/claim signing)

## Tests

Hermes tests live at `tests/hermes/` mirroring the module tree. Run with:

```
pytest tests/hermes/ -x -q --confcutdir=tests/hermes -o addopts=
```

The `--confcutdir` flag isolates Hermes tests from the heavy parent
`conftest.py` (which pulls in pydantic, sqlalchemy, httpx etc.); the
`-o addopts=` clears the repository-level coverage flags.
