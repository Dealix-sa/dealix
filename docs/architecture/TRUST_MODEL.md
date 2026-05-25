# Trust Model

The trust gate inspects every request payload for:

- **Overclaim** — phrases like "guaranteed sales", "100% conversion".
- **Sovereign leak** — references to `sovereign_memory`, `internal_strategy`,
  `raw_customer_export` in an external-action payload.
- **Unapproved pricing** — pricing in an external email without an
  approval marker.

Trust signals (case studies, customer quotes, verified outcomes,
evidence packs, security posture, partner testimonials, public
methodology) are required for any externally-published claim. The
`TrustSignalLedger.check_claim(subject, minimum=N)` helper enforces a
minimum count before a campaign can launch.
