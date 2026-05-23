# Escalation Matrix

The system must know when to wake the CEO and when not to. If everything
is urgent, nothing is urgent.

## Red Escalations
Immediate CEO attention:
- A3 action attempted
- public repo safety violation
- client data exposure
- payment dispute
- delivery overdue for paid client
- CI broken on main
- legal/compliance claim requested

## Yellow Escalations
Review within 24 hours:
- proposal waiting approval
- client health below 60
- follow-ups overdue
- high-value lead replied
- pricing exception requested
- delivery QA pending

## Green Notifications
No urgent action:
- lead batch ready
- content draft ready
- weekly report generated
- new experiment logged

## Mapping to Company State

The Control Plane derives Red / Yellow signals automatically from
`control_plane/company_state.py` (`red_signals()`, `yellow_signals()`).
Any new red/yellow rule must be reflected in both this document and the
state object so that the CEO Brief shows it.
