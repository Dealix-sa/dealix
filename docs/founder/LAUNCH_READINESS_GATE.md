# Launch Readiness Gate

The hard gate that must pass before any public surface (new page, new
campaign, new product) goes live.

## Purpose

Make "ready for the world" a binary, machine-checked state — not a
judgement call made under deadline pressure.

## Owner

Founder. The gate cannot be self-bypassed; even the founder records the
override in the decision log.

## Cadence

- Per launch.
- Re-verified weekly while a campaign is live.

## Source of Truth

- This file (gate checklist).
- `make production-certification` output.

## Gate Checklist

A launch is **ready** only when **every** box is checked.

- [ ] `make everything` exits 0
- [ ] `make production-certification` exits 0
- [ ] Frontend builds clean (`npm --prefix apps/web run build`)
- [ ] /healthz returns 200 from production
- [ ] No banned claims in any public surface
  (`scripts/verify_prompt_output_quality.py`)
- [ ] No direct external send paths
  (`scripts/verify_live_send_safety.py`)
- [ ] Live-send flag (`WHATSAPP_ALLOW_LIVE_SEND`) is off OR a paired
  approval+audit gate is wired
- [ ] All A3 actions in the agent registry require approval
- [ ] All A2/A3 actions write to the audit log
- [ ] CEO daily brief produced today
- [ ] Decision logged in `CEO_DECISION_LOG.md`
- [ ] Rollback plan written into the launch entry

## Inputs

- The artifact being launched (page, campaign, product, agent change)
- The owner of follow-through
- The rollback steps

## Outputs

- A gate verdict (PASS / FAIL) appended to this file
- A decision-log entry referencing the verdict

## KPI

- 0 launches that bypass the gate
- 0 launches with a banned claim
- 0 launches without a documented rollback

## Trust Boundary

The gate cannot be skipped silently. Skipping it is itself a logged
decision with a written reason.

## Failure Mode

- A box left unchecked → gate FAIL → no launch.
- A box checked falsely → caught by the corresponding verifier; treated
  as a process failure.

## Recovery Path

1. Re-run `make everything`.
2. Fix the first failing item.
3. Re-run the gate.
4. Only when all boxes are checked, append a PASS verdict here.

## Verification

```bash
make everything
make production-certification
```

## Next Action

If you are about to launch anything, run `make production-certification`
first. If it does not exit 0, do not launch.
