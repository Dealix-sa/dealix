# External Agent Radar Commands

Run from the repository root:

```bash
python scripts/agents/external_agent_stack_radar.py
python -m pytest -q tests/test_external_agent_stack_radar.py
```

Generated outputs:

```text
reports/agents/external_agent_stack_radar.md
reports/agents/external_agent_stack_radar.json
```

Safety posture:

- no dependencies installed
- no repositories cloned
- no runtime framework imported
- no MCP enabled
- no outbound enabled
- no external send

Use this radar before deciding whether Dealix should adopt, defer, or reject a new AI-agent repository or framework.
