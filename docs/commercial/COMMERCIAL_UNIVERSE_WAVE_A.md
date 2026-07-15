# Commercial Universe Wave A — Contract

## Why this is product value

Dealix now has a small, testable core for the thing a company actually needs: one private universe of accounts and relationships that can be viewed by sales, partnerships, market access, service exchange, customer success, and renewal teams without turning the product into another generic CRM.

The core answers four operational questions:

1. Which department objective does this account serve?
2. What relationship exists with the counterparty?
3. Is research allowed, or is contact permission present?
4. What reviewable action and proof should be prepared next?

## Safety boundary

The module is pure and draft-only:

- tenant ID is mandatory on every account and approval envelope;
- unknown/research-only permission blocks external action, regardless of score;
- warm, inbound, referral, opted-in, and approved records still require founder approval;
- no sender, scraper, CRM mutation, payment, calendar invite, or production side effect exists;
- `external_action_allowed` is structurally false.

## Commercial workflow

```text
account + department objective + relationship + permission
  -> deterministic fit score
  -> next action / proof target
  -> Approval Command Center envelope
  -> human approve / reject / edit
  -> channel adapter in a later, separately approved wave
```

## Integration contract

Wave B should adapt `CommercialAccount` and `ApprovalEnvelope` into the existing canonical account and Approval Command Center records. It must not add a second account table, approval queue, or daily scheduler.

Required integration tests:

- tenant A cannot read tenant B's commercial records;
- research-only records remain non-contactable at score 100;
- service-exchange and market-access relationships route to distinct objectives;
- approval envelopes retain source and proof references;
- no calendar or external message is created before approval.

## Scope of this wave

This PR implements domain contracts and regression tests only. Database migration, API routes, UI work, and live connectors belong to later waves after canonical schema mapping and production trust are verified.
