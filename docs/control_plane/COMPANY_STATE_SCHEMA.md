# Company State Schema

> The Control Plane reads from many systems (CRM, ledgers, pipelines,
> approval logs, trust queues, CI). Rather than each consumer poking each
> system, we materialise the daily state into one typed object so every
> downstream loop (CEO Brief, Decision Queue, Action Router, Risk Engine,
> Approval Router) reads from the same picture.

The canonical implementation lives in `control_plane/company_state.py`.

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

## Derived Signals

The state object exposes two derived views consumed by the Escalation
Matrix:

- `red_signals()`   -- A3 attempts, open incidents, blocked paid delivery, CI broken on main.
- `yellow_signals()` -- approvals/proposals waiting, QA pending, replies without follow-up calls.

## Update Cadence

| State block | Source system               | Cadence       |
|-------------|-----------------------------|---------------|
| Revenue     | invoices, manual_payment_log| daily         |
| Sales       | CRM, outreach pipeline      | daily         |
| Delivery    | delivery/qa/, runbooks      | daily         |
| Trust       | approval log, A3 guard      | live          |
| Product     | CI status, bug tracker      | live          |
| Learning    | experiment_log, win_loss    | weekly        |
