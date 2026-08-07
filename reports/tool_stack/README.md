# Tool Stack Reports

This directory stores generated rankings for the Dealix open-source autonomy stack.

Generate a report with:

```bash
python scripts/commercial/score_tool_stack.py   --registry dealix/strategy_execution/tool_registry.json   --output reports/tool_stack/ranked_tool_stack.md
```

Reports are decision aids only. They do not install tools, enable live outbound, or change production.
