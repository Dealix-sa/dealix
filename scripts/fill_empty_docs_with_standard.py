from pathlib import Path

DOC_FOLDERS = [
    "docs/founder",
    "docs/strategy",
    "docs/revenue",
    "docs/acquisition",
    "docs/sales",
    "docs/offers",
    "docs/delivery",
    "docs/trust",
    "docs/finance",
    "docs/client_success",
    "docs/product",
    "docs/content",
    "docs/learning",
    "docs/people",
    "docs/agents",
    "docs/ai_management",
    "docs/control_plane",
    "docs/ops",
    "docs/partners",
    "docs/investor",
    "docs/brand",
    "docs/api",
    "docs/deployment",
]

def title_from_path(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").title()

TEMPLATE = """# {title}

## Purpose
Define the operating role of this document inside Dealix Company OS.

## Owner
Sami / Current system owner.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data.
- Operating signals.
- Founder decisions.
- Customer evidence where applicable.

## Outputs
- Clear operating guidance.
- Decisions, rules, or templates.
- Evidence needed for verification.

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
- Linked file, workflow, test output, customer feedback, payment, delivery, or decision log.

## Last Reviewed
YYYY-MM-DD
"""

updated = []

for folder in DOC_FOLDERS:
    base = Path(folder)
    if not base.exists():
        continue

    for path in base.rglob("*.md"):
        if path.stat().st_size == 0:
            path.write_text(TEMPLATE.format(title=title_from_path(path)), encoding="utf-8")
            updated.append(str(path))

print(f"Updated {len(updated)} empty docs.")
for item in updated:
    print(f"- {item}")
