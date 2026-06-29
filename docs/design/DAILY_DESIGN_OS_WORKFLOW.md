# Daily Dealix Design OS Workflow

## Morning

Run:

```bash
make design-os-generate TYPE=founder-war-room
make design-os-generate TYPE=revenue-command-room
```

Review:

- highest-value founder decision
- revenue next actions
- approval cards
- trust/outbound status
- blockers

## Midday

For an active client or prospect, run one focused artifact:

```bash
make design-os-generate TYPE=sales-deck
make design-os-generate TYPE=client-proof-pack
make design-os-generate TYPE=client-growth
```

## End of day

Check:

```bash
cat reports/design/latest.md
```

Record:

```text
Decision made:
Action taken:
Proof created:
Next review:
```

## Safety rule

Generated artifacts stay internal until claims, approval state, and handoff target are reviewed.
