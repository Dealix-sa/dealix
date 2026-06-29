#!/usr/bin/env python3
"""Dealix Design Command Room generator.

This module turns the Dealix design contract into practical draft artifacts for
revenue, founder, delivery, proof-pack, sales, landing-page, and growth work.

It is intentionally dependency-free and draft-only. It never sends externally,
never changes production routes, and never marks generated artifacts as approved.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from textwrap import dedent

DEFAULT_OUTPUT_DIR = Path("reports/design")
LATEST_MARKDOWN = DEFAULT_OUTPUT_DIR / "latest.md"
LATEST_JSON = DEFAULT_OUTPUT_DIR / "latest.json"

SAFE_ENV_DEFAULTS = {
    "EXTERNAL_SEND_ENABLED": "false",
    "EMAIL_SEND_ENABLED": "false",
    "WHATSAPP_SEND_ENABLED": "false",
    "WHATSAPP_ALLOW_LIVE_SEND": "false",
    "SMS_SEND_ENABLED": "false",
    "OUTBOUND_MODE": "draft_only",
}

BLOCKED_CLAIMS = [
    "guaranteed revenue",
    "guaranteed roi",
    "fake testimonial",
    "fake client",
    "fake logo",
    "official partner",
    "live outbound enabled",
]


@dataclass(frozen=True)
class ArtifactTemplate:
    """A Dealix design artifact template."""

    key: str
    title: str
    business_goal: str
    primary_user: str
    handoff_target: str
    sections: tuple[str, ...]
    required_states: tuple[str, ...] = (
        "draft",
        "needs_review",
        "approved_for_demo",
        "approved_for_client",
        "approved_for_production",
        "rejected",
    )
    safety_checks: tuple[str, ...] = (
        "No fake ROI or guaranteed revenue claim",
        "No fake testimonial, logo, customer, or case study",
        "Assumptions labeled before client use",
        "No live outbound implication unless gates exist",
        "Human approval required before production or client handoff",
    )


@dataclass
class DesignArtifact:
    """Rendered Dealix artifact metadata and body."""

    artifact_key: str
    title: str
    generated_at: str
    business_goal: str
    primary_user: str
    source_context: str
    generated_by: str
    approval_state: str
    safety_status: str
    handoff_target: str
    sections: list[dict[str, str]] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    next_actions: list[str] = field(default_factory=list)
    live_sends: int = 0


TEMPLATES: dict[str, ArtifactTemplate] = {
    "revenue-command-room": ArtifactTemplate(
        key="revenue-command-room",
        title="Revenue Command Room V0",
        business_goal="Give the founder/operator one daily screen for targets, follow-ups, proposals, approvals, and next actions.",
        primary_user="Founder, sales operator, or Dealix operator",
        handoff_target="html_preview",
        sections=(
            "Today's Revenue Focus",
            "Target Account Queue",
            "Follow-up Queue",
            "Proposal Queue",
            "Approval Cards",
            "Trust and Outbound Status",
            "Next 10 Actions",
            "Risks and Blockers",
        ),
    ),
    "founder-war-room": ArtifactTemplate(
        key="founder-war-room",
        title="Founder War Room V0",
        business_goal="Show the most important operating decisions of the day across revenue, delivery, product, and trust.",
        primary_user="Founder / CEO",
        handoff_target="internal_review",
        sections=(
            "What Changed Today",
            "Highest-value Decision",
            "Revenue Pressure",
            "Delivery Pressure",
            "Trust and Safety Risk",
            "Product or Engineering Blocker",
            "Recommended Action",
            "Review Date",
        ),
    ),
    "client-proof-pack": ArtifactTemplate(
        key="client-proof-pack",
        title="Client Proof Pack V0",
        business_goal="Show what Dealix diagnosed, prepared, reviewed, validated, and recommends next for a client.",
        primary_user="Client decision maker or transformation owner",
        handoff_target="client_review",
        sections=(
            "Client Context",
            "Current Workflow Pain",
            "What Dealix Prepared",
            "What Was Reviewed",
            "What Was Validated",
            "Before / After Workflow Map",
            "Risks and Assumptions",
            "Next 30 Days",
            "Approval and Handoff",
        ),
    ),
    "sales-deck": ArtifactTemplate(
        key="sales-deck",
        title="Dealix Sales Deck V0",
        business_goal="Explain the outcome, method, pilot scope, proof plan, and next step for a qualified prospect.",
        primary_user="Prospect founder, sales leader, or operations leader",
        handoff_target="pdf_export",
        sections=(
            "Client Pain",
            "Why Now",
            "What Dealix Does",
            "Proposed Operating System",
            "Before / After Workflow",
            "Pilot Scope",
            "Implementation Timeline",
            "Proof Pack and Review Cadence",
            "Commercial Model",
            "Next Step",
        ),
    ),
    "landing-page": ArtifactTemplate(
        key="landing-page",
        title="Dealix Landing Page V0",
        business_goal="Convert qualified Saudi B2B prospects into a discovery or focused pilot conversation.",
        primary_user="Saudi B2B prospect",
        handoff_target="web_preview",
        sections=(
            "Hero Outcome",
            "Pain Narrative",
            "Dealix Offer",
            "Product Surfaces",
            "Trust and Safety",
            "Pilot Model",
            "Call to Action",
        ),
    ),
    "client-growth": ArtifactTemplate(
        key="client-growth",
        title="Client Growth Operator Artifact V0",
        business_goal="Prepare reviewed multi-channel growth action cards for a client without uncontrolled live outbound.",
        primary_user="Client growth owner or Dealix operator",
        handoff_target="internal_review",
        sections=(
            "Client Operating Profile",
            "Target Segments",
            "Channel Action Cards",
            "Reply Classification",
            "Approval Queue",
            "Trust Gates",
            "Next Follow-up Dates",
        ),
    ),
    "delivery-os": ArtifactTemplate(
        key="delivery-os",
        title="Client Delivery OS Artifact V0",
        business_goal="Move a client engagement from intake to diagnosis, scope, blueprint, validation, and proof pack.",
        primary_user="Dealix delivery owner or client operations lead",
        handoff_target="client_review",
        sections=(
            "Intake Summary",
            "Diagnosis",
            "Scope Card",
            "Workflow Blueprint",
            "Acceptance Criteria",
            "Proof Pack Plan",
            "Next 30 Days",
        ),
    ),
    "company-brain": ArtifactTemplate(
        key="company-brain",
        title="Company Brain Design Artifact V0",
        business_goal="Turn operating signals into a decision-ready executive artifact.",
        primary_user="Founder / CEO / executive operator",
        handoff_target="internal_review",
        sections=(
            "Signal Summary",
            "Decision Queue",
            "Why Now",
            "Expected Impact",
            "Risk if Ignored",
            "Recommended Action",
            "Success Metric",
        ),
    ),
}


def normalize_key(value: str) -> str:
    return value.strip().lower().replace("_", "-")


def env_safety_status() -> tuple[str, list[str]]:
    problems: list[str] = []
    for key, expected in SAFE_ENV_DEFAULTS.items():
        current = os.getenv(key, expected).strip().lower()
        if current != expected:
            problems.append(f"{key}={current!r} expected {expected!r}")
    status = "safe_draft_only" if not problems else "needs_review_env_mismatch"
    return status, problems


def review_claims(text: str) -> list[str]:
    lowered = text.lower()
    return [claim for claim in BLOCKED_CLAIMS if claim in lowered]


def section_body(template: ArtifactTemplate, section: str, source_context: str) -> str:
    if section.lower().startswith("trust"):
        return (
            "Live outbound remains draft-only by default. Show email opt-out status, "
            "WhatsApp opt-in/template status, LinkedIn manual-only status, and source verification."
        )
    if "approval" in section.lower():
        return "Use visible approval states: Draft, Needs Review, Approved, Blocked, Rejected."
    if "next" in section.lower():
        return "List specific next actions with owner, date, source, and review status."
    if "risk" in section.lower() or "blocker" in section.lower():
        return "Label assumptions, missing proof, operational blockers, and decision risks."
    if "proof" in section.lower() or "validated" in section.lower():
        return "Separate generated outputs from verified evidence. Do not claim results without proof."
    return f"Draft this section from the source context: {source_context}"


def build_artifact(template: ArtifactTemplate, source_context: str) -> DesignArtifact:
    safety_status, env_problems = env_safety_status()
    sections = [
        {"title": section, "body": section_body(template, section, source_context)}
        for section in template.sections
    ]
    risks = [
        "Artifact is draft-only until reviewed.",
        "Claims must be source-backed or labeled as assumptions.",
        *env_problems,
    ]
    next_actions = [
        "Review artifact against docs/design/DEALIX_DESIGN.md.",
        "Run claims review before client or production use.",
        "Choose handoff target and owner.",
        "Promote only after approval state changes from draft.",
    ]
    return DesignArtifact(
        artifact_key=template.key,
        title=template.title,
        generated_at=datetime.now(UTC).isoformat(),
        business_goal=template.business_goal,
        primary_user=template.primary_user,
        source_context=source_context,
        generated_by="scripts/design_command_room.py",
        approval_state="draft",
        safety_status=safety_status,
        handoff_target=template.handoff_target,
        sections=sections,
        risks=risks,
        next_actions=next_actions,
        live_sends=0,
    )


def render_markdown(artifact: DesignArtifact) -> str:
    section_markdown = "\n\n".join(
        f"## {section['title']}\n\n{section['body']}" for section in artifact.sections
    )
    risks = "\n".join(f"- {risk}" for risk in artifact.risks)
    next_actions = "\n".join(f"- {action}" for action in artifact.next_actions)
    return dedent(
        f"""
        # {artifact.title}

        ```text
        Artifact: {artifact.artifact_key}
        Business goal: {artifact.business_goal}
        Primary user: {artifact.primary_user}
        Source context: {artifact.source_context}
        Generated by: {artifact.generated_by}
        Generated at: {artifact.generated_at}
        Approval state: {artifact.approval_state}
        Safety status: {artifact.safety_status}
        Handoff target: {artifact.handoff_target}
        Live sends: {artifact.live_sends}
        ```

        {section_markdown}

        ## Risks and Assumptions

        {risks}

        ## Next Actions

        {next_actions}

        ## Claims Review

        ```text
        Claims reviewed: pending
        Proof available: pending
        Assumptions labeled: required
        External-send implication checked: required
        Approved by: pending
        Date: pending
        ```
        """
    ).strip() + "\n"


def write_artifact(artifact: DesignArtifact, output_dir: Path = DEFAULT_OUTPUT_DIR) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    markdown_path = output_dir / f"{artifact.artifact_key}-{timestamp}.md"
    json_path = output_dir / f"{artifact.artifact_key}-{timestamp}.json"
    markdown = render_markdown(artifact)
    blocked = review_claims(markdown)
    if blocked:
        artifact.risks.append("Blocked claims detected: " + ", ".join(blocked))
        artifact.safety_status = "needs_review_blocked_claims"
        markdown = render_markdown(artifact)
    markdown_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(json.dumps(asdict(artifact), ensure_ascii=False, indent=2), encoding="utf-8")
    LATEST_MARKDOWN.write_text(markdown, encoding="utf-8")
    LATEST_JSON.write_text(json.dumps(asdict(artifact), ensure_ascii=False, indent=2), encoding="utf-8")
    return markdown_path, json_path


def list_templates() -> str:
    rows = ["# Dealix Design Command Room Templates", ""]
    for template in TEMPLATES.values():
        rows.append(f"- `{template.key}` — {template.title}: {template.business_goal}")
    return "\n".join(rows) + "\n"


def generate_all(source_context: str, output_dir: Path = DEFAULT_OUTPUT_DIR) -> list[tuple[Path, Path]]:
    results = []
    for template in TEMPLATES.values():
        results.append(write_artifact(build_artifact(template, source_context), output_dir))
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate Dealix draft design artifacts.")
    parser.add_argument(
        "--type",
        default="revenue-command-room",
        help="Artifact type or 'all'. Use --list to see options.",
    )
    parser.add_argument(
        "--context",
        default="Dealix operating system launch and commercial command room.",
        help="Source context used to draft the artifact.",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for generated artifacts.",
    )
    parser.add_argument("--list", action="store_true", help="List available templates.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.list:
        print(list_templates())
        return 0

    output_dir = Path(args.output_dir)
    artifact_type = normalize_key(args.type)
    if artifact_type == "all":
        generated = generate_all(args.context, output_dir)
        for markdown_path, json_path in generated:
            print(f"generated: {markdown_path} | {json_path}")
        return 0

    template = TEMPLATES.get(artifact_type)
    if template is None:
        parser.error(f"Unknown artifact type {args.type!r}. Use --list to see options.")

    artifact = build_artifact(template, args.context)
    markdown_path, json_path = write_artifact(artifact, output_dir)
    print(f"generated: {markdown_path}")
    print(f"generated: {json_path}")
    print(f"latest: {LATEST_MARKDOWN}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
