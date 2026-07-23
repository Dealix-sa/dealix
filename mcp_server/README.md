# Dealix MCP Server

Exposes the Dealix Business OS as MCP tools for Claude Desktop, Claude Code, and any other MCP client.

## Tools available

| Tool | Description |
|------|-------------|
| `get_mcp_trust_manifest` | Fingerprinted permissions and denied capabilities for every tool |
| `get_war_room_today` | Today's P0 leads with outreach status |
| `get_kpi_snapshot` | Platform + commercial KPIs |
| `get_business_now` | 8-pillar business status |
| `get_commercial_strategy` | Offer ladder + GTM focus |
| `get_doctrine_rules` | 11 non-negotiable rules |
| `get_founder_cockpit` | Daily founder cockpit |
| `get_expansion_status` | GTM targeting + social queue depth |
| `get_outreach_drafts` | Pending drafts awaiting approval |
| `get_evidence_summary` | Proof event counts by tier |
| `get_commercial_digest` | Full morning brief |
| `get_ceo_master_plan_status` | 90-day plan progress |
| `get_platform_kpi_baselines` | Platform KPI targets |
| `get_todo_registry` | Open task registry |
| `get_risk_register` | Risk register |
| `get_targeting_pool` | Warm account pool |
| `get_social_content_queue` | LinkedIn content queue |
| `get_company_policy` | Safe mode status |
| `get_war_room_lead_stages` | Funnel stage definitions |
| `draft_warm_intro` | Generate outreach draft (no send) |
| `run_diagnostic_report` | Prospect diagnostic report |

## Run locally

```bash
# Install dependencies
pip install fastmcp

# STDIO mode (Claude Desktop / Claude Code)
python mcp_server/dealix_mcp.py

# HTTP mode (remote access)
python mcp_server/dealix_mcp.py --transport http --port 8001

# Via FastMCP CLI
fastmcp run mcp_server/dealix_mcp.py
fastmcp run mcp_server/dealix_mcp.py --transport http --port 8001
```

## Claude Desktop setup

Add to `~/.config/claude/claude_desktop_config.json` (Linux/Mac) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "dealix": {
      "command": "python",
      "args": ["/path/to/dealix/mcp_server/dealix_mcp.py"],
      "env": {
        "DEALIX_API_BASE": "http://localhost:8000",
        "DEALIX_ADMIN_API_KEY": "your-admin-key"
      }
    }
  }
}
```

## Claude Code setup

Add to `.mcp.json` in the project root:

```json
{
  "mcpServers": {
    "dealix": {
      "command": "python",
      "args": ["mcp_server/dealix_mcp.py"],
      "env": {
        "DEALIX_API_BASE": "http://localhost:8000",
        "DEALIX_ADMIN_API_KEY": "your-admin-key"
      }
    }
  }
}
```

## Railway deployment (HTTP mode)

Remote HTTP is fail-closed. It must sit behind an ingress that enforces authentication,
and the exact public hostname and browser origin must be declared. Wildcards are rejected.

Add to `railway.json` services:

```json
{
  "command": "python mcp_server/dealix_mcp.py --transport http --host 0.0.0.0 --port $PORT"
}
```

Required environment gates for the example above:

```bash
DEALIX_MCP_REMOTE_HTTP_ENABLED=1
DEALIX_MCP_TRUSTED_INGRESS_AUTH=1
DEALIX_MCP_ALLOWED_HOSTS=mcp.dealix.me
DEALIX_MCP_ALLOWED_ORIGINS=https://chatgpt.com
```

Do not set `DEALIX_MCP_TRUSTED_INGRESS_AUTH=1` unless the ingress actually rejects
unauthenticated requests. `allowed_hosts` and `allowed_origins` are passed directly to
FastMCP host/origin protection. STDIO and loopback HTTP remain available without these
remote gates.

Before adding a remote MCP client endpoint, call `validate_mcp_endpoint()` from
`mcp_server.trust_gate`, connect only to a returned IP while preserving the original
hostname for TLS, and call `revalidate_mcp_endpoint()` before reconnecting. A changed
DNS fingerprint requires a fresh approval.

## Doctrine enforcement

All write tools (draft_warm_intro, run_diagnostic_report) produce drafts only.
No external messages are sent automatically. Founder approval is required for everything.

Every tool is registered through `@governed_tool`. Import fails if a tool requests an
undeclared capability, secret access, external side effects, or draft authority without
an approval requirement. The runtime manifest SHA-256 changes whenever permissions drift.
Each policy also declares a bounded timeout and rate limit. Rate limits are enforced per
process, and every call emits a metadata-only audit record without arguments or results.

See `get_doctrine_rules()` for the full list of non-negotiables.
