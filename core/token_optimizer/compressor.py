"""
Context compressor — reduces token count of long documents, RAG chunks, prompts.
ضاغط السياق — يقلل عدد توكنز الوثائق الطويلة وقطع RAG والبرومبتات.

Strategies (applied in order):
  1. Whitespace normalization
  2. Comment stripping (code)
  3. Sentence importance scoring (TF-IDF-lite)
  4. LLMLingua (if installed) for deep compression
  5. Max-token truncation (safety net)
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any

from core.token_optimizer.counter import count_tokens

logger = logging.getLogger(__name__)


@dataclass
class CompressionResult:
    original_text: str
    compressed_text: str
    original_tokens: int
    compressed_tokens: int
    strategy: str
    compression_ratio: float

    @classmethod
    def from_texts(
        cls, original: str, compressed: str, strategy: str, model: str = "cl100k_base"
    ) -> CompressionResult:
        orig_t = count_tokens(original, model)
        comp_t = count_tokens(compressed, model)
        ratio = 1.0 - (comp_t / orig_t) if orig_t > 0 else 0.0
        return cls(
            original_text=original,
            compressed_text=compressed,
            original_tokens=orig_t,
            compressed_tokens=comp_t,
            strategy=strategy,
            compression_ratio=round(ratio, 3),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy": self.strategy,
            "original_tokens": self.original_tokens,
            "compressed_tokens": self.compressed_tokens,
            "compression_ratio_pct": round(self.compression_ratio * 100, 1),
            "tokens_saved": self.original_tokens - self.compressed_tokens,
        }


# ── Strategy 1: Whitespace Normalization ────────────────────────

def normalize_whitespace(text: str) -> str:
    """Remove redundant whitespace, blank lines, trailing spaces."""
    lines = [line.rstrip() for line in text.splitlines()]
    # Collapse 3+ consecutive blank lines to 1
    result: list[str] = []
    blank_count = 0
    for line in lines:
        if line == "":
            blank_count += 1
            if blank_count <= 1:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)
    return "\n".join(result).strip()


# ── Strategy 2: Comment Stripping ───────────────────────────────

def strip_code_comments(text: str, language: str = "auto") -> str:
    """Remove single-line and block comments from code."""
    if language == "auto":
        # Detect by content patterns
        if "def " in text or "import " in text or "class " in text:
            language = "python"
        elif "function" in text or "const " in text or "=>" in text:
            language = "javascript"
        else:
            language = "python"

    if language in ("python",):
        # Remove # comments
        text = re.sub(r"(?m)^\s*#.*$", "", text)
        # Remove triple-quoted docstrings (simplified)
        text = re.sub(r'"""[\s\S]*?"""', "", text)
        text = re.sub(r"'''[\s\S]*?'''", "", text)

    elif language in ("javascript", "typescript", "js", "ts"):
        # Remove // comments
        text = re.sub(r"(?m)^\s*//.*$", "", text)
        # Remove /* */ blocks
        text = re.sub(r"/\*[\s\S]*?\*/", "", text)

    return normalize_whitespace(text)


# ── Strategy 3: Sentence Importance Scoring ─────────────────────

def _word_freq(text: str) -> dict[str, int]:
    """Simple word frequency dict."""
    words = re.findall(r"\b\w+\b", text.lower())
    freq: dict[str, int] = {}
    for w in words:
        if len(w) > 3:  # skip short stop words
            freq[w] = freq.get(w, 0) + 1
    return freq


def extract_important_sentences(
    text: str,
    keep_ratio: float = 0.6,
    min_sentences: int = 3,
) -> str:
    """
    Keep the most important sentences based on TF-IDF-lite scoring.
    Useful for compressing long docs, meeting notes, RAG context.

    keep_ratio: fraction of sentences to retain (0.6 = keep top 60%)
    """
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if len(sentences) <= min_sentences:
        return text

    freq = _word_freq(text)
    if not freq:
        return text

    max_freq = max(freq.values())

    def score(sentence: str) -> float:
        words = re.findall(r"\b\w+\b", sentence.lower())
        if not words:
            return 0.0
        return sum(freq.get(w, 0) / max_freq for w in words if len(w) > 3) / len(words)

    scored = [(score(s), i, s) for i, s in enumerate(sentences)]
    keep_n = max(min_sentences, int(len(sentences) * keep_ratio))
    top_indices = {i for _, i, _ in sorted(scored, reverse=True)[:keep_n]}

    # Maintain original order
    return " ".join(s for i, s in enumerate(sentences) if i in top_indices)


# ── Strategy 4: LLMLingua (optional) ────────────────────────────

async def compress_with_llmlingua(
    text: str,
    ratio: float = 0.5,
    question: str | None = None,
) -> str | None:
    """
    Compress text using LLMLingua if installed.
    Returns None if LLMLingua is not available.

    Install: pip install llmlingua
    Note: requires PyTorch (~2GB download on first use)
    """
    try:
        from llmlingua import PromptCompressor  # type: ignore
        compressor = PromptCompressor(
            model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
            use_llmlingua2=True,
            device_map="cpu",
        )
        result = compressor.compress_prompt(
            text,
            rate=ratio,
            question=question or "",
            force_tokens=["\n", "?"],
        )
        return result.get("compressed_prompt", text)
    except ImportError:
        return None
    except Exception as e:
        logger.warning("LLMLingua compression failed: %s", e)
        return None


# ── Strategy 5: Max-Token Truncation ────────────────────────────

def truncate_to_tokens(
    text: str,
    max_tokens: int,
    model: str = "claude-sonnet-4-6",
    from_end: bool = False,
) -> str:
    """
    Hard truncate text to max_tokens.
    from_end=True: keep the END of the text (useful for chat history).
    """
    current = count_tokens(text, model)
    if current <= max_tokens:
        return text

    # Binary search for the right split point
    chars = len(text)
    # Estimate chars per token
    ratio = chars / current
    target_chars = int(max_tokens * ratio * 0.95)  # 5% safety margin

    if from_end:
        truncated = text[-target_chars:]
        # Find first newline to avoid mid-sentence cut
        nl = truncated.find("\n")
        if nl > 0:
            truncated = truncated[nl + 1:]
    else:
        truncated = text[:target_chars]
        # Find last newline
        nl = truncated.rfind("\n")
        if nl > 0:
            truncated = truncated[:nl]

    return truncated


# ── Main Compressor ─────────────────────────────────────────────

class ContextCompressor:
    """
    Pipeline compressor: applies strategies in order, stops when target is met.

    Usage:
        comp = ContextCompressor(target_tokens=4000)
        result = await comp.compress(long_document)
        print(f"Saved {result.original_tokens - result.compressed_tokens} tokens")
    """

    def __init__(
        self,
        target_tokens: int = 4000,
        keep_ratio: float = 0.6,
        use_llmlingua: bool = False,
        model: str = "claude-sonnet-4-6",
    ) -> None:
        self.target_tokens = target_tokens
        self.keep_ratio = keep_ratio
        self.use_llmlingua = use_llmlingua
        self.model = model

    async def compress(
        self,
        text: str,
        content_type: str = "text",
        question: str | None = None,
    ) -> CompressionResult:
        """
        Compress text using progressive strategies.

        content_type: "text" | "code" | "markdown"
        question: optional question for LLMLingua (improves relevance)
        """
        original = text
        current = text

        if count_tokens(current, self.model) <= self.target_tokens:
            return CompressionResult.from_texts(original, current, "no_compression_needed", self.model)

        # Strategy 1: Whitespace normalization
        current = normalize_whitespace(current)
        strategy = "whitespace"
        if count_tokens(current, self.model) <= self.target_tokens:
            return CompressionResult.from_texts(original, current, strategy, self.model)

        # Strategy 2: Comment stripping for code
        if content_type == "code":
            current = strip_code_comments(current)
            strategy = "whitespace+comments"
            if count_tokens(current, self.model) <= self.target_tokens:
                return CompressionResult.from_texts(original, current, strategy, self.model)

        # Strategy 3: Sentence importance scoring for text/markdown
        if content_type in ("text", "markdown"):
            current = extract_important_sentences(current, keep_ratio=self.keep_ratio)
            strategy = "whitespace+sentence_scoring"
            if count_tokens(current, self.model) <= self.target_tokens:
                return CompressionResult.from_texts(original, current, strategy, self.model)

        # Strategy 4: LLMLingua (optional, heavy)
        if self.use_llmlingua:
            compressed = await compress_with_llmlingua(current, ratio=0.5, question=question)
            if compressed:
                current = compressed
                strategy = "llmlingua"
                if count_tokens(current, self.model) <= self.target_tokens:
                    return CompressionResult.from_texts(original, current, strategy, self.model)

        # Strategy 5: Hard truncation (safety net)
        current = truncate_to_tokens(current, self.target_tokens, self.model)
        strategy = strategy + "+truncation"

        return CompressionResult.from_texts(original, current, strategy, self.model)

    def compress_sync(self, text: str, content_type: str = "text") -> CompressionResult:
        """Synchronous wrapper for non-async contexts."""
        import asyncio
        return asyncio.get_event_loop().run_until_complete(
            self.compress(text, content_type=content_type)
        )


def compress_rag_chunks(
    chunks: list[str],
    max_total_tokens: int = 8000,
    keep_ratio: float = 0.6,
    model: str = "claude-sonnet-4-6",
) -> list[str]:
    """
    Compress a list of RAG chunks to fit within max_total_tokens.
    Most relevant chunks (by length proxy) are kept; others are trimmed.
    """
    # Calculate per-chunk budget
    n = len(chunks)
    if n == 0:
        return chunks
    per_chunk = max_total_tokens // n

    result = []
    for chunk in chunks:
        if count_tokens(chunk, model) <= per_chunk:
            result.append(chunk)
        else:
            important = extract_important_sentences(chunk, keep_ratio=keep_ratio)
            result.append(truncate_to_tokens(important, per_chunk, model))
    return result
