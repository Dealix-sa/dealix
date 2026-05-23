# Revenue Agent Swarm

The set of agents that touch the revenue path:

| id | role |
|---|---|
| `revenue_research_agent` | researches target accounts → lead records |
| `lead_scoring_agent` | scores fit + urgency |
| `outreach_draft_agent` | drafts personalised outreach |
| `followup_planner_agent` | plans next touch |
| `reply_classifier_agent` | classifies inbound replies |
| `sample_draft_agent` | drafts a sample for the prospect |
| `proposal_draft_agent` | drafts the paid proposal |
| `payment_followup_agent` | drafts payment reminders |
| `delivery_copilot` | tracks delivery commitments |
| `partner_revenue_agent` | tracks partner-sourced opportunities |

All swarm members:

* Cannot send externally. Every external-impact action is queued as an
  A2 approval row.
* Run the eval gate before any output is shown to the founder.
* Read only from their declared `data_access_level` subtree.
* Are kill-switched: `POST /api/v1/internal/control/agents/{id}/disable`.

The swarm is intentionally **boring**: it drafts, scores, recommends,
and stops. Sending is the founder's act.
