# Executive Control Plane

## Purpose
The control plane is the system that decides what the founder works on. It is intentionally narrow: one brief, one queue, one score.

## Surfaces
1. **Mission control** — the operating state right now (`founder/mission_control.md`).
2. **CEO action queue** — the ordered list of actions (`founder/ceo_action_queue.md`).
3. **Control tower brief** — the morning brief (`founder/control_tower_brief.md`).
4. **CEO business score** — weekly company health (`business_audit/ceo_business_score.md`).
5. **Execution assurance report** — proof we are following our own system (`evidence/execution_assurance_report.md`).

## Decision algorithm
The priority router (`control_plane/priority_router.py`) scores candidate actions by:
- **Money proximity** (closer to cash = higher).
- **Reversibility cost** (less reversible = higher).
- **Time decay** (older = higher up to a cap).
- **Founder bottleneck** (only founder can do it = higher).

The strategic decision engine (`control_plane/strategic_decision_engine.py`) handles the weekly bet.

## Loops
- **Daily**: mission control + CEO action queue + control tower.
- **Weekly**: business score + assurance report + strategic decision engine.
- **Monthly**: access review + restore drill + pricing review.

## Authority
- The founder can override the queue, but every override is logged in `trust/approval_log.csv`.
- The control plane never sends external messages.
- The control plane never spends money.

## Outputs go to private ops only
None of the executive control plane outputs are committed to the public repo. They live in `dealix-ops-private/founder/` and `dealix-ops-private/business_audit/`.
