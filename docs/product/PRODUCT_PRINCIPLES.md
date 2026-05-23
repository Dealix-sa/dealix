# Product Principles

> The constitution for product decisions.
> When a feature debate gets stuck, the answer is in here.

## 1. Outcomes > Features

We ship outcomes that the buyer can put on a slide for their CEO. Features that don't produce that outcome don't ship.

## 2. Productize Before Building

Every feature corresponds to a productized offer rung. If a feature doesn't make a rung better, it doesn't ship.

## 3. Trust Beats Speed

If shipping faster means weaker trust gates, we ship slower. Trust is the moat; speed is a tactic.

## 4. Eat Our Cooking

Dealix runs the Dealix company on Dealix. If a feature doesn't survive the founder using it daily, it fails internally before shipping externally.

## 5. AI Prepares, Humans Approve

Every external action has a human approval gate by default. Removing a gate requires a logged decision + the action passing classification rules in `APPROVAL_MATRIX.md`.

## 6. Evidence > Opinion

Every claim about a feature must have evidence. "Customers want this" isn't enough; show the data.

## 7. Documented > Built

A feature isn't done until it has a playbook, a test, and a ledger entry. Working code without docs is half-shipped.

## 8. Bias To Refuse

Default to refusing scope additions. Saying yes is cheap today and expensive tomorrow.

## 9. Reversible First

Build small, reversible features first. Build large irreversible features only with explicit Weekly CEO Review approval.

## 10. Saudi First

Build for the Saudi mid-market context first. International generalization comes after, never before.

## 11. Stable Surfaces, Movable Internals

External-facing surfaces (offer ladder, pricing, approval rules) change rarely and with notice. Internal implementations can change freely.

## 12. Kill With Honor

Killing a feature gets a ledger entry, a learning, and a redirect. Never quiet abandonment.

## When Principles Conflict

If two principles conflict, the order above wins. Trust (#3) always beats speed and outcomes (#1).

## When To Add A Principle

Add a principle only after:
- A real decision exposed the missing rule
- The new rule is general (not case-specific)
- The new rule doesn't contradict an existing one (if it does, supersede the old one explicitly)

## Review Cadence

- Quarterly: read this file end to end during Weekly CEO Review
- Anytime: when a decision feels off, check if a principle is missing
