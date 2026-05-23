# Proof Library

> Where every approved proof artifact lives, with its consent record.

## Library Schema

```
- id: P-yyyy-mm-dd-NN
  title: "..."
  type: case_study / quote / sample_anonymised / aggregate_stat
  customer: name (or "anonymised")
  date_published: yyyy-mm-dd
  consent_reference: path to consent letter
  consent_expires: yyyy-mm-dd (or "until withdrawn")
  evidence_links:
    - ...
  public_url: ...
```

## Categories of Proof

### Strongest: Named case studies
- Customer is named.
- Written consent on file.
- Numbers verifiable.

### Strong: Approved quotes
- Customer quote with written consent.
- Used in proposals or posts.

### Moderate: Anonymised samples
- Real Sprint output, customer names removed.
- Used for demo and as Sprint preview.

### Light: Aggregate statistics
- "Across 12 Sprints" type figures.
- Backed by ledger entries.

## Library Use

- Sales: `docs/sales/PROOF_BASED_SALES.md` references the library.
- Content: posts cite library items as their evidence link.
- Audit: `make audit` checks that referenced items still have valid
  consent.

## Library Maintenance

- Monthly: any new consent collected.
- Quarterly: any consent expiring soon; renewal requested.
- Annually: full re-confirmation of every named case study.

## Forbidden

- "Proof" without an entry in this library.
- An entry without a consent reference (for named items).
- Listing a case study in the library before consent is on file.
