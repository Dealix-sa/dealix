"""
Safety classifier — prompt-injection, jailbreak, secret-exfil, doctrine breach.
طبقة السلامة — كشف محاولات حقن التعليمات وتجاوز الحوكمة.

Returns a deterministic score in [0,1] (where 1 = clearly malicious),
the matched cues, and an action recommendation aligned with Dealix's
"never live-send / never charge / never bypass approval" rules.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from dealix.intelligence.arabic_nlp import normalize_arabic

Severity = Literal["safe", "warn", "block"]


# Heuristic cue dictionaries — Arabic + English. Single-words go via
# token check; phrases via substring match on normalized text.
_INJECTION_CUES = [
    "ignore previous", "ignore the above", "disregard previous", "forget your",
    "you are now", "act as", "roleplay as", "system prompt",
    "do anything now", "dan mode", "developer mode",
    "تجاهل التعليمات", "تجاهل ما سبق", "انسى التعليمات", "تظاهر انك",
    "تصرف كأنك", "وضع المطور",
]
_SECRET_EXFIL_CUES = [
    "api_key", "api key", "secret key", "anthropic_api_key", "openai_api_key",
    "groq_api_key", "google_api_key", "deepseek_api_key", "supabase_service",
    "private key", "ssh key", "stripe_secret", "moyasar_secret", "bearer ",
    "password", ".env file", "credentials.json",
    "مفتاح سري", "كلمة سر", "كلمة المرور", "ملف بيئة",
]
_DOCTRINE_BREACH_CUES = [
    "send a real message", "actually send", "go live", "live-send",
    "charge the customer", "real charge", "bypass approval", "skip approval",
    "delete user", "drop table", "wipe database", "rm -rf",
    "ارسل فعلا", "ارسل مباشر", "اخصم فعلا", "تجاوز الموافقه",
    "تجاوز الموافقة", "احذف العميل",
]
_JAILBREAK_CUES = [
    "jailbreak", "dan prompt", "rebel prompt", "no restrictions",
    "without ethics", "without filter", "without policies",
    "اختراق التعليمات", "بدون قيود", "بدون فلتر",
]

_BASE64_LIKE = re.compile(r"\b[A-Za-z0-9+/]{40,}={0,2}\b")
_HOMOGLYPH_LATIN_IN_AR = re.compile(r"[؀-ۿ][a-z]|[a-z][؀-ۿ]")


@dataclass(frozen=True)
class SafetyFinding:
    category: str
    cue: str
    severity: Severity


@dataclass(frozen=True)
class SafetyResult:
    score: float  # 0..1
    severity: Severity
    findings: tuple[SafetyFinding, ...]
    redacted_input: str
    recommended_action: Literal["allow", "review", "block"]


class SafetyClassifier:
    """Heuristic guardrails — first line of defense before LLM call."""

    def __init__(
        self,
        *,
        block_threshold: float = 0.65,
        warn_threshold: float = 0.30,
    ) -> None:
        self.block_threshold = block_threshold
        self.warn_threshold = warn_threshold

    def evaluate(self, text: str) -> SafetyResult:
        if not text or not text.strip():
            return SafetyResult(0.0, "safe", tuple(), "", "allow")
        norm = normalize_arabic(text.lower())
        findings: list[SafetyFinding] = []
        score = 0.0

        score += self._scan_cues(norm, _INJECTION_CUES, "prompt_injection", 0.45, findings)
        score += self._scan_cues(norm, _JAILBREAK_CUES, "jailbreak", 0.55, findings)
        score += self._scan_cues(norm, _DOCTRINE_BREACH_CUES, "doctrine_breach", 0.7, findings)
        score += self._scan_cues(norm, _SECRET_EXFIL_CUES, "secret_exfil", 0.6, findings)

        # Suspicious encodings
        if _BASE64_LIKE.search(text):
            findings.append(SafetyFinding("encoded_payload", "base64-like", "warn"))
            score += 0.15
        if _HOMOGLYPH_LATIN_IN_AR.search(text):
            findings.append(SafetyFinding("mixed_script", "AR/EN adjacency", "warn"))
            score += 0.05

        score = min(1.0, score)
        severity: Severity
        if score >= self.block_threshold:
            severity = "block"
        elif score >= self.warn_threshold:
            severity = "warn"
        else:
            severity = "safe"
        action: Literal["allow", "review", "block"]
        if severity == "block":
            action = "block"
        elif severity == "warn":
            action = "review"
        else:
            action = "allow"
        return SafetyResult(
            score=round(score, 4),
            severity=severity,
            findings=tuple(findings),
            redacted_input=self._redact(text, findings) if findings else text,
            recommended_action=action,
        )

    # ── Internals ─────────────────────────────────────────────────
    @staticmethod
    def _scan_cues(
        text: str,
        cues: list[str],
        category: str,
        weight: float,
        sink: list[SafetyFinding],
    ) -> float:
        norm_cues = [normalize_arabic(c.lower()) for c in cues]
        total = 0.0
        for cue, ncue in zip(cues, norm_cues):
            if ncue in text:
                sink.append(SafetyFinding(category, cue, "block" if weight >= 0.6 else "warn"))
                total += weight
        return total

    @staticmethod
    def _redact(text: str, findings: list[SafetyFinding]) -> str:
        out = text
        for f in findings:
            if not f.cue:
                continue
            out = re.sub(re.escape(f.cue), "[REDACTED]", out, flags=re.IGNORECASE)
        return out
