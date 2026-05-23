# Trust Guardian Agent

`trust_guardian` enforces policy at the moment of drafting. It runs:

- forbidden phrase detection
- claim overclaim detection
- suppression list lookup
- secret pattern detection
- evidence link presence (for A3)

When a violation is found the agent writes to `trust/trust_flags.csv`
in the private ops tree and blocks the draft from advancing to the
approval queue.
