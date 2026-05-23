# No-Overbuild Policy

> Over-built products kill founders.
> Code we did not need cost us the customer we did not get.

## The Rule

Build the **smallest** thing that:

1. Removes a measured friction, **or**
2. Enables a measured revenue motion, **or**
3. Repays a measured trust risk.

Anything else is overbuild.

## What is overbuild

- A feature for a hypothetical customer.
- Generality before three concrete uses.
- A configuration option before two divergent uses.
- A second tool when one tool would suffice.
- An abstraction layer with one implementation.
- A dashboard that no one reads weekly.
- A document that is not referenced in any workflow.
- An agent for a workflow at Level < 2.

## The Three Questions Before Building

1. **Who specifically needs this?** Name them.
2. **What would they do tomorrow without it?** Be honest.
3. **What is the smallest version that proves the value in one week?**

If you cannot answer all three, do not build.

## The "Smallest Version" Discipline

- Manual first.
- Template second.
- Script third.
- Service fourth.
- SaaS last, and only after Levels 1–4 are complete (`PRODUCTIZATION_ENGINE.md`).

## When we **do** build

Even when the rule allows building, we minimise:

- Two configuration options, not five.
- One dashboard panel, not ten.
- One model vendor first; add fallback only when usage justifies.

## Anti-Patterns

- "It is cool tech."
- "It would be elegant."
- "We should have it because everyone has it."
- "Maybe in the future…"

## Audit

Quarterly: audit recent builds.

- For each: is it being used weekly by either us or a customer?
- If no: it is a build we should not have done. Log the lesson.
