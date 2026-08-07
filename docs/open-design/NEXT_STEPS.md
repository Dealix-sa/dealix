# Next Steps: Dealix Design Command Room OS

## Phase 1 — Contract and rules

Completed in this PR:

- Dealix design system contract
- artifact rules
- Open Design integration strategy
- Design Command Room project skill
- attribution and validation notes

## Phase 2 — First artifact generator

Recommended next PR:

```text
scripts/design/generate_design_artifact.py
reports/design/latest.md
make design-room
```

The generator should create one reviewed markdown/HTML-ready artifact from a structured brief.

## Phase 3 — Revenue Command Room prototype

Recommended next PR:

```text
reports/design/revenue-command-room-v0.md
apps/web/app/design-lab/revenue-command-room/page.tsx
```

Keep the route demo-only until approved.

## Phase 4 — Sales deck system

Recommended next PR:

```text
sales/decks/templates/dealix_sales_deck.md
scripts/design/generate_sales_deck.py
reports/design/sales-deck-latest.md
```

## Phase 5 — Proof pack system

Recommended next PR:

```text
reports/proof/templates/client_proof_pack.md
scripts/design/generate_proof_pack_artifact.py
```

## Phase 6 — Optional Open Design runtime evaluation

Only evaluate running Open Design itself outside Dealix after the Dealix-native Design Command Room OS proves useful. Do not add its runtime stack to Dealix unless there is a clear commercial reason.
