# Account Scoring Model

A deterministic, documented, founder-overridable scoring model. The model is **not** machine-learned. It is rules-based so the founder can audit any A/B/C/Reject decision.

## 1. Inputs (10 fields)

| #  | Field                       | Range  | Direction |
|----|-----------------------------|--------|-----------|
| 1  | Saudi relevance             | 0–10   | Higher better |
| 2  | B2B fit                     | 0–10   | Higher better |
| 3  | High-ticket potential       | 0–10   | Higher better |
| 4  | Buyer clarity               | 0–10   | Higher better |
| 5  | Pain urgency                | 0–10   | Higher better |
| 6  | Outreach fit                | 0–10   | Higher better |
| 7  | Proof fit                   | 0–10   | Higher better |
| 8  | Partner potential           | 0–10   | Higher better |
| 9  | Delivery complexity         | 0–10   | LOWER better |
| 10 | Trust risk                  | 0–10   | LOWER better |

## 2. Composite scores

We compute three composite scores so we can sort accounts multiple ways without losing the underlying inputs.

```
focus_score   = Saudi_relevance + B2B_fit + High_ticket_potential + Buyer_clarity + Pain_urgency
                # 0–50 — drives queue priority
proof_score   = Proof_fit + Partner_potential
                # 0–20 — drives "should we publish a proof artefact?"
risk_score    = Delivery_complexity + Trust_risk
                # 0–20 — LOWER = safer
```

## 3. Priority rule (deterministic)

```
if   focus_score >= 38 and risk_score <= 10:
        priority = "A"
elif focus_score >= 30 and risk_score <= 12:
        priority = "B"
elif focus_score >= 22:
        priority = "C"
else:
        priority = "Reject"
```

Additional hard rejects (any one of these overrides the score):

- `Trust_risk >= 8` → Reject.
- `Delivery_complexity >= 9` → Reject.
- Account in anti-ICP list → Reject.
- Country ≠ KSA AND `Saudi_relevance < 6` → Reject.

## 4. Recommended action (deterministic)

| Priority | Default recommended action                                  |
|----------|-------------------------------------------------------------|
| A        | Founder-approved outreach this week + Sample/Diagnostic     |
| B        | Warm nurture stream + monthly check-in                      |
| C        | Watch list — reassess quarterly                             |
| Reject   | Remove from queue; document reason                          |

## 5. Recommended offer (deterministic)

| Condition                                                                          | Recommended offer                  |
|------------------------------------------------------------------------------------|------------------------------------|
| High_ticket_potential ≥ 8 AND Buyer_clarity ≥ 7 AND Pain_urgency ≥ 7              | Revenue Desk Retainer              |
| Pain_urgency ≥ 7 AND Buyer_clarity ≥ 6 AND first time we engage                    | Revenue Sprint                     |
| Buyer_clarity ≥ 6 but Pain_urgency unknown                                         | Free Sample / Diagnostic           |
| Partner_potential ≥ 7 AND High_ticket_potential ≥ 6                                | Partner / White-label              |
| High_ticket_potential ≥ 9 AND Buyer_clarity ≥ 8 AND we have proof in their sector  | Founder Console / Command Center   |

## 6. Recommended channel (deterministic)

| Condition                                                          | Recommended channel       |
|--------------------------------------------------------------------|---------------------------|
| Buyer has a public LinkedIn AND posts at least monthly             | LinkedIn (founder-led)    |
| Buyer has a public business email AND we have a warm reference     | Email (founder-led)       |
| We have a warm introducer                                          | Warm intro (founder-led)  |
| Buyer reachable only via partner                                   | Partner channel           |
| None of the above                                                  | Defer — needs research    |

## 7. Override

The founder may override any priority at any time. Every override is logged in the CSV with `override_by`, `override_reason`, and `override_at` so the audit trail is intact.

## 8. Schema (CSV)

See `data/growth/account_scores.csv`. The header row is the canonical set of fields.

## 9. KPI on the model

- ≥ 80% of A-priority accounts produce at least one founder-approved outbound within 7 days.
- ≤ 10% of A-priority accounts get flipped to Reject within 30 days (= model accuracy proxy).
- 100% of Rejects carry a documented reason.
