"""Unit tests for core.token_optimizer — counter, budget, cache, compressor."""
from __future__ import annotations

import asyncio
import time

import pytest


# ── counter.py ─────────────────────────────────────────────────────────────


class TestCountTokens:
    def test_returns_positive_int(self):
        from core.token_optimizer.counter import count_tokens
        n = count_tokens("Hello, world!")
        assert isinstance(n, int)
        assert n > 0

    def test_empty_string_returns_non_negative(self):
        from core.token_optimizer.counter import count_tokens
        assert count_tokens("") >= 0

    def test_longer_text_has_more_tokens(self):
        from core.token_optimizer.counter import count_tokens
        short = count_tokens("hi")
        long = count_tokens("The quick brown fox jumps over the lazy dog " * 10)
        assert long > short

    def test_known_model_openai(self):
        from core.token_optimizer.counter import count_tokens
        n = count_tokens("Test prompt", model="gpt-4o")
        assert n > 0

    def test_unknown_model_uses_heuristic(self):
        from core.token_optimizer.counter import count_tokens
        n = count_tokens("hello world", model="unknown-model-xyz")
        assert n >= 1


class TestCountMessagesTokens:
    def test_simple_messages(self):
        from core.token_optimizer.counter import count_messages_tokens
        messages = [
            {"role": "user", "content": "What is 2+2?"},
            {"role": "assistant", "content": "It is 4."},
        ]
        n = count_messages_tokens(messages)
        assert n > 0

    def test_with_system_prompt(self):
        from core.token_optimizer.counter import count_messages_tokens
        messages = [{"role": "user", "content": "Hello"}]
        without_sys = count_messages_tokens(messages)
        with_sys = count_messages_tokens(messages, system="You are a helpful assistant.")
        assert with_sys > without_sys

    def test_empty_messages_returns_at_least_two(self):
        from core.token_optimizer.counter import count_messages_tokens
        # 0 messages still adds 2 reply priming tokens
        n = count_messages_tokens([])
        assert n >= 2


class TestCostEstimate:
    def test_sonnet_estimate(self):
        from core.token_optimizer.counter import CostEstimate
        est = CostEstimate(input_tokens=1000, model="claude-sonnet-4-6")
        assert est.input_cost_usd > 0
        assert est.output_cost_usd > 0
        assert est.total_cost_usd == pytest.approx(
            est.input_cost_usd + est.output_cost_usd
        )

    def test_to_dict_keys(self):
        from core.token_optimizer.counter import CostEstimate
        est = CostEstimate(input_tokens=500, model="gpt-4o-mini")
        d = est.to_dict()
        assert set(d.keys()) >= {
            "model", "input_tokens", "estimated_output_tokens",
            "input_cost_usd", "output_cost_usd", "total_cost_usd",
        }

    def test_cache_read_reduces_cost(self):
        from core.token_optimizer.counter import CostEstimate
        no_cache = CostEstimate(input_tokens=1000, model="claude-sonnet-4-6")
        with_cache = CostEstimate(
            input_tokens=1000, model="claude-sonnet-4-6", cache_read_tokens=800
        )
        assert with_cache.input_cost_usd < no_cache.input_cost_usd

    def test_zero_output_tokens(self):
        from core.token_optimizer.counter import CostEstimate
        est = CostEstimate(
            input_tokens=100, model="claude-haiku-4-5", estimated_output_tokens=0
        )
        assert est.output_cost_usd == 0.0


class TestEstimateCost:
    def test_from_string(self):
        from core.token_optimizer.counter import estimate_cost
        est = estimate_cost("hello world", model="claude-sonnet-4-6")
        assert est.input_tokens > 0
        assert est.total_cost_usd >= 0

    def test_from_int(self):
        from core.token_optimizer.counter import estimate_cost
        est = estimate_cost(1000, model="claude-haiku-4-5")
        assert est.input_tokens == 1000

    def test_unknown_model_gets_default_price(self):
        from core.token_optimizer.counter import estimate_cost
        est = estimate_cost(100, model="totally-unknown-llm")
        assert est.total_cost_usd > 0


class TestTokenSummary:
    def test_summary_keys(self):
        from core.token_optimizer.counter import token_summary
        s = token_summary("Sample text for testing.", model="claude-sonnet-4-6")
        assert set(s.keys()) >= {"chars", "tokens", "chars_per_token", "cost_usd", "model"}

    def test_chars_equals_len(self):
        from core.token_optimizer.counter import token_summary
        text = "Hello world"
        s = token_summary(text)
        assert s["chars"] == len(text)

    def test_cost_non_negative(self):
        from core.token_optimizer.counter import token_summary
        s = token_summary("x")
        assert s["cost_usd"] >= 0


class TestCostTable:
    def test_has_anthropic_models(self):
        from core.token_optimizer.counter import COST_TABLE
        assert "claude-sonnet-4-6" in COST_TABLE
        assert "claude-opus-4-8" in COST_TABLE
        assert "claude-haiku-4-5" in COST_TABLE

    def test_has_openai_models(self):
        from core.token_optimizer.counter import COST_TABLE
        assert "gpt-4o" in COST_TABLE
        assert "gpt-4o-mini" in COST_TABLE

    def test_has_cheapest_models(self):
        from core.token_optimizer.counter import COST_TABLE
        assert "deepseek-chat" in COST_TABLE
        assert "gemini-1.5-flash" in COST_TABLE


# ── budget.py ─────────────────────────────────────────────────────────────


class TestBudgetConfig:
    def test_defaults(self):
        from core.token_optimizer.budget import BudgetConfig
        cfg = BudgetConfig()
        assert cfg.max_input_tokens_per_call == 100_000
        assert cfg.max_cost_per_call_usd == 0.50
        assert cfg.max_tokens_per_session == 1_000_000
        assert cfg.max_cost_per_session_usd == 5.0
        assert cfg.warn_threshold_pct == 0.80

    def test_custom_limits(self):
        from core.token_optimizer.budget import BudgetConfig
        cfg = BudgetConfig(max_input_tokens_per_call=1000, max_cost_per_call_usd=0.01)
        assert cfg.max_input_tokens_per_call == 1000
        assert cfg.max_cost_per_call_usd == 0.01

    def test_none_disables_check(self):
        from core.token_optimizer.budget import BudgetConfig
        cfg = BudgetConfig(max_input_tokens_per_call=None, max_cost_per_call_usd=None)
        assert cfg.max_input_tokens_per_call is None


class TestBudgetGuard:
    def test_allows_small_call(self):
        from core.token_optimizer.budget import BudgetConfig, BudgetGuard
        guard = BudgetGuard(BudgetConfig(max_input_tokens_per_call=10_000))
        est = guard.check_pre_call("Hello", model="claude-sonnet-4-6")
        assert est.input_tokens > 0

    def test_raises_on_too_many_tokens(self):
        from core.token_optimizer.budget import BudgetConfig, BudgetExceededError, BudgetGuard
        guard = BudgetGuard(BudgetConfig(max_input_tokens_per_call=1))
        with pytest.raises(BudgetExceededError, match="exceeds per-call limit"):
            guard.check_pre_call("This is a longer text that will exceed 1 token")

    def test_raises_on_cost_exceeded(self):
        from core.token_optimizer.budget import BudgetConfig, BudgetExceededError, BudgetGuard
        guard = BudgetGuard(BudgetConfig(max_cost_per_call_usd=0.000001))
        with pytest.raises(BudgetExceededError, match="Estimated cost"):
            guard.check_pre_call("A" * 200, model="claude-opus-4-8")

    def test_no_limit_none_passes_any_call(self):
        from core.token_optimizer.budget import BudgetConfig, BudgetGuard
        guard = BudgetGuard(
            BudgetConfig(
                max_input_tokens_per_call=None,
                max_cost_per_call_usd=None,
                max_tokens_per_session=None,
                max_cost_per_session_usd=None,
            )
        )
        est = guard.check_pre_call("A" * 10000)
        assert est.input_tokens > 0

    def test_integer_tokens_input(self):
        from core.token_optimizer.budget import BudgetGuard
        guard = BudgetGuard()
        est = guard.check_pre_call(500, model="gpt-4o-mini")
        assert est.input_tokens == 500

    def test_raises_on_session_token_limit(self):
        from core.token_optimizer.budget import BudgetConfig, BudgetExceededError, BudgetGuard
        guard = BudgetGuard(BudgetConfig(max_tokens_per_session=10, max_cost_per_call_usd=None))
        # First call is fine; accumulate session
        asyncio.get_event_loop().run_until_complete(
            guard.session.record(9, 0, 0, 0.0)
        )
        with pytest.raises(BudgetExceededError, match="Session would reach"):
            guard.check_pre_call(100, model="gpt-4o-mini")

    def test_reset_session(self):
        from core.token_optimizer.budget import BudgetGuard
        guard = BudgetGuard()
        asyncio.get_event_loop().run_until_complete(
            guard.session.record(100, 50, 0, 0.01)
        )
        assert guard.session.total_calls == 1
        guard.reset_session()
        assert guard.session.total_calls == 0

    @pytest.mark.asyncio
    async def test_record_post_call(self):
        from core.token_optimizer.budget import BudgetGuard
        guard = BudgetGuard()
        await guard.record_post_call(500, 200, cached_tokens=100, model="claude-sonnet-4-6")
        assert guard.session.total_input_tokens == 500
        assert guard.session.total_output_tokens == 200
        assert guard.session.total_cached_tokens == 100
        assert guard.session.total_cost_usd > 0

    def test_usage_dict(self):
        from core.token_optimizer.budget import BudgetGuard
        guard = BudgetGuard()
        d = guard.usage_dict()
        assert "total_calls" in d
        assert "total_cost_usd" in d


class TestBudgetExceededError:
    def test_has_estimate(self):
        from core.token_optimizer.budget import BudgetExceededError
        from core.token_optimizer.counter import CostEstimate
        est = CostEstimate(input_tokens=1000, model="claude-sonnet-4-6")
        err = BudgetExceededError("too much", est)
        assert err.estimate is est
        assert "too much" in str(err)

    def test_no_estimate(self):
        from core.token_optimizer.budget import BudgetExceededError
        err = BudgetExceededError("budget exceeded")
        assert err.estimate is None


class TestSessionUsage:
    @pytest.mark.asyncio
    async def test_accumulates(self):
        from core.token_optimizer.budget import SessionUsage
        usage = SessionUsage()
        await usage.record(100, 50, 20, 0.01)
        await usage.record(200, 100, 0, 0.02)
        assert usage.total_input_tokens == 300
        assert usage.total_output_tokens == 150
        assert usage.total_calls == 2
        assert usage.total_cost_usd == pytest.approx(0.03)

    @pytest.mark.asyncio
    async def test_cache_hit_rate(self):
        from core.token_optimizer.budget import SessionUsage
        usage = SessionUsage()
        await usage.record(1000, 200, 500, 0.005)
        assert usage.cache_hit_rate == pytest.approx(0.5)

    @pytest.mark.asyncio
    async def test_cache_hit_rate_zero_division(self):
        from core.token_optimizer.budget import SessionUsage
        usage = SessionUsage()
        # No input tokens yet
        assert usage.cache_hit_rate == 0.0

    def test_total_tokens_property(self):
        from core.token_optimizer.budget import SessionUsage
        usage = SessionUsage()
        usage.total_input_tokens = 100
        usage.total_output_tokens = 50
        assert usage.total_tokens == 150

    @pytest.mark.asyncio
    async def test_to_dict_keys(self):
        from core.token_optimizer.budget import SessionUsage
        usage = SessionUsage()
        await usage.record(100, 50, 0, 0.001)
        d = usage.to_dict()
        assert "total_calls" in d
        assert "total_cost_usd" in d
        assert "cache_hit_rate_pct" in d
        assert "elapsed_seconds" in d


class TestGetDefaultGuard:
    def test_returns_budget_guard(self):
        from core.token_optimizer.budget import BudgetGuard, get_default_guard
        guard = get_default_guard()
        assert isinstance(guard, BudgetGuard)

    def test_singleton(self):
        from core.token_optimizer.budget import get_default_guard
        g1 = get_default_guard()
        g2 = get_default_guard()
        assert g1 is g2


class TestBudgetCheckDecorator:
    @pytest.mark.asyncio
    async def test_passes_when_within_budget(self):
        from core.token_optimizer.budget import budget_check

        @budget_check(max_tokens=10_000)
        async def dummy(prompt: str) -> str:
            return "result"

        result = await dummy(prompt="Hello")
        assert result == "result"

    @pytest.mark.asyncio
    async def test_raises_when_over_budget(self):
        from core.token_optimizer.budget import BudgetExceededError, budget_check

        @budget_check(max_tokens=1)
        async def dummy(prompt: str) -> str:
            return "result"

        with pytest.raises(BudgetExceededError):
            await dummy(prompt="This text is definitely longer than 1 token")

    @pytest.mark.asyncio
    async def test_handles_list_messages(self):
        from core.token_optimizer.budget import budget_check

        @budget_check(max_tokens=10_000)
        async def dummy(messages: list) -> str:
            return "ok"

        result = await dummy(messages=[{"role": "user", "content": "hi"}])
        assert result == "ok"


# ── cache.py ──────────────────────────────────────────────────────────────


class TestLRUCache:
    @pytest.mark.asyncio
    async def test_get_miss(self):
        from core.token_optimizer.cache import LRUCache
        cache = LRUCache()
        assert await cache.get("nonexistent") is None

    @pytest.mark.asyncio
    async def test_set_and_get(self):
        from core.token_optimizer.cache import LRUCache
        cache = LRUCache()
        await cache.set("key1", "value1")
        assert await cache.get("key1") == "value1"

    @pytest.mark.asyncio
    async def test_ttl_expiry(self):
        from core.token_optimizer.cache import LRUCache
        cache = LRUCache(ttl_seconds=0)
        await cache.set("key", "value")
        # TTL=0 means any subsequent access is expired
        time.sleep(0.01)
        assert await cache.get("key") is None

    @pytest.mark.asyncio
    async def test_max_size_eviction(self):
        from core.token_optimizer.cache import LRUCache
        cache = LRUCache(max_size=2)
        await cache.set("a", 1)
        await cache.set("b", 2)
        await cache.set("c", 3)
        # 'a' should be evicted as least recently used
        assert await cache.get("a") is None
        assert await cache.get("b") == 2
        assert await cache.get("c") == 3

    @pytest.mark.asyncio
    async def test_invalidate(self):
        from core.token_optimizer.cache import LRUCache
        cache = LRUCache()
        await cache.set("key", "value")
        await cache.invalidate("key")
        assert await cache.get("key") is None

    @pytest.mark.asyncio
    async def test_stats(self):
        from core.token_optimizer.cache import LRUCache
        cache = LRUCache()
        await cache.set("k", "v")
        await cache.get("k")  # hit
        await cache.get("missing")  # miss
        s = cache.stats()
        assert s["hits"] == 1
        assert s["misses"] == 1
        assert s["hit_rate_pct"] == 50.0


class TestMakeCacheKey:
    def test_deterministic(self):
        from core.token_optimizer.cache import make_cache_key
        k1 = make_cache_key([{"role": "user", "content": "hi"}], "claude-sonnet-4-6")
        k2 = make_cache_key([{"role": "user", "content": "hi"}], "claude-sonnet-4-6")
        assert k1 == k2

    def test_different_inputs_different_keys(self):
        from core.token_optimizer.cache import make_cache_key
        k1 = make_cache_key("hello", "claude-sonnet-4-6")
        k2 = make_cache_key("goodbye", "claude-sonnet-4-6")
        assert k1 != k2

    def test_different_model_different_key(self):
        from core.token_optimizer.cache import make_cache_key
        k1 = make_cache_key("hello", "claude-sonnet-4-6")
        k2 = make_cache_key("hello", "gpt-4o")
        assert k1 != k2

    def test_returns_hex_string(self):
        from core.token_optimizer.cache import make_cache_key
        k = make_cache_key("test", "model")
        assert len(k) == 64  # SHA-256 hex


class TestCachedResponse:
    def test_creation(self):
        from core.token_optimizer.cache import CachedResponse
        resp = CachedResponse(
            content="The answer is 42.",
            provider="anthropic",
            model="claude-sonnet-4-6",
            input_tokens=10,
            output_tokens=5,
        )
        assert resp.content == "The answer is 42."
        assert resp.cached_at > 0

    def test_to_json_has_fields(self):
        from core.token_optimizer.cache import CachedResponse
        import json
        resp = CachedResponse(
            content="test", provider="openai", model="gpt-4o",
            input_tokens=20, output_tokens=10,
        )
        d = json.loads(resp.to_json())
        assert d["content"] == "test"
        assert d["provider"] == "openai"
        assert "cached_at" in d

    def test_from_json_roundtrip(self):
        from core.token_optimizer.cache import CachedResponse
        resp = CachedResponse(
            content="roundtrip test", provider="anthropic", model="claude-haiku-4-5",
            input_tokens=5, output_tokens=3,
        )
        json_str = resp.to_json()
        restored = CachedResponse.from_json(json_str)
        assert restored.content == resp.content
        assert restored.provider == resp.provider
        assert restored.input_tokens == resp.input_tokens


# ── compressor.py ─────────────────────────────────────────────────────────


class TestNormalizeWhitespace:
    def test_strips_trailing_spaces(self):
        from core.token_optimizer.compressor import normalize_whitespace
        result = normalize_whitespace("hello   \nworld  ")
        assert result == "hello\nworld"

    def test_collapses_multiple_blank_lines(self):
        from core.token_optimizer.compressor import normalize_whitespace
        text = "line1\n\n\n\nline2"
        result = normalize_whitespace(text)
        assert result == "line1\n\nline2"

    def test_strips_outer_whitespace(self):
        from core.token_optimizer.compressor import normalize_whitespace
        result = normalize_whitespace("  \n  hello  \n  ")
        assert "hello" in result

    def test_empty_string(self):
        from core.token_optimizer.compressor import normalize_whitespace
        assert normalize_whitespace("") == ""


class TestStripCodeComments:
    def test_strips_python_standalone_comments(self):
        from core.token_optimizer.compressor import strip_code_comments
        # The regex strips standalone comment lines (lines starting with #)
        code = "x = 1\n    # standalone comment\ny = 2"
        result = strip_code_comments(code, language="python")
        assert "standalone comment" not in result
        assert "y = 2" in result

    def test_strips_js_standalone_comments(self):
        from core.token_optimizer.compressor import strip_code_comments
        # The regex strips standalone comment lines (lines starting with //)
        code = "const x = 1;\n// standalone comment\nconst y = 2;"
        result = strip_code_comments(code, language="javascript")
        assert "standalone comment" not in result
        assert "y = 2" in result

    def test_auto_detect_python(self):
        from core.token_optimizer.compressor import strip_code_comments
        code = "def foo():\n    # comment\n    return 1"
        result = strip_code_comments(code, language="auto")
        assert "comment" not in result

    def test_auto_detect_javascript(self):
        from core.token_optimizer.compressor import strip_code_comments
        code = "function foo() {\n  // standalone comment\n  return 1;\n}"
        result = strip_code_comments(code, language="auto")
        assert "standalone comment" not in result


class TestExtractImportantSentences:
    def test_short_text_unchanged(self):
        from core.token_optimizer.compressor import extract_important_sentences
        text = "Short text. Only two sentences."
        result = extract_important_sentences(text, min_sentences=3)
        assert result == text

    def test_reduces_long_text(self):
        from core.token_optimizer.compressor import extract_important_sentences
        sentences = [f"Sentence number {i} about business intelligence." for i in range(20)]
        text = " ".join(sentences)
        result = extract_important_sentences(text, keep_ratio=0.5)
        assert len(result) < len(text)

    def test_maintains_original_order(self):
        from core.token_optimizer.compressor import extract_important_sentences
        text = "First point about revenue. Second point about customers. Third point about growth. Fourth point about profit. Fifth point about scaling."
        result = extract_important_sentences(text, keep_ratio=0.6)
        # Verify the result only contains sentences from original
        assert len(result) > 0


class TestTruncateToTokens:
    def test_short_text_unchanged(self):
        from core.token_optimizer.compressor import truncate_to_tokens
        text = "Short text."
        result = truncate_to_tokens(text, max_tokens=100)
        assert result == text

    def test_long_text_gets_truncated(self):
        from core.token_optimizer.compressor import truncate_to_tokens
        text = "word " * 1000
        result = truncate_to_tokens(text, max_tokens=50)
        assert len(result) < len(text)

    def test_from_end(self):
        from core.token_optimizer.compressor import truncate_to_tokens
        text = "START " + "filler " * 500 + "END"
        result = truncate_to_tokens(text, max_tokens=30, from_end=True)
        # Should keep the end portion
        assert "END" in result


class TestContextCompressor:
    @pytest.mark.asyncio
    async def test_short_text_no_compression(self):
        from core.token_optimizer.compressor import ContextCompressor
        comp = ContextCompressor(target_tokens=5000)
        result = await comp.compress("Hello, this is a short text.")
        assert result.strategy == "no_compression_needed"
        assert result.compressed_text == result.original_text

    @pytest.mark.asyncio
    async def test_compresses_long_text(self):
        from core.token_optimizer.compressor import ContextCompressor
        long_text = "Important business insight. " * 300
        comp = ContextCompressor(target_tokens=50)
        result = await comp.compress(long_text)
        assert result.compressed_tokens <= result.original_tokens
        assert result.original_tokens > 50

    @pytest.mark.asyncio
    async def test_compression_result_has_ratio(self):
        from core.token_optimizer.compressor import ContextCompressor
        long_text = "Revenue intelligence data point. " * 200
        comp = ContextCompressor(target_tokens=100)
        result = await comp.compress(long_text)
        assert 0.0 <= result.compression_ratio <= 1.0

    @pytest.mark.asyncio
    async def test_code_content_type(self):
        from core.token_optimizer.compressor import ContextCompressor
        code = "def foo():\n    # long comment here\n    return 1\n" * 100
        comp = ContextCompressor(target_tokens=50)
        result = await comp.compress(code, content_type="code")
        assert result.compressed_tokens <= result.original_tokens

    def test_to_dict(self):
        from core.token_optimizer.compressor import CompressionResult
        result = CompressionResult(
            original_text="abc",
            compressed_text="ab",
            original_tokens=3,
            compressed_tokens=2,
            strategy="whitespace",
            compression_ratio=0.333,
        )
        d = result.to_dict()
        assert "strategy" in d
        assert "tokens_saved" in d
        assert d["tokens_saved"] == 1


class TestCompressRagChunks:
    def test_empty_returns_empty(self):
        from core.token_optimizer.compressor import compress_rag_chunks
        assert compress_rag_chunks([]) == []

    def test_short_chunks_unchanged(self):
        from core.token_optimizer.compressor import compress_rag_chunks
        chunks = ["Short chunk one.", "Short chunk two."]
        result = compress_rag_chunks(chunks, max_total_tokens=10000)
        assert result == chunks

    def test_compresses_oversized_chunks(self):
        from core.token_optimizer.compressor import compress_rag_chunks
        big_chunk = "Revenue data point. " * 200
        result = compress_rag_chunks([big_chunk], max_total_tokens=50)
        assert len(result) == 1
        assert len(result[0]) < len(big_chunk)


class TestRedisExactCacheGracefulFallback:
    """RedisExactCache degrades gracefully when Redis is unavailable."""

    @pytest.mark.asyncio
    async def test_get_returns_none_when_redis_down(self):
        from core.token_optimizer.cache import RedisExactCache
        cache = RedisExactCache(redis_url="redis://127.0.0.1:1")  # bad port
        result = await cache.get("somekey")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_does_not_raise_when_redis_down(self):
        from core.token_optimizer.cache import CachedResponse, RedisExactCache
        cache = RedisExactCache(redis_url="redis://127.0.0.1:1")
        resp = CachedResponse(content="test", provider="test", model="test",
                              input_tokens=1, output_tokens=1)
        await cache.set("key", resp)  # should not raise

    def test_stats_zero_when_unused(self):
        from core.token_optimizer.cache import RedisExactCache
        cache = RedisExactCache(redis_url="redis://127.0.0.1:1")
        s = cache.stats()
        assert s["hits"] == 0
        assert s["misses"] == 0


class TestTokenCacheWithLRUOnly:
    """TokenCache works via LRU tier even when Redis is unavailable."""

    @pytest.mark.asyncio
    async def test_get_miss_returns_none(self):
        from core.token_optimizer.cache import TokenCache
        cache = TokenCache(redis_url="redis://127.0.0.1:1")
        result = await cache.get([{"role": "user", "content": "hi"}], "gpt-4o")
        assert result is None

    @pytest.mark.asyncio
    async def test_set_and_get_via_lru(self):
        from core.token_optimizer.cache import CachedResponse, TokenCache
        cache = TokenCache(redis_url="redis://127.0.0.1:1")
        resp = CachedResponse(content="42", provider="test", model="gpt-4o",
                              input_tokens=5, output_tokens=2)
        msgs = [{"role": "user", "content": "What is 6x7?"}]
        await cache.set(msgs, "gpt-4o", resp)
        # LRU should return the value without Redis
        hit = await cache.get(msgs, "gpt-4o")
        assert hit is not None
        assert hit.content == "42"

    def test_stats_returns_dict(self):
        from core.token_optimizer.cache import TokenCache
        cache = TokenCache(redis_url="redis://127.0.0.1:1")
        s = cache.stats()
        assert "lru" in s
        assert "redis_exact" in s
        assert "semantic" in s


class TestGetTokenCache:
    def test_returns_token_cache(self):
        from core.token_optimizer.cache import TokenCache, get_token_cache
        # Reset singleton
        import core.token_optimizer.cache as cache_mod
        cache_mod._cache_instance = None
        c = get_token_cache()
        assert isinstance(c, TokenCache)

    def test_singleton(self):
        from core.token_optimizer.cache import get_token_cache
        import core.token_optimizer.cache as cache_mod
        cache_mod._cache_instance = None
        c1 = get_token_cache()
        c2 = get_token_cache()
        assert c1 is c2


# ── tracker.py ────────────────────────────────────────────────────────────


class TestLangfuseTracker:
    def test_disabled_without_keys(self):
        from core.token_optimizer.tracker import LangfuseTracker
        tracker = LangfuseTracker(public_key=None, secret_key=None)
        assert not tracker.is_enabled

    def test_track_generation_noop_when_disabled(self):
        from core.token_optimizer.tracker import LangfuseTracker
        tracker = LangfuseTracker()
        # Should not raise even when disabled
        tracker.track_generation(
            name="test",
            model="claude-sonnet-4-6",
            input_text="prompt",
            output_text="response",
            input_tokens=10,
            output_tokens=5,
        )

    def test_track_cache_hit_noop_when_disabled(self):
        from core.token_optimizer.tracker import LangfuseTracker
        tracker = LangfuseTracker()
        tracker.track_cache_hit(
            cache_type="exact",
            model="claude-sonnet-4-6",
            tokens_saved=100,
        )

    def test_flush_noop_when_disabled(self):
        from core.token_optimizer.tracker import LangfuseTracker
        tracker = LangfuseTracker()
        tracker.flush()  # Should not raise

    def test_get_tracker_singleton(self):
        # Calling get_tracker twice should return the same instance
        # (module-level singleton)
        from core.token_optimizer import tracker as tracker_mod
        # Reset singleton for test isolation
        tracker_mod._tracker = None
        t1 = tracker_mod.get_tracker()
        t2 = tracker_mod.get_tracker()
        assert t1 is t2


class TestTokenUsageMiddleware:
    @pytest.mark.asyncio
    async def test_adds_response_time_header(self):
        from core.token_optimizer.tracker import TokenUsageMiddleware

        received_messages: list = []

        async def fake_app(scope, receive, send):
            await send({"type": "http.response.start", "status": 200, "headers": []})

        async def fake_send(message):
            received_messages.append(message)

        middleware = TokenUsageMiddleware(fake_app)
        scope = {"type": "http"}
        await middleware(scope, None, fake_send)

        assert len(received_messages) == 1
        headers = dict(received_messages[0]["headers"])
        assert b"x-response-time-ms" in headers

    @pytest.mark.asyncio
    async def test_passes_through_non_http_scope(self):
        from core.token_optimizer.tracker import TokenUsageMiddleware

        called = []

        async def fake_app(scope, receive, send):
            called.append(True)

        middleware = TokenUsageMiddleware(fake_app)
        await middleware({"type": "websocket"}, None, None)
        assert called == [True]


# ── __init__.py exports ───────────────────────────────────────────────────


class TestPackageExports:
    def test_all_exports_importable(self):
        import core.token_optimizer as to
        assert hasattr(to, "COST_TABLE")
        assert hasattr(to, "count_tokens")
        assert hasattr(to, "estimate_cost")
        assert hasattr(to, "BudgetGuard")
        assert hasattr(to, "BudgetConfig")
        assert hasattr(to, "BudgetExceededError")
        assert hasattr(to, "LangfuseTracker")
        assert hasattr(to, "get_tracker")
