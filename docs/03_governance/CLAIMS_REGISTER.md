# Claims Register

> **Status:** CANONICAL · **Owner:** Founder · **Last reviewed:** 2026-06-05
>
> Human-readable companion to the machine-checked register at
> `dealix/registers/no_overclaim.yaml`. Doctrine rule #7: no public claim without
> evidence here.

---

## 1. How claims work

A claim may appear publicly (README, website, deck, social) **only if**:
1. It exists in `dealix/registers/no_overclaim.yaml` with status `Production`.
2. It does not exceed the status in `docs/00_platform_truth/MODULE_STATUS_MAP.md`.
3. It has evidence in Proof OS.

The CI gate fails a release if README/deck claims are not present in the register
or are not `Production`-status.

## 2. Status legend (matches the YAML register)

| Status | Meaning |
|---|---|
| Planned | Not built yet |
| Pilot | Built, tested internally only, not default-on |
| Partial | Available under a flag, missing hardening |
| Production | Fully built, tested, default-on |

## 3. Claims we currently make (and their status)

| Claim | Status | Evidence |
|---|---|---|
| Saudi AI Business Operating System (category framing) | Production | This is positioning, not a capability claim; backed by the module map. |
| Approval-first (no auto-send) | Production | `HUMAN_APPROVAL_POLICY.md`, agent contracts, no-send default. |
| PDPL-aware | Production | `PRIVACY_AND_PDPL_READINESS.md`, Data OS minimum-data rule. |
| ZATCA-aware (advisory, not a provider) | Production | `FINANCE_OS.md` ZATCA posture section. |
| NCA-aligned controls | Production | `SECURITY_BASELINE.md`, Governance OS. |
| Command Sprint deliverable | Production | `COMMAND_SPRINT_OFFER.md`, delivery spec. |
| Revenue OS engines | Partial | Service-delivered; not self-serve SaaS. |
| Full 14-module platform "ready" | **Not claimed** | Modules carry honest status; do not imply all ready. |

## 4. Phrases we never use

"PDPL certified", "ZATCA certified", "NCA certified", "fully automated",
"guaranteed revenue". See `docs/00_platform_truth/PUBLIC_POSITIONING.md`.

## 5. Maintenance

- Add a row here and in the YAML register whenever a new public claim is made.
- Downgrade or remove a claim the moment its evidence weakens.
- Re-review on every release alongside the Module Status Map.
