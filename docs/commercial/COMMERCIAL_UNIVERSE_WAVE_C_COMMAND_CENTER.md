# Commercial Universe Wave C — Daily Command Center Projection

The command-center projection is a pure read model for the founder and
department workspaces. It accepts the tenant-scoped accounts and approval
envelopes already produced by Waves A and B, then returns:

- account count
- pending approval count
- blocked count
- department distribution
- deterministic priority account IDs
- next actions for the priority queue

Ranking uses the existing fit score and urgency, with account ID as a stable
tie-breaker. Only approval-required items enter the priority list; research-only
items remain visible as blocked and cannot be promoted by scoring.

This is not a scheduler or outbound executor. A later API/UI integration can
render the snapshot in the daily command center while continuing to use the
canonical approval queue, tenant isolation, proof targets, and audit links.

Recommended follow-up:

1. Persist the universe in existing tenant-scoped database models.
2. Add an API read endpoint behind the existing authentication/RBAC boundary.
3. Render department views and meeting-prep cards in apps/web.
4. Keep external execution behind the existing approval gate.
