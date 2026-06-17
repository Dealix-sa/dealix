# Competitive Intelligence Machine

## Doctrine Anchor
- Non-negotiables touched: #2 (no value claim without evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: control-plane verification scripts as release blockers.

## Purpose

Track competitors, alternatives, pricing, positioning, and market signals — and convert that intelligence into better sales conversations, sharper objection handling, and faster product decisions. Intelligence without sales-conversation impact is overhead.

## Tracks

| Track | What we monitor |
|-------|-----------------|
| CRM tools | Local and global, positioning vs Dealix |
| Sales automation tools | Where they overclaim, where they undeliver |
| Lead generation agencies | Their pricing, their proof, their churn signals |
| AI agent platforms | Their feature claims and limits |
| Local Saudi consultants | Reputation, sector coverage, referral relationships |
| ERP / CRM implementers | Partnership candidates and competitive overlap |
| Marketing agencies | Where they hand off and where they could partner |

## Outputs

Each track produces:

- **Positioning updates** — how Dealix should describe itself relative to the alternative.
- **Objection handling** — specific buyer objections this competitor seeds, and the answer.
- **Pricing comparison** — public price points; never claimed without a source link.
- **Feature gaps** — what they have that we do not, and vice versa.
- **Partnership opportunities** — where the overlap is actually complementary.

## Core Rules

- Competitive intelligence is for Dealix's sales conversations. It is not a public attack channel.
- We do not publish disparaging claims about competitors.
- Every public statement Dealix makes about a competitor or alternative carries a source link.
- Pricing claims about competitors are quoted from public price pages or RFP documents, never inferred.
- Intelligence that is not source-evidence-linked stays internal and is treated as hypothesis.

## Operating Cadence

| Cadence | What happens |
|---------|--------------|
| Weekly | Sales conversation review: which objections came up, did we have an answer |
| Monthly | Competitive landscape update: positioning, pricing, feature gaps |
| Quarterly | Strategic review: kill, mirror, leapfrog, or partner per competitor |

## Runtime Wiring

- Existing competitive positioning: `docs/COMPETITIVE_POSITIONING.md`.
- Existing competitive strategy: `docs/moat/COMPETITIVE_STRATEGY.md`.
- Existing intelligence cluster: `docs/intelligence/` (22 files).
- Audit log (records when competitive intel was used in a proposal or outreach): `db/models.py::AuditLogRecord`.
- Autonomous growth competitor monitor agent: `autonomous_growth/agents/` (competitor monitor referenced).

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Sales objections we had a sourced answer for | trending up | conversation log |
| Public competitive claims without a source link | 0 | review |
| Positioning updates shipped per quarter | tracked | release notes |
| Partnerships sourced from competitive intel | tracked | partner ledger |

## Cross-Links

- `docs/COMPETITIVE_POSITIONING.md`
- `docs/moat/COMPETITIVE_STRATEGY.md`
- `docs/intelligence/` (existing cluster)
- `docs/distribution/DEALIX_DISTRIBUTION_OS.md`
- `docs/distribution/ABM_STRATEGIC_ACCOUNT_MACHINE.md`
- `docs/partners/PARTNER_REVENUE_MACHINE.md`
- `docs/sales/` (existing objection-handling docs)

## Open Items

- A "sales objections to sourced answers" registry does not yet exist as one file; today, answers live across sales-kit files.
- Competitor monitor agent (`autonomous_growth/agents/`) is partial; structured output into the intelligence cluster is open.
- Pricing comparison spreadsheet is referenced in some sales-kit files; a single up-to-date competitive pricing source-of-truth is open.
