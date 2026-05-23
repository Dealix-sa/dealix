# Sample Generation System

> How we produce sanitized sample artifacts to send prospects.
> Samples close deals — but unsafe samples kill the company. This system governs both.

## What A Sample Is

A "sample" is a pre-built, sanitized artifact that demonstrates what a Sprint or Data Pack delivers — without using any single client's real data.

Examples:
- Sample lead scorecard (50 fictional companies in a sector, real format)
- Sample message playbook (Arabic + English, 3 variants for an objection)
- Sample sector benchmark (peer-aggregated, fully anonymized)
- Sample evidence pack template (showing how we cite sources)

## Why This Matters

Samples are how a 499 SAR Sprint feels real before the buyer pays. But:
- A sample with real client data is a Trust incident
- A sample that overclaims results is a Trust incident
- A sample with broken sources is a credibility incident

## Sample Production Workflow

1. Founder (or sample agent) writes a sample using **synthetic** or **publicly cited** data only
2. Trust check: `claim_guard.py` passes (no unsubstantiated claims)
3. Trust check: source citations valid (every number → public URL or "synthetic example")
4. Founder reviews and approves
5. Sample stored in `content/proof_library/` (private repo, with public-safe export path)
6. Sample versioned (filename includes date + version: `sample-logistics-scorecard-2026-05-23-v1.pdf`)

## Required Labels On Every Sample

Every sample carries this header:

```
SAMPLE ARTIFACT
For illustrative purposes. Data is {synthetic | publicly cited}.
Not derived from any single client.
Version: YYYY-MM-DD vN
```

This label is non-negotiable. Removing it converts the sample into an unverified claim.

## Source Discipline

- **Synthetic data** must look realistic but be clearly fictional (use sector but fake company names like "Acme Logistics Co.")
- **Publicly cited data** must include the URL and the access date
- **Aggregated data** (after we have multiple sprints) must be unambiguously anonymized (no n=1)
- **Never** use a prior client's data, even sanitized, without explicit written client consent + advisor review

## Sample Library Structure

```
content/proof_library/
├── sector/
│   ├── logistics/
│   │   ├── sample-scorecard-v1.pdf
│   │   ├── sample-message-set-v1.md
│   │   └── sample-benchmark-v1.pdf
│   ├── b2b_services/
│   └── manufacturing/
├── format/
│   ├── sample-data-pack-v1.pdf
│   └── sample-evidence-pack-v1.pdf
└── INDEX.md
```

## Sample Approval Tier

- A2 default (founder approval per sample, batch-approvable)
- A3 if the sample makes any claim about results (e.g. "Sprint X delivered Y%") — requires evidence pack

## When To Send A Sample

- After: prospect explicit interest / reply
- Before: any proposal (samples derisk the proposal ask)
- During: discovery call (live walkthrough is best)

## When NOT To Send A Sample

- Cold first touch (looks like spam)
- To anyone on the suppression list
- To anyone outside ICP
- Before the sample passed the approval workflow

## Sample Refresh Cadence

- Per sprint shipped: update the matching sector sample with a new (sanitized) data point
- Monthly: review for stale references (URLs, dates, prices)
- Quarterly: kill samples that haven't been sent in 90 days

## When A Sample Goes Wrong

If a recipient flags:
- Inaccuracy → fix the sample, log incident, retract from any prospect who received the bad version
- Overclaim → revise + add citation, log incident, notify recipients
- Privacy concern (recognized a real company) → immediate retract, incident log, root cause

Every sample incident appears in `trust/data_incidents.md`.

## Sample Volume Targets

- 1 new sample per active sector per month
- Each sample sent ≥ 5 times before considered "in production"
- Each sample logged when sent: which prospect, which sample version

## Tools

- `dealix/agents/` sample_generation_agent (when present) — drafts sample from sector template
- Trust gate enforces label + source citation before publish

## What This System Refuses

- Faked screenshots ("here's what real client X got")
- "Composite case studies" without explicit composite labeling
- Samples generated on the fly without review
- Samples that include unverifiable third-party data
