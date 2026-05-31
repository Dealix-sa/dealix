"""
Data Loss Prevention — منع تسريب البيانات المنظّمة.

يفحص النص بحثًا عن tokens منظّمة (هوية وطنية، IBAN، بطاقات، أرقام جوّال
سعوديّة، عناوين بريد). إذا وُجدت ولم يكن هناك workspace أو كان workspace
خارجيًّا (external)، يُرفض الطلب.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RegulatedHit:
    kind: str
    sample: str  # عيّنة مُختصرة (أوّل/آخر رمز فقط).


@dataclass
class DLPVerdict:
    allow: bool
    reason: str
    hits: list[RegulatedHit] = field(default_factory=list)


# ما يُعدّ "خارجيًا" — أي workspace غير معروف داخل الشركة.
_INTERNAL_PREFIXES: tuple[str, ...] = ("dealix-", "internal-", "ws_internal_")


_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("saudi_national_id", re.compile(r"(?<!\d)[12]\d{9}(?!\d)")),
    ("iban_sa", re.compile(r"\bSA\d{22}\b")),
    ("credit_card", re.compile(r"(?<!\d)(?:\d[ -]?){12,15}\d(?!\d)")),
    ("saudi_mobile", re.compile(r"(?<!\d)(?:\+?966|0)?5\d{8}(?!\d)")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")),
)


def _redact_sample(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)
    return value[:2] + "*" * (len(value) - 4) + value[-2:]


def _is_internal_workspace(workspace_id: str | None) -> bool:
    if not workspace_id:
        return False
    return any(workspace_id.startswith(prefix) for prefix in _INTERNAL_PREFIXES)


class DLP:
    """واجهة DLP الرئيسة."""

    def scan(self, text: str, workspace_id: str | None) -> DLPVerdict:
        if not isinstance(text, str):
            raise TypeError("text must be str")

        hits: list[RegulatedHit] = []
        for kind, pattern in _PATTERNS:
            for match in pattern.finditer(text):
                hits.append(RegulatedHit(kind=kind, sample=_redact_sample(match.group(0))))

        if not hits:
            return DLPVerdict(allow=True, reason="no_regulated_tokens", hits=[])

        if workspace_id is None:
            return DLPVerdict(
                allow=False,
                reason="regulated_tokens_without_workspace",
                hits=hits,
            )

        if not _is_internal_workspace(workspace_id):
            return DLPVerdict(
                allow=False,
                reason=f"regulated_tokens_in_external_workspace:{workspace_id}",
                hits=hits,
            )

        return DLPVerdict(
            allow=True,
            reason="regulated_tokens_within_internal_workspace",
            hits=hits,
        )


__all__ = ["DLP", "DLPVerdict", "RegulatedHit"]
