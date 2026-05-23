# Product Strategy

> What we build, in what order, why.
> Pairs with `docs/product/BUILD_DEFER_KILL.md` and `docs/product/PRODUCT_PRINCIPLES.md`.

## Product Thesis

The product is the **Company Operating System** that runs revenue-ops for the founder, with AI as a preparation layer and humans as the approval layer.

The product is **not**:
- A SaaS subscription with a polished UI as the primary deliverable
- A general "AI agent platform" for everything
- A marketing automation tool

## Build Order (this quarter)

The order is dictated by what unblocks revenue:

1. **Trust & Governance OS code** (now) — approval matrix, claim guard, policy engine. Unblocks every external action.
2. **Revenue Sprint productization** (now) — make Sprint a documented, repeatable, evidence-producing process.
3. **Sector playbooks** (after first sprint) — Tier 1 sectors get scoring + message + objection sets.
4. **Founder Brief generator** (after sprint #2) — automate the Daily Brief from CSV sources.
5. **Managed Ops pilot template** (after retainer #1) — productize the monthly retainer.

That's it. Everything else is DEFER until these 5 are real.

## Build Heuristics

Apply in order:
1. Does building this remove a founder bottleneck > 2 hr/week? → BUILD
2. Does building this raise close rate ≥ 10%? → BUILD
3. Does building this raise delivery throughput ≥ 20%? → BUILD
4. Does building this reduce a Trust risk on the register? → BUILD
5. Otherwise → DEFER (with revisit date)

## Don't-Build List (this quarter)

- Public marketplace for AI agents
- Multi-tenant SaaS dashboard
- Mobile app
- Marketing site beyond the landing page that exists
- Self-serve checkout
- Anything in `archived_strategy/` or `auto_client_acquisition/` that isn't actively serving a sprint

These are not bad ideas. They are mistimed.

## How Strategy Becomes Product Tickets

- A strategy decision → a one-page in `docs/product/FEATURE_INTAKE.md`
- A one-page → a PR with a `feature/` branch
- A PR → tests + docs + ledger entry
- A merged PR → a row in `DEALIX_EXECUTION_LEDGER.md`

If a feature ships without an intake one-pager, that's a process bug — log it.

## Product Org (this quarter)

- **Founder** — every role until otherwise stated
- **AI** — drafts, scoring, enrichment, brief generation
- **Contractor** (only when triggered by `docs/people/HIRING_TRIGGERS.md`) — execution, not decisions

## Distribution Strategy (product-coupled)

- Every product update produces a public learning post (Content OS)
- Every shipped feature on the Trust layer produces a "trust update" note
- We do not announce features until at least one paying customer is using them in production

## What Strategy Refuses

- Roadmaps longer than 90 days (we don't know yet)
- Features without an ICP they serve
- Features without a trust gate when they touch external action
- Features built to attract investors rather than customers
- "Platform" framing before we have a system worth standing on
