# Sovereign Readiness Scorecard

Generator: [`scripts/generate_sovereign_readiness.py`](../../scripts/generate_sovereign_readiness.py).

## What it measures

Per-layer presence + verifier-pass:

* Founder Console pages (16 pages).
* Internal API plumbing (auth, runtime reader, policy adapter, router).
* Policy-as-code, Agent Registry, Eval Gate.
* Bootstrap + worker scripts.
* CI workflow.
* Verifier scripts pass locally.

Each layer is 1 (PASS) or 0 (FAIL). Total is a percentage.

## Honesty

A 100% sovereign-readiness score does **not** mean Dealix is
production-ready. Production readiness is a separate gate — see
[`docs/security/PRODUCTION_SECURITY_GATE.md`](../security/PRODUCTION_SECURITY_GATE.md).

The Sovereign Readiness scorecard measures whether the *control surface*
is wired and verifiable.

## Run

```bash
make sovereign-readiness PRIVATE_OPS=/opt/dealix-ops-private
```
