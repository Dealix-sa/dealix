# Tenant Security Model

## Rules

1. Fail closed if tenant context is missing.
2. Block cross-tenant access by default.
3. Require role checks for billing, invites, settings, and audit exports.
4. Write audit events for admin actions.
5. Keep outbound disabled unless controlled-live gates are explicitly enabled.

## Outbound safety defaults

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

## Audit events

Audit events should include:

- organization_id
- workspace_id
- actor_id
- action
- resource_type
- resource_id
- status
- created_at

## Current verdict

Safe for internal demo and founder-led beta. Not yet public self-serve SaaS.
