#!/usr/bin/env python3
"""Proof Asset OS — generate honest, anonymized proof TEMPLATES (review-only).

Outputs under outputs/proof_assets/templates/:
    anonymized_case_template.md
    before_after_workflow_template.md
    proof_permission_checklist.md

These are blank templates with guardrails against fake claims. They publish
nothing and contain no real client data.

    AI prepares. Founder approves. Manual action only. No external sending.
"""

from __future__ import annotations

from _v7_revenue_common import OUTPUTS, SAFETY_BANNER, write_text

ANON_CASE = f"""# Anonymized Case Template

> {SAFETY_BANNER}
> Use only with written client permission. No fake metrics. No guaranteed ROI.

- Sector (generic): ____
- Company size band: ____
- Region: ____

## Challenge
Describe the verified problem in neutral terms. No identifying details.

## What we did
- Workflow mapped: ____
- Review-only automation prepared: ____
- Human approval gate kept on: ____

## Result (only if measured and client-approved)
- Metric: ____ (before) → ____ (after)
- Time period: ____
- Source of measurement: ____

## Permission
- [ ] Client approved this anonymized write-up in writing.
- [ ] No confidential data or identifiers included.
"""

BEFORE_AFTER = f"""# Before / After Workflow Template

> {SAFETY_BANNER}
> Only document changes you actually observed. No invented numbers.

| Step | Before | After |
| ---- | ------ | ----- |
| Trigger | ____ | ____ |
| Manual work | ____ | ____ |
| Approval | ____ | ____ (human kept in loop) |
| Output | ____ | ____ |

## Notes
- External actions remain manual/founder-approved in the "after" state.
- Include measurement method for any quantitative claim.
"""

PERMISSION = f"""# Proof Permission Checklist

> {SAFETY_BANNER}

- [ ] Written client consent obtained before publishing anything.
- [ ] All identifiers removed or anonymized.
- [ ] Every metric is real, measured, and sourced.
- [ ] No guaranteed-ROI or unverifiable claims.
- [ ] Client reviewed the final asset.
- [ ] Founder approved publication (manual, no auto-posting).
"""


def generate() -> dict:
    out_dir = OUTPUTS / "proof_assets" / "templates"
    files = {
        "anonymized_case_template.md": ANON_CASE,
        "before_after_workflow_template.md": BEFORE_AFTER,
        "proof_permission_checklist.md": PERMISSION,
    }
    for name, content in files.items():
        write_text(out_dir / name, content)
    return {"out_dir": str(out_dir), "files": list(files)}


def main() -> int:
    result = generate()
    print(f"[proof_asset] templates → {result['out_dir']}")
    print(f"[proof_asset] {SAFETY_BANNER}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
