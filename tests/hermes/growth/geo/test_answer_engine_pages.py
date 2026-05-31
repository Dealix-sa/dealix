"""Answer-engine pages register with target queries and citation assets."""

from __future__ import annotations

from dealix.hermes.growth.geo.answer_engine_pages import list_pages, register, reset


def test_register_and_list_pages() -> None:
    reset()
    p = register("AI sales benchmark", "/blog/ai-sales-benchmark", ["best ai sales"], ["asset_a"])
    pages = list_pages()
    assert p.page_id in {x.page_id for x in pages}
    assert pages[-1].target_queries == ("best ai sales",)
