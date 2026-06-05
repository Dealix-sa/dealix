# Data OS

> **Status:** `BETA` · **Plane:** Data · **Owner:** Founder · **Last reviewed:** 2026-06-05
>
> The data layer. PDPL is not a side topic — it is a differentiator.

---

## Purpose

Govern data intake, quality, consent, and lifecycle so Dealix is clean and
trustworthy by design.

## Functions

- Intake
- Normalization
- Deduplication
- Source tracking
- Consent
- Retention
- Deletion / export requests
- Data quality score

## Data principle

```
Collect minimum.
Store intentionally.
Delete predictably.
Prove responsibly.
```

## PDPL as a differentiator

A recent study of 100 Saudi e-commerce sites found that only **31%** disclosed all
four privacy elements examined: retention period, right to request deletion, right
to request a copy, and a complaints mechanism. This is a strong opportunity for
Dealix to stand out with clear privacy and data practices from day one.

## Minimum data (Command Sprint)

company name · industry · contact role · current sales/delivery flow ·
top 5 opportunities · current offer · follow-up examples · pain points ·
approval contact · consent.

## Forbidden data (at start)

passwords · full CRM dumps · unnecessary sensitive data · customer API keys ·
large personal files · scraped data from platforms that do not allow it.

## Inputs / Outputs

**Inputs:** consented customer data only. **Outputs:** normalized, deduplicated,
source-tracked records with a data quality score and a retention tag.

## Approval & doctrine

- Deletion and export requests are honored and **logged** (no deletion without a record).
- Consent is captured at intake.
- See `docs/03_governance/DATA_RETENTION.md` and `PRIVACY_AND_PDPL_READINESS.md`.

## Deeper references

- `db/`, `integrations/`, `docs/04_data_os/`, `docs/06_data_os/`
