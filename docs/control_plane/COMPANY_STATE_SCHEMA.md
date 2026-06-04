# Company State Schema

## Purpose
Define the single operating state that Dealix uses to understand the company.

## Owner
Sami / Control Plane owner.

## Review Cadence
Monthly or whenever new systems are added.

## Inputs
- Pipeline data.
- Revenue data.
- Delivery status.
- Trust logs.
- Product status.
- Learning reviews.

## Outputs
- CEO brief.
- Decision queue.
- Risk flags.
- System scorecard.
- Weekly review.

## Revenue State
- cash_collected
- cash_expected
- mrr
- proposals_pending
- pipeline_value
- best_next_close

## Sales State
- new_leads
- qualified_leads
- contacted
- replies
- calls_booked
- proposals_sent

## Delivery State
- active_clients
- reports_due
- qa_needed
- blocked_deliveries
- delivery_on_time_rate

## Trust State
- approvals_waiting
- A3_blocked_actions
- opt_outs
- claims_needing_review
- incidents

## Product State
- ci_status
- bugs_open
- release_candidate
- customer_requested_features
- trust_tests_status

## Learning State
- experiments_running
- latest_win_loss
- best_message
- best_sector
- biggest_objection
- next_experiment

## Rules
- Company State must be evidence-based.
- Unknown values should be marked unknown, not guessed.
- Sensitive data must not be stored in public repo.
- CEO brief must derive from Company State.

## Metrics
- Completeness of state.
- Number of unknown fields.
- Decision usefulness.
- Risk detection accuracy.

## Evidence
- private ops files
- GitHub Actions
- CI output
- revenue logs
- delivery logs

## Last Reviewed
YYYY-MM-DD
