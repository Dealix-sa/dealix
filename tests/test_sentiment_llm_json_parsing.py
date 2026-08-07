"""The LLM sentiment answer must survive prose around its JSON.

``_analyze_llm`` extracted the JSON with::

    raw = response.content.strip().strip("```json").strip("```").strip()
    result = json.loads(raw)

Two problems. ``str.strip(chars)`` takes a character *set*, not a prefix, so
that middle call stripped any of ``` ` j s o n ``` from both ends (ruff B005).
It happens not to corrupt well-formed JSON, because ``{`` and ``}`` are not in
that set — a coincidence, not a design.

The failure that does bite is prose. The prompt says "Output valid JSON only";
models routinely add "Sure!" in front or a "Note: ..." after. Any of those
made ``json.loads`` raise, ``analyze_async`` swallowed the exception, and the
caller silently got the **lexicon** score instead — same shape of result, so
nothing downstream could tell that the LLM answer had been discarded.

Measured against the original expression before changing it:

    prose before        FAILS (JSONDecodeError)
    prose after         FAILS (JSONDecodeError)
    fenced + prose      FAILS (JSONDecodeError)
    bare, well-formed   OK

``BaseAgent.parse_json_response`` already handles all four.
"""

from __future__ import annotations

import pytest

from core.nlp.sentiment import ArabicSentimentAnalyzer

# Exactly the shapes measured above.
PROSE_WRAPPED = [
    pytest.param('Sure! {"label": "positive", "score": 0.8}', id="prose-before"),
    pytest.param(
        '{"label": "positive", "score": 0.8}\n\nNote: confidence is high.',
        id="prose-after",
    ),
    pytest.param(
        'Here:\n```json\n{"label": "positive", "score": 0.8}\n```\nHope that helps.',
        id="fenced-plus-prose",
    ),
    pytest.param('```json\n{"label": "positive", "score": 0.8}\n```', id="fenced"),
    pytest.param('{"label": "positive", "score": 0.8}', id="bare"),
]


class _Response:
    def __init__(self, content: str) -> None:
        self.content = content


class _Router:
    """Returns one canned completion, so only the parsing is under test."""

    def __init__(self, content: str) -> None:
        self._content = content

    async def run(self, *_args, **_kwargs):
        return _Response(self._content)


@pytest.fixture
def analyzer():
    return ArabicSentimentAnalyzer()


def _patch_router(monkeypatch, content: str) -> None:
    import core.llm

    monkeypatch.setattr(core.llm, "get_router", lambda: _Router(content))


@pytest.mark.asyncio
@pytest.mark.parametrize("content", PROSE_WRAPPED)
async def test_llm_answer_survives_surrounding_prose(analyzer, monkeypatch, content):
    """The regression: prose around the JSON discarded the LLM answer."""
    _patch_router(monkeypatch, content)

    result = await analyzer._analyze_llm("نص تجريبي", task=object())

    assert result["label"] == "positive"
    assert result["score"] == 0.8
    assert result["method"] == "llm"


@pytest.mark.asyncio
async def test_unparseable_reply_still_raises(analyzer, monkeypatch):
    """Garbage must not be swallowed into a fake result.

    ``analyze_async`` catches this and falls back to the lexicon on purpose;
    what matters is that ``_analyze_llm`` does not invent an answer.
    """
    _patch_router(monkeypatch, "I am afraid I cannot help with that.")

    with pytest.raises(Exception):
        await analyzer._analyze_llm("نص تجريبي", task=object())


@pytest.mark.asyncio
async def test_lexicon_fallback_is_still_reached_on_a_bad_reply(analyzer, monkeypatch):
    """The fallback stays — it just should not fire for parseable answers."""
    _patch_router(monkeypatch, "no json here at all")

    result = await analyzer.analyze_async("ممتاز جدا", task=object(), force_llm=True)

    assert result["method"] == "lexicon"


@pytest.mark.asyncio
async def test_a_parseable_answer_does_not_fall_back(analyzer, monkeypatch):
    """The whole point: a usable LLM reply must reach the caller.

    Before the fix this returned `method == "lexicon"` for every reply with
    prose around it, and the caller could not tell.
    """
    _patch_router(monkeypatch, 'Sure! {"label": "negative", "score": 0.9}')

    result = await analyzer.analyze_async("نص", task=object(), force_llm=True)

    assert result["method"] == "llm", "a usable LLM answer was discarded"
    assert result["label"] == "negative"
    assert "lexicon_backup" in result


def test_the_old_strip_expression_is_gone():
    """`.strip()` with a multi-character string is a character-set strip.

    Pinned separately from behaviour because the expression is easy to
    reintroduce by reflex, and ruff only started covering `core/` in this
    same change.
    """
    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "core/nlp/sentiment.py"
    body = source.read_text(encoding="utf-8")
    code = "\n".join(
        line for line in body.splitlines() if not line.lstrip().startswith("#")
    )

    assert ".strip(" not in code.replace(".strip()", ""), (
        "a character-set strip is back in sentiment.py"
    )
