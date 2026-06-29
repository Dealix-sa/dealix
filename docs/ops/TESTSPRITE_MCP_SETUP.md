# TestSprite MCP Setup

This guide adds TestSprite as a local MCP server for Dealix development without committing API keys.

## Security status

The repository already ignores local MCP config files named `.mcp.json`. Keep the real key only in your local machine, Codespaces secret store, or MCP client secret settings.

If an API key was pasted into chat, logs, terminal history, or a GitHub issue/PR, rotate it in TestSprite before using it again.

## Local setup

Copy the safe example into a local-only config file:

```bash
cp .mcp.testsprite.example.json .mcp.json
```

Edit `.mcp.json` locally and replace the placeholder:

```json
"API_KEY": "<TESTSPRITE_API_KEY>"
```

Do not commit `.mcp.json`.

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

## Validation

Run:

```bash
python scripts/ops/check_testsprite_mcp_env.py
```

Expected safe output when configured:

```text
TESTSPRITE_MCP_ENV=READY
```

Expected output when not configured:

```text
TESTSPRITE_MCP_ENV=MISSING
```

## Dealix operating rule

TestSprite can be used to generate and run tests, but it must not receive production secrets, live customer records, raw outreach lists, private ledgers, or uncontrolled outbound credentials.
