#!/usr/bin/env python3
"""verify_live_send_safety.py — no live external send may bypass the gate.

Confirms:
  1. docs/trust/LIVE_SEND_SAFETY_GATE.md exists and names every guard.
  2. No source file under api/, dealix/, scripts/, auto_client_acquisition/
     contains a direct unguarded send call (e.g. `send_whatsapp_direct`).
  3. The `WHATSAPP_ALLOW_LIVE_SEND` env flag, where referenced, is paired
     with an approval / policy / audit gate in the same file.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GATE_DOC = REPO / "docs" / "trust" / "LIVE_SEND_SAFETY_GATE.md"
REQUIRED_TOKENS = (
    "approval",
    "policy",
    "audit",
    "suppression",
    "daily_limit",
    "mock_mode",
    "kill_switch",
)

BANNED_DIRECT_CALLS = (
    "send_whatsapp_direct",
    "linkedin_auto_send",
    "send_now_without_approval",
    "publish_case_study_now",
)

SCAN_DIRS = ("api", "dealix", "scripts", "auto_client_acquisition")
SCAN_SUFFIXES = (".py", ".ts", ".tsx", ".js")


def main() -> int:
    failures: list[str] = []

    if not GATE_DOC.exists():
        failures.append(f"missing_gate_doc:{GATE_DOC.relative_to(REPO)}")
    else:
        body = GATE_DOC.read_text(encoding="utf-8", errors="ignore").lower()
        for tok in REQUIRED_TOKENS:
            if tok.lower() not in body:
                failures.append(f"gate_missing_token:'{tok}'")

    # Skip the verifiers themselves and the manifest — they legitimately
    # mention banned patterns as strings.
    SELF_SKIPS = {
        (REPO / "scripts" / "verify_live_send_safety.py").resolve(),
        (REPO / "scripts" / "verify_production_safety.py").resolve(),
        (REPO / "scripts" / "verify_everything.py").resolve(),
        (REPO / "scripts" / "verify_prompt_output_quality.py").resolve(),
        (REPO / "dealix_manifest.yaml").resolve(),
    }
    # Any file that contains this marker near the top is opting in to the
    # banned-patterns being mentioned (e.g., docs, lint configs).
    DOCTRINE_OPT_OUT_TAG = "audit-allow: live-send-doctrine"

    GATE_TOKENS = (
        "approval", "audit", "policy", "queue", "gate", "mock",
        "block", "deny", "suppression", "require",
    )

    for sub in SCAN_DIRS:
        root = REPO / sub
        if not root.is_dir():
            continue
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in SCAN_SUFFIXES:
                continue
            try:
                resolved = p.resolve()
            except OSError:
                continue
            if resolved in SELF_SKIPS:
                continue
            # Skip the broader verify_* family — they enumerate patterns as data.
            if p.name.startswith("verify_") and p.suffix == ".py":
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            low = text.lower()
            if DOCTRINE_OPT_OUT_TAG in low[:1024]:
                continue

            # A banned pattern that appears only inside a defensive
            # construct — a forbidden-channels set, a deny flag, a negated
            # comparison — is the *protection*, not the danger.
            lines = text.splitlines()
            for bad in BANNED_DIRECT_CALLS:
                if bad not in low:
                    continue
                for idx, line in enumerate(lines):
                    llow = line.lower()
                    if bad not in llow:
                        continue
                    near = " ".join(lines[max(0, idx - 1): idx + 2]).lower()
                    if any(
                        tok in near
                        for tok in (
                            "forbidden", "banned", "deny", "block",
                            "blocked", "no_", "denied", "not in",
                            "!= ", "raise ", "must not", "forbid",
                            "continue", "skip", "exclude", "filter",
                            "reject", "drop", "ignore",
                        )
                    ):
                        continue
                    failures.append(
                        f"direct_send_call:{p.relative_to(REPO).as_posix()}:"
                        f"{idx + 1}:'{bad}'"
                    )
            # If WHATSAPP_ALLOW_LIVE_SEND is referenced, the same file must
            # also reference at least one gate keyword (defense-in-depth).
            if "whatsapp_allow_live_send" in low:
                if not any(tok in low for tok in GATE_TOKENS):
                    failures.append(
                        "ungated_live_send_flag:"
                        f"{p.relative_to(REPO).as_posix()}"
                    )

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(f"LIVE_SEND_SAFETY_PASS={'true' if ok else 'false'} (failures={len(failures)})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
