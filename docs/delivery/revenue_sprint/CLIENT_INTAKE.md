# Client Intake — Template

> Filled at Day 0 (scope signed, payment received).

```yaml
client_id: yyyy-mm-dd-<short-name>
legal_name: ""
website: ""
sector: ""
size_employees: ""
size_revenue_range: ""
geo_focus: "Saudi Arabia / GCC / global"
language_preferences:
  primary: "Arabic / English"
  secondary: "..."
tone: "formal / direct / consultative"
contract:
  type: "Sprint / Pilot / Retainer"
  price_sar: 0
  payment_received: yyyy-mm-dd
  scope_signed_on: yyyy-mm-dd
icp_definition:
  sectors: []
  company_size: ""
  decision_makers: []
  trigger_signals: []
  exclusions: []
existing_pipeline_overlap:
  shared_crm: false
  do_not_contact: []
delivery_channel: "shared sheet / CRM / email"
delivery_window:
  start: yyyy-mm-dd
  handoff_target: yyyy-mm-dd
decision_maker_at_client: ""
day_to_day_contact_at_client: ""
notes: |
  Free text from onboarding call.
```

Stored at `dealix-ops-private/clients/<client_id>/intake.yaml`.

## Required at intake

- [ ] Scope signed (PDF in client directory)
- [ ] Payment / PO received (receipt or PO in client directory)
- [ ] ICP defined in writing
- [ ] Decision-maker named
- [ ] Delivery channel agreed
- [ ] Onboarding call booked
- [ ] Client added to `client_register.csv`

Any unchecked box = no Sprint start.
