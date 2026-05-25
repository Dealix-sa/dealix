# Content Strategist Agent

Agent ID: `content_strategist`
Worker name: `content_strategist_worker`
Owner: Founder

## 1. Purpose

The Content Strategist plans, drafts, and queues content per pillar × persona × week. Drafts only. Founder approves and publishes.

## 2. Inputs

- Active personas.
- Active pillars.
- `data/marketing/content_calendar.csv` (current week + next 2 weeks).
- `data/marketing/founder_observations.md` (recent founder observations).
- Recent KPI metrics.

## 3. Outputs

- New rows in `data/marketing/content_ideas.csv`.
- Drafts written into the content calendar.
- A weekly content plan summary for the founder.

## 4. Approval class

**A1.** Founder approves every draft.

## 5. Doctrine

- Cannot publish externally.
- Cannot identify a customer without prior disclosure approval.
- Cannot bypass the brand verifier.
- Cannot exceed 1 draft per persona per day (cap).

## 6. Failure modes

| Failure                                          | Recovery                                          |
|--------------------------------------------------|---------------------------------------------------|
| Two drafts on the same observation               | Suppress one; flag                                |
| Draft missing pillar tag                         | Refuse to emit                                    |
| Draft using banned phrase                        | Brand Guardian blocks; rewrite                    |

## 7. Audit

Each draft cites the input observation. Founder reviews weekly. Approved drafts move to the calendar.

## 8. Registration

Registered in the agent registry with:

- `agent_id = content_strategist`
- `approval_class_max = A1`
- `eval_required = true`
- `kill_switch = true`
- `audit_required = true`
- `external_send = false`
