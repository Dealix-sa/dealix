#!/usr/bin/env python3
"""Dealix Design OS automation suite.

Adds practical operations around the draft-only Design Command Room generator:

- validate generated artifacts
- build a markdown index of artifacts
- render a simple safe HTML preview from markdown
- generate a daily operating pack across all core Dealix surfaces

The suite is dependency-free and does not send externally, alter production UI,
or mark any artifact as approved.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    import design_command_room
except ModuleNotFoundError:  # pragma: no cover - defensive path for direct imports
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import design_command_room

DEFAULT_REPORT_DIR = Path("reports/design")
REQUIRED_FIELDS = {
    "artifact_key",
    "title",
    "generated_at",
    "business_goal",
    "primary_user",
    "source_context",
    "generated_by",
    "approval_state",
    "safety_status",
    "handoff_target",
    "sections",
    "risks",
    "next_actions",
    "live_sends",
}
BLOCKED_APPROVAL_STATES = {"approved_for_client", "approved_for_production"}


@dataclass(frozen=True)
class ValidationFinding:
    severity: str
    code: str
    message: str

    def as_markdown(self) -> str:
        return f"- **{self.severity}** `{self.code}` — {self.message}"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_json_files(report_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in report_dir.glob("*.json")
        if path.name != "latest.json" and path.is_file()
    )


def validate_artifact(data: dict[str, Any]) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    missing = sorted(REQUIRED_FIELDS - set(data))
    if missing:
        findings.append(
            ValidationFinding("error", "missing_fields", f"Missing fields: {', '.join(missing)}")
        )
    if data.get("live_sends") != 0:
        findings.append(
            ValidationFinding("error", "live_sends", "Design artifacts must keep live_sends=0.")
        )
    approval_state = str(data.get("approval_state", "")).strip().lower()
    if approval_state in BLOCKED_APPROVAL_STATES:
        findings.append(
            ValidationFinding(
                "error",
                "unreviewed_approval_state",
                f"Generated artifact cannot be {approval_state!r} by default.",
            )
        )
    if not str(data.get("safety_status", "")).strip():
        findings.append(ValidationFinding("error", "missing_safety_status", "Missing safety status."))
    sections = data.get("sections")
    if not isinstance(sections, list) or not sections:
        findings.append(ValidationFinding("error", "missing_sections", "Artifact has no sections."))
    text_blob = json.dumps(data, ensure_ascii=False).lower()
    blocked_claims = design_command_room.review_claims(text_blob)
    if blocked_claims:
        findings.append(
            ValidationFinding(
                "warning",
                "blocked_claim_terms",
                "Potential risky claim terms found: " + ", ".join(blocked_claims),
            )
        )
    return findings


def validate_report_dir(report_dir: Path) -> tuple[list[ValidationFinding], list[Path]]:
    findings: list[ValidationFinding] = []
    files = artifact_json_files(report_dir)
    latest = report_dir / "latest.json"
    if latest.exists():
        files = [latest, *files]
    if not files:
        findings.append(
            ValidationFinding(
                "warning",
                "no_artifacts",
                f"No generated artifact JSON files found under {report_dir}.",
            )
        )
        return findings, files
    for path in files:
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            findings.append(ValidationFinding("error", "invalid_json", f"{path}: {exc}"))
            continue
        for finding in validate_artifact(data):
            findings.append(
                ValidationFinding(finding.severity, finding.code, f"{path}: {finding.message}")
            )
    return findings, files


def render_validation_report(report_dir: Path, findings: list[ValidationFinding], files: list[Path]) -> str:
    errors = sum(1 for finding in findings if finding.severity == "error")
    warnings = sum(1 for finding in findings if finding.severity == "warning")
    status = "pass" if errors == 0 else "fail"
    lines = [
        "# Dealix Design OS Validation Report",
        "",
        "```text",
        f"Generated at: {datetime.now(UTC).isoformat()}",
        f"Report dir: {report_dir}",
        f"Artifacts checked: {len(files)}",
        f"Status: {status}",
        f"Errors: {errors}",
        f"Warnings: {warnings}",
        "```",
        "",
        "## Findings",
        "",
    ]
    if findings:
        lines.extend(finding.as_markdown() for finding in findings)
    else:
        lines.append("- No validation findings.")
    lines.extend(
        [
            "",
            "## Safety Reminder",
            "",
            "Generated design artifacts remain draft-only until reviewed. Do not treat validation as client or production approval.",
        ]
    )
    return "\n".join(lines) + "\n"


def command_validate(args: argparse.Namespace) -> int:
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    findings, files = validate_report_dir(report_dir)
    markdown = render_validation_report(report_dir, findings, files)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    print(f"validation report: {output}")
    return 1 if any(finding.severity == "error" for finding in findings) else 0


def build_index(report_dir: Path) -> str:
    files = artifact_json_files(report_dir)
    lines = [
        "# Dealix Design OS Artifact Index",
        "",
        "```text",
        f"Generated at: {datetime.now(UTC).isoformat()}",
        f"Report dir: {report_dir}",
        f"Artifacts indexed: {len(files)}",
        "```",
        "",
        "| Artifact | Title | Approval | Safety | Handoff | Generated |",
        "|---|---|---|---|---|---|",
    ]
    for path in files:
        try:
            data = load_json(path)
        except json.JSONDecodeError:
            continue
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{data.get('artifact_key', path.stem)}`",
                    str(data.get("title", "")),
                    str(data.get("approval_state", "")),
                    str(data.get("safety_status", "")),
                    str(data.get("handoff_target", "")),
                    str(data.get("generated_at", "")),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Next Review Actions",
            "",
            "- Review `latest.md` first.",
            "- Run `make design-os-validate` before any client or production use.",
            "- Promote only after claims, safety, and owner review.",
        ]
    )
    return "\n".join(lines) + "\n"


def command_index(args: argparse.Namespace) -> int:
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_index(report_dir), encoding="utf-8")
    print(f"artifact index: {output}")
    return 0


def markdown_to_html(markdown: str, title: str) -> str:
    body_lines: list[str] = []
    in_code = False
    for line in markdown.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                body_lines.append("</pre>")
                in_code = False
            else:
                body_lines.append("<pre>")
                in_code = True
            continue
        escaped = html.escape(line)
        if in_code:
            body_lines.append(escaped)
        elif stripped.startswith("# "):
            body_lines.append(f"<h1>{html.escape(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            body_lines.append(f"<h2>{html.escape(stripped[3:])}</h2>")
        elif stripped.startswith("- "):
            body_lines.append(f"<p class='bullet'>• {html.escape(stripped[2:])}</p>")
        elif not stripped:
            body_lines.append("<br />")
        else:
            body_lines.append(f"<p>{escaped}</p>")
    if in_code:
        body_lines.append("</pre>")
    body = "\n".join(body_lines)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #0f172a; color: #e5e7eb; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 48px 24px; }}
    h1 {{ font-size: 40px; line-height: 1.05; margin: 0 0 24px; }}
    h2 {{ margin-top: 36px; padding-top: 20px; border-top: 1px solid rgba(148, 163, 184, .28); }}
    p {{ color: #cbd5e1; line-height: 1.65; }}
    pre {{ white-space: pre-wrap; background: rgba(15, 23, 42, .9); border: 1px solid rgba(148, 163, 184, .35); border-radius: 16px; padding: 18px; color: #f8fafc; overflow: auto; }}
    .bullet {{ padding-left: 10px; }}
    .banner {{ background: rgba(34, 197, 94, .12); border: 1px solid rgba(34, 197, 94, .35); color: #bbf7d0; padding: 14px 16px; border-radius: 14px; margin-bottom: 28px; }}
  </style>
</head>
<body>
  <main>
    <div class="banner">Dealix Design OS Preview — draft only, not approved for client or production use.</div>
    {body}
  </main>
</body>
</html>
"""


def command_html(args: argparse.Namespace) -> int:
    source = Path(args.input)
    if not source.exists():
        print(f"missing input markdown: {source}", file=sys.stderr)
        return 1
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown = source.read_text(encoding="utf-8")
    title = source.stem.replace("-", " ").title()
    output.write_text(markdown_to_html(markdown, title), encoding="utf-8")
    print(f"html preview: {output}")
    return 0


def command_daily_pack(args: argparse.Namespace) -> int:
    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    generated = design_command_room.generate_all(args.context, report_dir)
    index_path = report_dir / "INDEX.md"
    validation_path = report_dir / "VALIDATION.md"
    html_path = report_dir / "latest.html"
    index_path.write_text(build_index(report_dir), encoding="utf-8")
    findings, files = validate_report_dir(report_dir)
    validation_path.write_text(render_validation_report(report_dir, findings, files), encoding="utf-8")
    latest_md = report_dir / "latest.md"
    if latest_md.exists():
        html_path.write_text(markdown_to_html(latest_md.read_text(encoding="utf-8"), "Dealix Design OS Latest"), encoding="utf-8")
    print(f"generated artifacts: {len(generated)}")
    print(f"artifact index: {index_path}")
    print(f"validation report: {validation_path}")
    print(f"html preview: {html_path}")
    return 1 if any(finding.severity == "error" for finding in findings) else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Operate Dealix Design OS artifacts.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate generated artifacts.")
    validate.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR))
    validate.add_argument("--output", default=str(DEFAULT_REPORT_DIR / "VALIDATION.md"))
    validate.set_defaults(func=command_validate)

    index = subparsers.add_parser("index", help="Build artifact index.")
    index.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR))
    index.add_argument("--output", default=str(DEFAULT_REPORT_DIR / "INDEX.md"))
    index.set_defaults(func=command_index)

    preview = subparsers.add_parser("html", help="Render latest markdown artifact to HTML preview.")
    preview.add_argument("--input", default=str(DEFAULT_REPORT_DIR / "latest.md"))
    preview.add_argument("--output", default=str(DEFAULT_REPORT_DIR / "latest.html"))
    preview.set_defaults(func=command_html)

    daily = subparsers.add_parser("daily-pack", help="Generate all artifacts, index, validation, and HTML preview.")
    daily.add_argument("--context", default="Dealix daily operating cycle.")
    daily.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR))
    daily.set_defaults(func=command_daily_pack)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
