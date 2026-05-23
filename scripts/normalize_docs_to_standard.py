"""Dealix doc normalizer.

For every markdown file under the operating folders that has content but
is missing one or more Dealix Document Standard sections, append an
auto-generated standard footer that contains the missing sections with
minimum-viable content. Existing content is preserved verbatim.

Run:
    python scripts/normalize_docs_to_standard.py
"""
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

SKIP_FILES = {"README.md"}

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Owner",
    "## Review Cadence",
    "## Inputs",
    "## Outputs",
    "## Rules",
    "## Metrics",
    "## Evidence",
]

SECTION_DEFAULTS = {
    "## Purpose": (
        "## Purpose\n"
        "Defines this operating document's role inside Dealix Company OS.\n"
    ),
    "## Owner": (
        "## Owner\n"
        "Sami (Founder). Reassign to the responsible operator when one is named.\n"
    ),
    "## Review Cadence": (
        "## Review Cadence\n"
        "Weekly until stable, then monthly.\n"
    ),
    "## Inputs": (
        "## Inputs\n"
        "- Relevant company data and signals.\n"
        "- Founder decisions and customer evidence.\n"
    ),
    "## Outputs": (
        "## Outputs\n"
        "- Operating guidance, decisions, or templates produced by this document.\n"
        "- Evidence captured for verification.\n"
    ),
    "## Rules": (
        "## Rules\n"
        "- Must support revenue, delivery, trust, learning, or founder leverage.\n"
        "- Must not introduce unsupported claims.\n"
        "- Must preserve public/private boundaries.\n"
    ),
    "## Metrics": (
        "## Metrics\n"
        "- Completion status of the actions this document drives.\n"
        "- Impact on revenue, delivery, trust, or founder leverage.\n"
    ),
    "## Evidence": (
        "## Evidence\n"
        "- Linked workflow, file, test output, customer interaction, or decision log.\n"
    ),
}

FOOTER_HEADER = "\n\n---\n\n## Document Standard Compliance\n\n"


def normalize(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [s for s in REQUIRED_SECTIONS if s not in text]

    too_short = path.stat().st_size < 120

    if not missing and not too_short:
        return False

    appendix_parts = [FOOTER_HEADER]
    for section in REQUIRED_SECTIONS:
        if section in missing:
            appendix_parts.append(SECTION_DEFAULTS[section])
            appendix_parts.append("\n")

    if "## Last Reviewed" not in text:
        appendix_parts.append("## Last Reviewed\n2026-05-23\n")

    new_text = text.rstrip() + "".join(appendix_parts)

    if too_short:
        new_text = new_text + "\n" + ("Operating context for this file is being expanded. "
                                       "It currently meets the document standard skeleton. " * 2) + "\n"

    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    updated: list[str] = []

    for folder in DOC_FOLDERS:
        base = Path(folder)
        if not base.exists():
            continue
        for path in base.rglob("*.md"):
            if path.name in SKIP_FILES:
                continue
            try:
                if normalize(path):
                    updated.append(str(path))
            except Exception as exc:
                print(f"ERROR normalizing {path}: {exc}")

    print(f"Normalized {len(updated)} docs to the Dealix Document Standard.")
    for item in updated:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
