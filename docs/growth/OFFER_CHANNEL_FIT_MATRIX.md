# Offer × Channel × Persona Fit Matrix

The single decision matrix the targeting OS uses to recommend the **right offer**, on the **right channel**, for the **right persona**.

## 1. Master matrix

Row = persona. Column = offer rung. Cell = recommended channel + opening hook.

| Persona ↓ \ Offer →    | Free Sample / Diagnostic | Revenue Sprint                       | Managed Pilot                       | Revenue Desk Retainer               | Founder Console                      | Enterprise OS | Partner / White-label |
|------------------------|--------------------------|--------------------------------------|-------------------------------------|-------------------------------------|--------------------------------------|---------------|-----------------------|
| P-CEO-MidMarket        | —                        | Warm intro · "Predictable revenue"   | Warm intro · "Pilot in 30 days"     | Warm intro · "Quarterly retainer"   | Warm intro · "One pane, ten functions" | —             | —                     |
| P-CRO                  | LinkedIn · "30-day diag" | LinkedIn · "7-day Revenue Sprint"    | LinkedIn · "Pilot a sequence"       | LinkedIn · "Monthly Revenue Desk"   | —                                    | —             | —                     |
| P-Founder-Agency       | —                        | LinkedIn · "Founder-to-founder sprint" | —                                  | LinkedIn · "Operate our desk"       | —                                    | —             | LinkedIn · "Co-deliver / refer" |
| P-Implementer          | Warm intro · "Sample pack"| Warm intro · "Sprint for one segment" | Warm intro · "Pilot in your sector" | Warm intro · "Quarterly retainer"   | —                                    | —             | Warm intro · "Reseller partner"|
| P-Cyber-SalesDirector  | LinkedIn · "Sector sample"| LinkedIn · "ABM Sprint"             | LinkedIn · "Sequence pilot"         | LinkedIn · "Channel desk"           | —                                    | —             | —                     |
| P-Logistics-CCO        | Warm intro · "Sector pack"| Warm intro · "Sprint for KSA mega-projects" | Warm intro · "Pilot on one segment" | Warm intro · "Quarterly retainer"   | —                                    | —             | Warm intro · "Sector partner" |
| P-SaaS-RevOps          | —                        | LinkedIn · "KSA-compliant Sprint"   | LinkedIn · "Pilot a desk"           | LinkedIn · "Revenue Desk monthly"   | —                                    | —             | —                     |

Legend: `—` means *do not pitch this offer to this persona*. Persona's "refused offers" trump the matrix.

## 2. How to read

1. Take an account's primary persona.
2. Read the row.
3. Sort by offer rung (right is heavier). Start with the **lightest** appropriate offer for first contact.
4. Use the listed channel + opening hook.
5. Never skip rungs without a documented reason.

## 3. Channel doctrine

| Channel       | When                                            | Limits                                                       |
|---------------|-------------------------------------------------|--------------------------------------------------------------|
| Warm intro    | We have a mutual contact who can introduce      | The introducer must approve our message                       |
| LinkedIn      | The buyer posts and accepts connections         | First touch is < 80 words; no automation; founder-approved   |
| Email         | Buyer has a public business email & no LinkedIn | First touch < 110 words; no attachments unless asked         |
| Partner       | Buyer is reachable via a Dealix partner         | Partner co-signs the message                                  |
| Phone         | Buyer explicitly invited a call                 | Never cold-call without an invite                            |

## 4. Cross-rung rules

- **Never** skip from Free Sample to Founder Console. Honour the ladder.
- A **Sprint** may upgrade to a **Retainer** only after a delivered Sprint with measured results.
- A **Retainer** may upgrade to a **Founder Console** only after 90 days of retainer history.
- An **Enterprise OS** engagement requires founder + customer-executive co-signature.

## 5. Refused combinations

Hard refusals (verifier-enforced):

- P-CRO + Founder Console — not their buying authority.
- P-Logistics-CCO + Founder Console — procurement-led; pitch the desk instead.
- P-Founder-Agency + Free Sample — they won't engage with a freebie.
- Any persona + Enterprise OS before having delivered 2 retainers in their sector.

## 6. Output schema

The matrix is rendered into `data/growth/distribution_machines.csv` and informs every outbound draft's `recommended_offer` and `recommended_channel` fields.

## 7. KPI

- ≥ 70% of A-priority accounts get a matching offer + channel within 7 days.
- ≤ 5% of approved drafts violate the matrix.
- Zero approved drafts pitch a refused combination.
