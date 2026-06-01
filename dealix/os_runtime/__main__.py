"""
__main__.py — CLI entry point for dealix.os_runtime

Usage:
    python -m dealix.os_runtime validate
    python -m dealix.os_runtime score-company
    python -m dealix.os_runtime route-offer
    python -m dealix.os_runtime approval-check
    python -m dealix.os_runtime daily-brief
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="dealix-os-runtime",
    help="Dealix OS Runtime CLI — validate configs, score companies, route offers",
    add_completion=False,
)
console = Console()

# ---------------------------------------------------------------------------
# Lazy imports to avoid heavy startup cost when not needed
# ---------------------------------------------------------------------------


def _get_loader():
    from dealix.os_runtime.config_loader import OSConfigLoader

    loader = OSConfigLoader()
    loader.load_all()
    return loader


def _get_validator():
    from dealix.os_runtime.validator import OSValidator

    return OSValidator()


def _run_validation():
    """Run validation and return (passed, errors, warnings)."""
    validator = _get_validator()
    result = validator.validate()
    return result.is_valid, result.errors, result.warnings


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


@app.command("validate")
def validate_cmd(
    strict: bool = typer.Option(False, "--strict", help="Fail on warnings too"),
) -> None:
    """Validate all OS configs and report errors/warnings."""
    console.print("[bold blue]Dealix OS Runtime — Validation[/bold blue]")
    passed, errors, warnings = _run_validation()

    # Errors table
    if errors:
        table = Table(title="Errors", style="red")
        table.add_column("#")
        table.add_column("Error")
        for i, err in enumerate(errors, 1):
            table.add_row(str(i), err)
        console.print(table)

    # Warnings table
    if warnings:
        table = Table(title="Warnings", style="yellow")
        table.add_column("#")
        table.add_column("Warning")
        for i, warn in enumerate(warnings, 1):
            table.add_row(str(i), warn)
        console.print(table)

    if passed and (not strict or not warnings):
        console.print(
            f"[bold green]PASSED[/bold green] — "
            f"{len(errors)} errors, "
            f"{len(warnings)} warnings"
        )
    else:
        console.print(
            f"[bold red]FAILED[/bold red] — "
            f"{len(errors)} errors, "
            f"{len(warnings)} warnings"
        )
        raise typer.Exit(code=1)


@app.command("score-company")
def score_company_cmd(
    company: str = typer.Option(..., "--company", "-c", help="Company name"),
    operations_complexity: str = typer.Option(
        "medium", help="high|medium|low|none"
    ),
    reporting_burden: str = typer.Option("medium", help="high|medium|low"),
    maintenance_field_ops: str = typer.Option(
        "partial", help="yes|partial|no"
    ),
    multi_branch: str = typer.Option("some", help="many|some|one"),
    output_format: str = typer.Option("table", "--format", help="table|json"),
) -> None:
    """Score a company against the Dealix scoring dimensions."""
    console.print(
        f"[bold blue]Scoring company:[/bold blue] {company}"
    )

    loader = _get_loader()
    signals = {
        "operations_complexity": operations_complexity,
        "reporting_burden": reporting_burden,
        "maintenance_or_field_ops": maintenance_field_ops,
        "multi_branch_or_scale": multi_branch,
    }
    result = loader.score_company(signals)
    result["company_name"] = company

    if output_format == "json":
        console.print_json(json.dumps(result, ensure_ascii=False, indent=2))
        return

    table = Table(title=f"Scoring: {company}")
    table.add_column("Dimension")
    table.add_column("Score")
    table.add_column("Level")
    table.add_column("Max")

    for dim in result.get("dimension_scores", []):
        table.add_row(
            dim["dimension_id"],
            str(dim["score"]),
            dim["level"],
            str(dim["max"]),
        )

    console.print(table)
    console.print(f"[bold]Total Score:[/bold] {result['total_score']}/100")
    console.print(f"[bold]Tier:[/bold] {result['tier']}")
    console.print(f"[bold]Recommended Offer:[/bold] {result['recommended_offer']}")
    console.print(f"[bold]Next Action:[/bold] {result['next_action']}")


@app.command("route-offer")
def route_offer_cmd(
    company: str = typer.Option(..., "--company", "-c", help="Company name"),
    sector: str = typer.Option(..., "--sector", "-s", help="Industry sector"),
    score: float = typer.Option(70.0, "--score", help="Company score (0-100)"),
    country: str = typer.Option("SA", "--country", help="Country code"),
    output_format: str = typer.Option("table", "--format", help="table|json"),
) -> None:
    """Route a company to the best offer and channel."""
    console.print(
        f"[bold blue]Routing offer for:[/bold blue] {company} ({sector})"
    )

    loader = _get_loader()
    profile = {
        "company": company,
        "sector": sector,
        "score": score,
        "country": country,
    }
    result = loader.route_offer(profile)

    if output_format == "json":
        console.print_json(json.dumps(result, ensure_ascii=False, indent=2))
        return

    console.print(f"[bold]Best Offer:[/bold] {result['best_offer']}")
    console.print(f"[bold]Best Channel:[/bold] {result['best_channel']}")
    console.print(
        f"[bold]Requires Approval:[/bold] {result['requires_approval']}"
    )
    console.print(f"[dim]Reasoning:[/dim] {result['reasoning']}")


@app.command("approval-check")
def approval_check_cmd(
    draft_id: str = typer.Option(
        None, "--draft-id", help="Draft ID to check approval status for"
    ),
    gate_id: str = typer.Option(
        None, "--gate-id", help="Gate ID to look up (e.g. G01)"
    ),
) -> None:
    """Check approval requirements for a draft or gate."""
    loader = _get_loader()

    if gate_id:
        gates = loader.approval_gates
        found = None
        for key, val in gates.items():
            if isinstance(val, dict) and val.get("id") == gate_id:
                found = val
                break
        if found:
            console.print(f"[bold]Gate {gate_id}:[/bold] {found.get('name')}")
            console.print(
                f"[bold]Requires Approval:[/bold] "
                f"{found.get('requires_human_approval')}"
            )
            console.print(f"[bold]Reason:[/bold] {found.get('reason', '')}")
        else:
            console.print(f"[red]Gate '{gate_id}' not found[/red]")
        return

    if draft_id:
        console.print(
            f"[bold]Draft {draft_id}:[/bold] "
            f"Requires founder approval before any send."
        )
        console.print(
            "[yellow]No live sends permitted — "
            "present to founder via Daily Brief.[/yellow]"
        )
        return

    console.print(
        "[yellow]Provide --draft-id or --gate-id to check approval status.[/yellow]"
    )


@app.command("daily-brief")
def daily_brief_cmd(
    output_format: str = typer.Option(
        "markdown", "--format", help="markdown|json"
    ),
    output_file: str = typer.Option(
        None, "--output", "-o", help="Write to file"
    ),
) -> None:
    """Generate and print the founder daily growth brief."""
    # Delegate to founder_growth_daily_report.py
    try:
        scripts_dir = Path(__file__).resolve().parent.parent.parent / "scripts"
        sys.path.insert(0, str(scripts_dir.parent))

        from scripts.founder_growth_daily_report import (  # type: ignore[import]
            generate_report,
            render_json,
            render_markdown,
        )

        report = generate_report()
        if output_format == "json":
            content = render_json(report)
        else:
            content = render_markdown(report)

        console.print(content)

        if output_file:
            Path(output_file).write_text(content, encoding="utf-8")
            console.print(f"\n[dim]Written to {output_file}[/dim]")

    except ImportError as exc:
        console.print(f"[red]Could not import daily report module: {exc}[/red]")
        raise typer.Exit(code=1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
