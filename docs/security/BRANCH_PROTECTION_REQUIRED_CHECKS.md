# Branch Protection — Required Checks

On the `main` branch the following GitHub status checks must be
required by branch protection:

- `dealix-ultimate-operating-layer / verify`

This guarantees that policy, agent registry, eval gate, prompt/output
quality, master verifier, and the frontend build all pass before a PR
can merge to `main`.

Setting this up is a one-time manual GitHub step.
