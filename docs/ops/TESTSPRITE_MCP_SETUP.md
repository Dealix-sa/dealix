# TestSprite MCP Setup

This guide adds TestSprite as a local MCP server for Dealix development without committing API keys.

## Security status

The repository already ignores local MCP config files named `.mcp.json`. Keep the real key only in your local machine, Codespaces secret store, or MCP client secret settings.

If an API key was pasted into chat, logs, terminal history, or a GitHub issue/PR, rotate it in TestSprite before using it again.

## Local setup

Set the secret in your current shell or Codespaces secret store:

```bash
export TESTSPRITE_API_KEY="..."
```

Validate that Dealix can see the secret without printing it:

```bash
python scripts/ops/check_testsprite_mcp_env.py
```

Generate a local-only `.mcp.json` from the environment variable:

```bash
python scripts/ops/prepare_testsprite_mcp_local.py
```

Do not commit `.mcp.json`.

## Direct MCP smoke run

Run a short MCP server smoke test:

```bash
bash scripts/ops/run_testsprite_mcp_smoke.sh
```

Expected safe result for a stdio MCP server:

```text
TESTSPRITE_MCP_SMOKE=SERVER_STAYED_ALIVE
```

This means the server started and did not crash during the timeout window.

## Recommended secret name

Use this name in your local shell, Codespaces secrets, or agent environment:

```bash
TESTSPRITE_API_KEY=...
```

Some MCP clients require the key to be written into their local JSON config. If so, keep that file outside Git tracking.

## MCP config shape

```json
{
  "mcpServers": {
    "TestSprite": {
      "command": "npx",
      "args": ["@testsprite/testsprite-mcp@latest"],
      "env": {
        "API_KEY": "<TESTSPRITE_API_KEY>"
      }
    }
  }
}
```

## Optional GitHub Actions workflow

A workflow template is provided at:

```text
docs/ops/testsprite-mcp-smoke.workflow.yml
```

To activate it, copy it to:

```text
.github/workflows/testsprite-mcp-smoke.yml
```

Then add a GitHub repository secret named:

```text
TESTSPRITE_API_KEY
```

The workflow is manual-only via `workflow_dispatch`.

## Dealix operating rule

TestSprite can be used to generate and run tests, inspect flows, and support quality gates, but it must not receive production secrets, live customer records, raw outreach lists, private ledgers, uncontrolled outbound credentials, or personal data that is not required for testing.

Use synthetic demo data by default.
