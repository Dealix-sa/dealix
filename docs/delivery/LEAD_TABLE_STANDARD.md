# Lead Table Standard

## Purpose
Define the quality standard for Revenue Sprint lead tables.

## Required Fields
- company
- sector
- website
- buyer_title
- why_relevant
- priority
- evidence
- suggested_angle
- source
- notes

## Priority Rules
- A = strong ICP fit, clear buyer, clear evidence.
- B = likely fit, needs validation.
- C = weak or exploratory.
- Reject = does not match ICP.

## Quality Rules
- Every A-priority lead needs evidence.
- Every lead needs a reason.
- No duplicates.
- No irrelevant sectors.
- No unsupported claims.
- Suggested angle must be specific.

## Evidence
- website
- public company page
- sector signal
- role relevance
- public business context

## Anti-Patterns
- "Looks like a good fit" without a reason.
- Same evidence string reused across many leads.
- Buyer titles like "decision maker" — must be specific.
- Adding sectors the client said to exclude.

## File
clients/<client_name_private>/lead_table.csv

## Header (canonical)
```
company,sector,website,buyer_title,why_relevant,priority,evidence,suggested_angle,source,notes
```
