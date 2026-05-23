# Sample Asset System

> A "sample" is a small, proof-safe artifact that demonstrates the
> Dealix system without giving away the engine. Examples: an anonymized
> diagnostic snippet, a redacted decision passport excerpt, a one-page
> lead-engine signal sheet for one sector.

## Rules

1. Samples are **never** real customer data. They are redacted or
   synthetic.
2. Every sample has a `proof_status` set to either `proof_pack_signed`
   (linked to a real, customer-approved proof) or `synthetic`.
3. The sample's file path lives in `assets/sales/samples/` and is
   tracked in `sales_asset_registry.csv`.
4. Samples are versioned by filename: `sample_<sector>_<offer>_v<NN>.md`.

## Per-offer expectations

| Offer                         | Default sample type                |
| ----------------------------- | ---------------------------------- |
| Managed Pilot (499 SAR)       | redacted diagnostic excerpt         |
| AI Sales Assistant SaaS       | replied-lead sample sheet           |
| Decision Passport             | redacted decision artifact         |
| Customer Health               | health-score excerpt               |
| Proof Curation                | proof-pack page (synthetic)        |
| Growth Signals                | sector signal report excerpt       |
| Executive Command Center      | scorecard screenshot (synthetic)   |

## Doctrine

A prospect cannot be sent a sample that contains another customer's
identifiable data. If a sample would require it, the answer is:
*"We will produce a redacted version after a signed NDA / proof
permission."*
