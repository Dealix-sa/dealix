# Revenue Agent Swarm

The Dealix revenue agents work as a swarm with strict role boundaries.
All of them write to the **approval queue** before any external action.

| Agent                    | Role                                     |
|--------------------------|------------------------------------------|
| revenue_research_agent   | research target accounts                 |
| lead_scoring_agent       | score leads against ICP + intent         |
| outreach_draft_agent     | draft outreach (never send)              |
| followup_planner_agent   | plan follow-ups                          |
| reply_classifier_agent   | classify replies                         |
| sample_draft_agent       | draft sample deliverables                |
| proposal_draft_agent     | draft proposals (A3 to send)             |
| payment_followup_agent   | draft payment follow-ups                 |

Every agent has `kill_switch: true` and can be disabled via
`POST /api/v1/internal/control/agents/{id}/disable`.
