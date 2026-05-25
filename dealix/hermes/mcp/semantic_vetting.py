"""
Semantic vetting — checks that the tool's stated purpose matches the
declared capability domain and required data scope.
"""

from __future__ import annotations

from dataclasses import dataclass

# Each declared capability domain has a set of *safe* verbs. If the
# descriptor mostly uses verbs from outside the safe set, it is flagged.
_DOMAIN_SAFE_VERBS: dict[str, frozenset[str]] = {
    "read": frozenset({"read", "list", "fetch", "get", "describe", "summarize"}),
    "draft": frozenset({"draft", "compose", "outline", "rewrite", "improve"}),
    "internal_write": frozenset({"create", "update", "annotate", "tag", "assign"}),
    "external_send": frozenset({"queue", "stage", "draft", "preview", "review"}),
}


@dataclass
class SemanticVerdict:
    ok: bool
    findings: list[str]


def vet_semantics(
    domain: str,
    descriptor: str,
    *,
    required_data_scope: list[str] | tuple[str, ...] | None = None,
    declared_data_scope: list[str] | tuple[str, ...] = (),
) -> SemanticVerdict:
    safe_verbs = _DOMAIN_SAFE_VERBS.get(domain)
    findings: list[str] = []
    if safe_verbs is None:
        findings.append(f"unknown_domain:{domain}")
    else:
        words = {w.lower().strip(",.;:") for w in descriptor.split()}
        hits = words & safe_verbs
        if not hits and descriptor:
            findings.append(f"no_safe_verbs_for_domain:{domain}")

    if required_data_scope:
        missing = set(required_data_scope) - set(declared_data_scope)
        if missing:
            findings.append(f"missing_data_scope:{sorted(missing)}")
        unexpected = set(declared_data_scope) - set(required_data_scope)
        if unexpected:
            findings.append(f"over_scoped_data:{sorted(unexpected)}")

    return SemanticVerdict(ok=not findings, findings=findings)
