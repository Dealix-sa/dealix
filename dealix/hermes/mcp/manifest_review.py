"""
Manifest review — static structural review of an MCP manifest.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

_REQUIRED_FIELDS = ("server_id", "version", "tools", "publisher")
_BANNED_TOOL_PREFIXES = ("admin/", "root/", "exec/")
_DANGEROUS_PATTERNS = (
    "rm -rf",
    "DROP TABLE",
    "import os; os.system",
    "subprocess.Popen(",
)


@dataclass
class ManifestReview:
    ok: bool
    findings: list[str]
    manifest_sha256: str


def review_manifest(manifest: dict[str, object]) -> ManifestReview:
    findings: list[str] = []

    for field_name in _REQUIRED_FIELDS:
        if field_name not in manifest:
            findings.append(f"missing_field:{field_name}")

    tools = manifest.get("tools") or []
    if not isinstance(tools, list):
        findings.append("tools_not_list")
        tools = []

    for tool in tools:
        if not isinstance(tool, dict):
            findings.append("tool_not_object")
            continue
        name = tool.get("name", "")
        if not name:
            findings.append("tool_missing_name")
        if any(str(name).startswith(p) for p in _BANNED_TOOL_PREFIXES):
            findings.append(f"banned_tool_prefix:{name}")
        descriptor = str(tool.get("description", "") or "")
        for pattern in _DANGEROUS_PATTERNS:
            if pattern in descriptor:
                findings.append(f"dangerous_descriptor_pattern:{pattern}")

    canonical = json.dumps(manifest, sort_keys=True, ensure_ascii=False).encode("utf-8")
    sha = hashlib.sha256(canonical).hexdigest()

    return ManifestReview(ok=not findings, findings=findings, manifest_sha256=sha)
