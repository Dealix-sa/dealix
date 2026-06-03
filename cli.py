"""
Interactive CLI — uses Typer + Rich for a nice bilingual console experience.
واجهة سطر أوامر تفاعلية.

Usage:
    python cli.py               # interactive menu
    python cli.py status        # check app status
    python cli.py sector healthcare
    python cli.py demo          # run end-to-end demo
"""

from __future__ import annotations

import asyncio
import re
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from auto_client_acquisition.agents.intake import LeadSource
from auto_client_acquisition.pipeline import AcquisitionPipeline
from autonomous_growth.agents.sector_intel import SaudiSector, SectorIntelAgent
from core.config.settings import get_settings
from core.llm import get_router
from core.prompts.sales_scripts import get_sales_script

app = typer.Typer(help="🏢 AI Company Saudi — CLI")
console = Console()


def _banner() -> None:
    settings = get_settings()
    console.print(
        Panel.fit(
            f"[bold cyan]🏢 {settings.app_name}[/bold cyan]\n"
            f"[dim]v{settings.app_version} · {settings.app_env}[/dim]",
            border_style="cyan",
        )
    )


# ── Commands ───────────────────────────────────────────────────
@app.command()
def status() -> None:
    """Show app status + configured LLM providers."""
    _banner()
    router = get_router()
    providers = router.available_providers()

    table = Table(title="LLM Providers", show_lines=True)
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="green")
    for provider in providers:
        table.add_row(provider.value, "✅ configured")
    if not providers:
        table.add_row("(none)", "[red]⚠️  no providers configured[/red]")
    console.print(table)


@app.command()
def sector(
    name: Annotated[str, typer.Argument(help="Sector name, e.g. healthcare")],
    enrich: Annotated[bool, typer.Option("--enrich", "-e")] = False,
) -> None:
    """Show intel for a Saudi sector."""
    _banner()
    try:
        sector_enum = SaudiSector(name)
    except ValueError:
        console.print(f"[red]Unknown sector: {name}[/red]")
        console.print(f"Available: {', '.join(s.value for s in SaudiSector)}")
        raise typer.Exit(code=1)

    agent = SectorIntelAgent()
    intel = asyncio.run(agent.run(sector=sector_enum, enrich_with_llm=enrich))

    table = Table(title=f"Sector: {intel.sector.value}", show_lines=True)
    table.add_column("Field", style="cyan")
    table.add_column("Value")
    table.add_row("Market size", f"{intel.market_size_sar:,.0f} SAR")
    table.add_row("Growth rate", f"{intel.growth_rate:.1%}")
    table.add_row("AI readiness", f"{intel.ai_readiness:.0%}")
    table.add_row("Key players", ", ".join(intel.key_players[:5]) or "—")
    table.add_row("Pain points", "\n".join(f"• {p}" for p in intel.pain_points[:5]))
    table.add_row("Opportunities", "\n".join(f"• {o}" for o in intel.opportunities[:5]))
    table.add_row("Vision 2030", intel.vision_2030_alignment)
    console.print(table)


@app.command()
def script(
    sector_name: Annotated[str, typer.Argument()] = "technology",
    locale: Annotated[str, typer.Option("--locale", "-l")] = "ar",
    script_type: Annotated[str, typer.Option("--type", "-t")] = "opener",
    name: Annotated[str, typer.Option("--name", "-n")] = "",
) -> None:
    """Print a bilingual sales script."""
    try:
        text = get_sales_script(
            script_type,
            locale=locale,
            name=name or ("العميل" if locale == "ar" else "there"),
            sector=sector_name,
            company="",
            date="",
            time="",
            link="",
        )
    except KeyError as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)
    console.print(Panel(text, title=f"{script_type} ({locale})", border_style="green"))


@app.command()
def lead(
    company: Annotated[str, typer.Option(prompt=True)] = "",
    name: Annotated[str, typer.Option(prompt=True)] = "",
    email: Annotated[str, typer.Option(prompt=True)] = "",
    sector: Annotated[str, typer.Option(prompt=True)] = "technology",
    message: Annotated[str, typer.Option(prompt=True)] = "",
) -> None:
    """Submit a lead through the full Phase 8 pipeline."""
    _banner()
    pipeline = AcquisitionPipeline()
    payload = {
        "company": company,
        "name": name,
        "email": email,
        "sector": sector,
        "region": "Saudi Arabia",
        "message": message,
    }
    with console.status("[cyan]Running pipeline...[/cyan]"):
        result = asyncio.run(pipeline.run(payload=payload, source=LeadSource.MANUAL))

    console.print(Panel("[bold]Pipeline complete[/bold]", border_style="green"))
    console.print(f"Lead ID: [cyan]{result.lead.id}[/cyan]")
    if result.fit_score:
        console.print(
            f"Fit tier: [bold]{result.fit_score.tier}[/bold] "
            f"(score {result.fit_score.overall_score:.2f})"
        )
    console.print(f"Status: {result.lead.status.value}")
    if result.warnings:
        console.print("[yellow]Warnings:[/yellow]")
        for w in result.warnings:
            console.print(f"  • {w}")


@app.command()
def demo() -> None:
    """Run an end-to-end demo: Arabic lead → full pipeline."""
    _banner()
    from scripts.run_demo import main as demo_main

    asyncio.run(demo_main())


# ── Hermes sub-app ─────────────────────────────────────────────
hermes_app = typer.Typer(help="Hermes multi-agent commands.")
app.add_typer(hermes_app, name="hermes")


@hermes_app.command("agents")
def hermes_agents() -> None:
    """List all registered Hermes agents."""
    _banner()
    try:
        from dealix.hermes.config import get_hermes_config
        from dealix.hermes.registry import HermesRegistry
    except ImportError as exc:
        console.print(f"[red]Hermes not available: {exc}[/red]")
        raise typer.Exit(code=1)

    registry = HermesRegistry.instance()
    registry.build_all_agents(config=get_hermes_config())

    table = Table(title="Hermes Agents", show_lines=True)
    table.add_column("Name", style="cyan")
    table.add_column("Description")
    for info in registry.all_info():
        table.add_row(info["name"], info["description"])
    if not registry.list_agents():
        table.add_row("(none)", "[dim]no agents registered[/dim]")
    console.print(table)


@hermes_app.command("run")
def hermes_run(
    name: Annotated[str, typer.Argument(help="Agent name to run")],
    input: Annotated[
        str,
        typer.Option("--input", "-i", help="JSON string of input data"),
    ] = "{}",
) -> None:
    """Run a named Hermes agent with optional JSON input."""
    import json

    _banner()
    try:
        from dealix.hermes.config import get_hermes_config
        from dealix.hermes.registry import HermesRegistry
    except ImportError as exc:
        console.print(f"[red]Hermes not available: {exc}[/red]")
        raise typer.Exit(code=1)

    try:
        input_data: dict = json.loads(input)
    except json.JSONDecodeError as exc:
        console.print(f"[red]Invalid JSON input: {exc}[/red]")
        raise typer.Exit(code=1)

    registry = HermesRegistry.instance()
    registry.build_all_agents(config=get_hermes_config())

    try:
        agent = registry.get(name)
    except KeyError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1)

    with console.status(f"[cyan]Running agent {name!r}...[/cyan]"):
        result = asyncio.run(agent.run(input_data))

    console.print_json(json.dumps(result, ensure_ascii=False, default=str))


@hermes_app.command("pipeline")
def hermes_pipeline(
    name: Annotated[str, typer.Argument(help="Pipeline name to run")],
    input: Annotated[
        str,
        typer.Option("--input", "-i", help="JSON string of input data"),
    ] = "{}",
) -> None:
    """Run a named Hermes pipeline with optional JSON input."""
    import json

    _banner()
    try:
        from dealix.hermes.config import get_hermes_config
        from dealix.hermes.orchestrator import HermesOrchestrator
        from dealix.hermes.registry import HermesRegistry
    except ImportError as exc:
        console.print(f"[red]Hermes not available: {exc}[/red]")
        raise typer.Exit(code=1)

    try:
        input_data: dict = json.loads(input)
    except json.JSONDecodeError as exc:
        console.print(f"[red]Invalid JSON input: {exc}[/red]")
        raise typer.Exit(code=1)

    registry = HermesRegistry.instance()
    config = get_hermes_config()
    registry.build_all_agents(config=config)
    orchestrator = HermesOrchestrator(registry=registry, config=config)

    with console.status(f"[cyan]Running pipeline {name!r}...[/cyan]"):
        result = asyncio.run(orchestrator.run_pipeline(name, input_data))

    console.print_json(json.dumps(result, ensure_ascii=False, default=str))


@hermes_app.command("health")
def hermes_health() -> None:
    """Check Hermes system health: API key presence and registered agents."""
    import os

    _banner()
    try:
        from dealix.hermes.config import get_hermes_config
        from dealix.hermes.registry import HermesRegistry
    except ImportError as exc:
        console.print(f"[red]Hermes not available: {exc}[/red]")
        raise typer.Exit(code=1)

    config = get_hermes_config()
    api_key = config.effective_api_key()

    table = Table(title="Hermes Health", show_lines=True)
    table.add_column("Check", style="cyan")
    table.add_column("Status")

    if api_key:
        table.add_row("API key", "[green]set[/green]")
    else:
        table.add_row("API key", "[red]not set (set ANTHROPIC_API_KEY or HERMES_API_KEY)[/red]")

    registry = HermesRegistry.instance()
    registry.build_all_agents(config=config)
    agent_names = registry.list_agents()
    table.add_row(
        "Registered agents",
        f"[green]{len(agent_names)}[/green]: {', '.join(agent_names)}" if agent_names
        else "[yellow]none[/yellow]",
    )

    console.print(table)


@app.command()
def menu() -> None:
    """Interactive menu (Arabic + English)."""
    _banner()
    while True:
        console.print(
            "\n[bold]Commands[/bold]\n"
            " [cyan]1[/cyan] · status\n"
            " [cyan]2[/cyan] · sector <name>\n"
            " [cyan]3[/cyan] · script <sector>\n"
            " [cyan]4[/cyan] · lead (interactive)\n"
            " [cyan]5[/cyan] · demo\n"
            " [cyan]0[/cyan] · exit"
        )
        choice = Prompt.ask("Choose", default="0")
        if choice == "0":
            break
        if choice == "1":
            status()
        elif choice == "2":
            s = Prompt.ask("Sector", default="healthcare")
            sector(s)
        elif choice == "3":
            s = Prompt.ask("Sector", default="technology")
            script(s)
        elif choice == "4":
            lead()
        elif choice == "5":
            demo()


# ── Success architecture commands ──────────────────────────────

_REPO_ROOT = Path(__file__).parent

_SCORE_PATTERN = re.compile(
    r"(?:score[:\s]+|total[:\s]+)?(\d{1,3})\s*(?:/\s*100|%|\.0)?",
    re.IGNORECASE,
)

_LAUNCH_TIERS: list[tuple[int, str, str]] = [
    (90, "Launch Ready", "proceed to full launch"),
    (85, "Controlled Launch", "launch with controlled rollout"),
    (75, "Soft Launch", "soft launch to limited accounts"),
    (60, "Dry Run", "dry run only; address blockers first"),
    (0, "Not Ready", "not ready — resolve all critical gaps"),
]

_WAR_ROOM_REPORTS: list[tuple[str, str]] = [
    ("reports/founder/DAILY_SUPER_COMMAND.md", "Founder"),
    ("reports/revenue/REVENUE_WAR_ROOM.md", "Revenue"),
    ("reports/delivery/DELIVERY_PIPELINE_STATUS.md", "Delivery"),
    ("reports/agents/AGENT_DAILY_ACTIVITY_REVIEW.md", "Agents"),
    ("reports/scale/ULTIMATE_SCALE_SCORECARD.md", "Scale"),
]


def _extract_score(content: str) -> int | None:
    """Return the first plausible 0-100 integer found in content, or None."""
    for match in _SCORE_PATTERN.finditer(content):
        value = int(match.group(1))
        if 0 <= value <= 100:
            return value
    return None


def _read_file_safe(path: Path) -> str | None:
    """Read a file and return its content, or None if it does not exist."""
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


@app.command("launch-score")
def launch_score() -> None:
    """Read LAUNCH_SCORECARD.md, extract score, and print tier and recommendation."""
    scorecard_path = _REPO_ROOT / "reports/launch/LAUNCH_SCORECARD.md"
    content = _read_file_safe(scorecard_path)
    if content is None:
        console.print(
            f"[red]File not found:[/red] {scorecard_path.relative_to(_REPO_ROOT)}"
        )
        raise typer.Exit(code=1)

    score = _extract_score(content)
    if score is None:
        console.print("[red]No numeric score (0-100) found in LAUNCH_SCORECARD.md[/red]")
        raise typer.Exit(code=1)

    tier_label = "Not Ready"
    recommendation = "not ready — resolve all critical gaps"
    for min_score, label, rec in _LAUNCH_TIERS:
        if score >= min_score:
            tier_label = label
            recommendation = rec
            break

    table = Table(title="Launch Scorecard", show_lines=True)
    table.add_column("Field", style="cyan")
    table.add_column("Value")
    table.add_row("Score", str(score))
    table.add_row("Tier", tier_label)
    table.add_row("Recommendation", recommendation)
    console.print(table)


@app.command("scale-score")
def scale_score() -> None:
    """Read ULTIMATE_SCALE_SCORECARD.md, extract score, and print tier."""
    scorecard_path = _REPO_ROOT / "reports/scale/ULTIMATE_SCALE_SCORECARD.md"
    content = _read_file_safe(scorecard_path)
    if content is None:
        console.print(
            f"[red]File not found:[/red] {scorecard_path.relative_to(_REPO_ROOT)}"
        )
        raise typer.Exit(code=1)

    score = _extract_score(content)
    if score is None:
        console.print(
            "[red]No numeric score (0-100) found in ULTIMATE_SCALE_SCORECARD.md[/red]"
        )
        raise typer.Exit(code=1)

    # Reuse launch tier thresholds for scale readiness
    tier_label = "Not Ready"
    for min_score, label, _ in _LAUNCH_TIERS:
        if score >= min_score:
            tier_label = label
            break

    table = Table(title="Scale Scorecard", show_lines=True)
    table.add_column("Field", style="cyan")
    table.add_column("Value")
    table.add_row("Score", str(score))
    table.add_row("Tier", tier_label)
    console.print(table)


_FOUNDER_COMMAND_TEMPLATE = """\
# DAILY SUPER COMMAND — TEMPLATE

## Priority 1 — Revenue
- [ ] Review pipeline and identify top 3 accounts to advance today

## Priority 2 — Delivery
- [ ] Check delivery blockers and assign resolution owners

## Priority 3 — Governance
- [ ] Review agent activity log for any anomalies

## Priority 4 — Metrics
- [ ] Update KPIs and note any deviations from targets

## Today's Decision
- Decision: [state the key decision for today]
- Owner: [name]
- Deadline: [date]
"""


@app.command("founder-command")
def founder_command(
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Print template instead of actual file")
    ] = False,
) -> None:
    """Read DAILY_SUPER_COMMAND.md and print it. With --dry-run prints a template."""
    if dry_run:
        console.print(
            Panel(
                _FOUNDER_COMMAND_TEMPLATE.strip(),
                title="Founder Command (template)",
                border_style="yellow",
            )
        )
        return

    command_path = _REPO_ROOT / "reports/founder/DAILY_SUPER_COMMAND.md"
    content = _read_file_safe(command_path)
    if content is None:
        console.print(
            f"[red]File not found:[/red] {command_path.relative_to(_REPO_ROOT)}"
        )
        raise typer.Exit(code=1)

    console.print(
        Panel(content.strip(), title="Founder Daily Command", border_style="cyan")
    )


_WAR_ROOM_STRUCTURE = """\
War Room — 5 Reports

1. Founder   reports/founder/DAILY_SUPER_COMMAND.md
2. Revenue   reports/revenue/REVENUE_WAR_ROOM.md
3. Delivery  reports/delivery/DELIVERY_PIPELINE_STATUS.md
4. Agents    reports/agents/AGENT_DAILY_ACTIVITY_REVIEW.md
5. Scale     reports/scale/ULTIMATE_SCALE_SCORECARD.md
"""


@app.command("war-room")
def war_room(
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="Print structure overview instead of summaries")
    ] = False,
) -> None:
    """Print summary from all 5 war room reports. With --dry-run prints structure overview."""
    if dry_run:
        console.print(
            Panel(
                _WAR_ROOM_STRUCTURE.strip(),
                title="War Room (structure overview)",
                border_style="yellow",
            )
        )
        return

    table = Table(title="War Room Summary", show_lines=True)
    table.add_column("Report", style="cyan")
    table.add_column("Status")
    table.add_column("First Line")

    for rel, label in _WAR_ROOM_REPORTS:
        path = _REPO_ROOT / rel
        content = _read_file_safe(path)
        if content is None:
            table.add_row(label, "[red]NOT FOUND[/red]", f"[dim]{rel}[/dim]")
        else:
            # Use the first non-empty, non-header line as a summary
            first_line = ""
            for line in content.splitlines():
                stripped = line.strip().lstrip("#").strip()
                if stripped:
                    first_line = stripped[:80]
                    break
            table.add_row(label, "[green]found[/green]", first_line or "[dim](empty)[/dim]")

    console.print(table)


if __name__ == "__main__":
    # Default to menu if no args
    import sys

    if len(sys.argv) == 1:
        menu()
    else:
        app()
