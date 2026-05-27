"""CLI for Hermes agent registry and governance checks."""

from __future__ import annotations

import json
from dataclasses import asdict

import typer

from hermes_agents.policy import validate_registry
from hermes_agents.registry import load_default_registry

app = typer.Typer(help="Hermes Agents operating CLI")


@app.command()
def list_agents(json_output: bool = typer.Option(False, "--json", help="Print JSON output.")) -> None:
    """List the default Hermes agents."""

    agents = load_default_registry()
    if json_output:
        typer.echo(json.dumps([asdict(agent) for agent in agents], ensure_ascii=False, indent=2))
        return

    for agent in agents:
        typer.echo(f"{agent.agent_id}: {agent.name} [{agent.risk_level.value}] owner={agent.owner}")


@app.command()
def check() -> None:
    """Validate Hermes registry governance rules."""

    findings = validate_registry(load_default_registry())
    if findings:
        for finding in findings:
            typer.echo(f"{finding.severity.upper()} {finding.agent_id}: {finding.message}")
        raise typer.Exit(code=1)

    typer.echo("Hermes registry governance check passed.")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
