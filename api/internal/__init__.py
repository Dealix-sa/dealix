"""Internal-only API surface for the Dealix Founder Console.

Every route in this package must:
  - require an internal key (auth.require_internal_key),
  - read-only from private ops by default,
  - never trigger external send,
  - queue any write to approval_queue.csv with full audit fields.
"""
