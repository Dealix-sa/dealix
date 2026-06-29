# Dealix Design OS Automation Suite

## Purpose

This suite upgrades the Dealix Design Command Room OS from one-off artifact generation into a practical review and handoff system.

It adds four operating capabilities:

1. **Daily Pack** — generate all core artifacts in one run.
2. **Validation** — check draft safety, required metadata, approval state, and live-send status.
3. **Index** — build a browsable artifact inventory.
4. **HTML Preview** — render the latest artifact into an internal static preview.

## Commands

```bash
make design-os-daily
make design-os-validate
make design-os-index
make design-os-html
make test-design-os
```

## Output paths

```text
reports/design/latest.md
reports/design/latest.json
reports/design/latest.html
reports/design/INDEX.md
reports/design/VALIDATION.md
reports/design/<artifact>-<timestamp>.md
reports/design/<artifact>-<timestamp>.json
```

## Safety model

The suite remains draft-only.

It does not:

- send externally
- mark artifacts as approved
- alter production UI
- add runtime dependencies
- use external APIs
- change Railway/deployment settings

## Validation checks

The validator checks:

- required artifact metadata
- `live_sends == 0`
- generated artifacts are not `approved_for_client` or `approved_for_production`
- safety status exists
- sections exist
- risky claim terms are flagged

## Best daily run

```bash
make design-os-daily CONTEXT="Dealix founder operating day: revenue, delivery, design, proof, and next actions."
cat reports/design/VALIDATION.md
cat reports/design/INDEX.md
```

## Best commercial run

```bash
make design-os-generate TYPE=sales-deck CONTEXT="Saudi B2B prospect pilot for Revenue Command Room"
make design-os-validate
make design-os-html
```

## Best delivery run

```bash
make design-os-generate TYPE=client-proof-pack CONTEXT="Client delivery sprint from diagnosis to proof pack"
make design-os-validate
make design-os-index
```

## Promotion rule

Validation is not approval. It only confirms the artifact is structurally safer for review. Client or production promotion still needs human approval.
