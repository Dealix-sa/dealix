"""Fill empty operating-document files with the Dealix document-standard
template, so every file that exists at least carries the minimum
viable operating structure.

This is a local utility: run it before committing if you have created
empty placeholder files. It only touches files whose size is exactly 0
bytes — it never overwrites content.

Intended workflow:
1. Create the folder skeleton you want.
2. ``touch`` the placeholder files you want filled.
3. Run ``python scripts/fill_empty_docs_with_standard.py``.
4. Run ``python scripts/verify_document_quality.py`` and fix the rest
   by hand.
"""

from __future__ import annotations

from pathlib import Path

DOC_FOLDERS = [
    "docs/founder",
    "docs/learning",
    "docs/delivery/revenue_sprint",
    "docs/ops",
    "docs/revenue",
    "docs/trust",
]

TEMPLATE = """# {title}

## Purpose
Define the operating role of this document inside the Dealix Company OS.

## Owner
Sami (Founder).

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant operating signals.
- Founder direction.
- Customer evidence where applicable.

## Outputs
- Clear operating guidance.
- Decisions, rules, or templates.
- Evidence required for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.
- Must be updated when repeated issues appear.

## Metrics
- Completion status.
- Usage frequency.
- Impact on revenue, delivery, trust, or founder leverage.
- Number of decisions or actions supported.

## Evidence
- Linked file, workflow, test output, customer feedback, payment,
  delivery, or decision log.

## Last Reviewed
YYYY-MM-DD
"""


def title_from_path(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").title()


def main() -> None:
    updated: list[str] = []

    for folder in DOC_FOLDERS:
        base = Path(folder)
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            if path.stat().st_size == 0:
                path.write_text(
                    TEMPLATE.format(title=title_from_path(path)),
                    encoding="utf-8",
                )
                updated.append(str(path))

    print(f"Updated {len(updated)} empty docs.")
    for item in updated:
        print(f"- {item}")


if __name__ == "__main__":
    main()
