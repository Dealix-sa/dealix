# MCP Security

MCP descriptors are treated as untrusted input. The MCP Risk Review
product audits every descriptor on a customer's MCP server, scores
each tool on data sensitivity and reversibility, and ships an
approval-gated tool registry.

## Rules

- Descriptors are version-pinned in the platform.
- Drift in a descriptor fires the `mcp_descriptor_changed` alert.
- High-risk tools (external action, S3 data) are wrapped in an
  approval ticket by default.
- Any tool whose descriptor is not in the registry is denied at the
  `tool_gate`.
