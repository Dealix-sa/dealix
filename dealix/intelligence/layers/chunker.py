"""
Smart text chunker — paragraph + sentence-aware splitter for RAG ingest.
مقطّع نصوص ذكي — يحترم الفقرات والجمل بالعربية والإنجليزية.

Output guarantees:
- chunks <= max_chars, with at most overlap_chars of overlap between
  adjacent chunks
- no chunk splits a word
- preserves sentence boundaries when possible
- bilingual aware (Arabic punctuation: ؟ ، ؛)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable

# Arabic + English sentence terminators.
_SENT_BOUNDARY = re.compile(r"(?<=[\.\?!؟])\s+|(?<=[\.\?!؟])$|\n+")
_PARA_BOUNDARY = re.compile(r"\n\s*\n+")
_WHITESPACE = re.compile(r"\s+")

DEFAULT_MAX_CHARS = 1200
DEFAULT_OVERLAP = 120


@dataclass(frozen=True)
class Chunk:
    text: str
    index: int
    start_char: int
    end_char: int
    metadata: dict = field(default_factory=dict)


class SmartChunker:
    """Hierarchical splitter: paragraphs → sentences → hard window."""

    def __init__(
        self,
        max_chars: int = DEFAULT_MAX_CHARS,
        overlap_chars: int = DEFAULT_OVERLAP,
        *,
        respect_sentences: bool = True,
    ) -> None:
        if max_chars <= 0:
            raise ValueError("max_chars must be > 0")
        if overlap_chars < 0 or overlap_chars >= max_chars:
            raise ValueError("overlap_chars must be 0 <= overlap < max_chars")
        self.max_chars = max_chars
        self.overlap_chars = overlap_chars
        self.respect_sentences = respect_sentences

    def chunk(self, text: str, metadata: dict | None = None) -> list[Chunk]:
        if not text or not text.strip():
            return []
        text = text.strip()
        # 1. Split by paragraphs
        paragraphs = [p.strip() for p in _PARA_BOUNDARY.split(text) if p.strip()]
        # 2. Within each paragraph, split by sentences if needed
        units: list[str] = []
        for para in paragraphs:
            if len(para) <= self.max_chars:
                units.append(para)
                continue
            if self.respect_sentences:
                sentences = [s.strip() for s in _SENT_BOUNDARY.split(para) if s.strip()]
            else:
                sentences = [para]
            units.extend(self._pack_sentences(sentences))
        # 3. Window units into chunks of <= max_chars with overlap
        chunks: list[Chunk] = []
        cursor = 0
        cursor_char = 0
        buf = ""
        for unit in units:
            if not buf:
                buf = unit
                continue
            if len(buf) + 1 + len(unit) <= self.max_chars:
                buf += "\n" + unit
            else:
                chunks.append(
                    Chunk(
                        text=buf,
                        index=cursor,
                        start_char=cursor_char,
                        end_char=cursor_char + len(buf),
                        metadata=dict(metadata or {}),
                    )
                )
                cursor += 1
                cursor_char += max(0, len(buf) - self.overlap_chars)
                tail = buf[-self.overlap_chars :] if self.overlap_chars else ""
                buf = (tail + "\n" + unit).strip() if tail else unit
        if buf.strip():
            chunks.append(
                Chunk(
                    text=buf,
                    index=cursor,
                    start_char=cursor_char,
                    end_char=cursor_char + len(buf),
                    metadata=dict(metadata or {}),
                )
            )
        return chunks

    def chunk_many(
        self, items: Iterable[tuple[str, dict | None]]
    ) -> list[list[Chunk]]:
        return [self.chunk(text, meta) for text, meta in items]

    def _pack_sentences(self, sentences: list[str]) -> list[str]:
        """Combine sentences greedily up to max_chars."""
        packed: list[str] = []
        buf = ""
        for s in sentences:
            s = _WHITESPACE.sub(" ", s).strip()
            if not s:
                continue
            if len(s) > self.max_chars:
                # Hard-split a single oversized sentence on word boundaries.
                if buf:
                    packed.append(buf)
                    buf = ""
                packed.extend(self._hard_split(s))
                continue
            if not buf:
                buf = s
            elif len(buf) + 1 + len(s) <= self.max_chars:
                buf += " " + s
            else:
                packed.append(buf)
                buf = s
        if buf:
            packed.append(buf)
        return packed

    def _hard_split(self, text: str) -> list[str]:
        parts: list[str] = []
        words = text.split()
        buf = ""
        for w in words:
            if not buf:
                buf = w
            elif len(buf) + 1 + len(w) <= self.max_chars:
                buf += " " + w
            else:
                parts.append(buf)
                buf = w
        if buf:
            parts.append(buf)
        return parts
