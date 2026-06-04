# 06 — Failure Response Playbook

ماذا نفعل عند الفشل. كل سيناريو له إشارة، إجراء فوري، وتعافٍ.
What to do when something fails. Each scenario has a signal, an immediate action, and recovery.

| Scenario | Immediate action | Recovery |
|---|---|---|
| Website build failed | Read the build log; do **not** deploy | Fix typecheck/build locally; re-run `npm run verify`/`build` |
| Safety audit failed | **Halt** all review/outreach | Inspect `safety_audit.json`; regenerate drafts; re-audit until PASS |
| Drafts < 400 | Block readiness | Re-run generator with `--target 400` (floor enforced) |
| Workflow failed | Read Actions log + artifacts | Reproduce locally with the same script; fix; re-dispatch |
| API health failed | Mark API NO-GO | Check deploy logs; confirm `/health`; rollback if needed |
| Spam / complaint signal | **Stop sending immediately** | Move lead to `suppressed`; review list quality; pause program |
| Professional-network restriction | Stop all platform activity | Manual-only behavior; never automate; appeal per platform |
| Messaging-compliance issue | Stop that channel | Confirm consent + opt-out; document; resume only if compliant |
| Lead quality weak | Pause outreach | Re-score; tighten ICP in `crm_pipeline_schema.json` |
| No replies | Don't increase volume | Improve copy from real signal; change angle, not quantity |
| High rejection rate | Reduce volume | Re-segment; personalize; revisit offer |
| Founder overwhelmed | Cut to top 20 | Time-box review; defer non-critical; protect delivery |

## القاعدة / Rule
> A failing gate is a **stop sign**, not a suggestion. Never bypass `commercial_safety_audit.py`
> or `final_launch_control_verify.py` to "ship". Fix the cause, re-run, then proceed.
