from typing import Any, Coroutine

from duckduckgo_search import DDGS

from example_app.dataloader.duckduckgo.model import (
    DDGSearchState,
    SearchResult,
    SearchResultItem,
)


class DuckDuckGoTextSearch:
    name = "DuckDuckGo Search"
    description = "A tool that uses DuckDuckGo to search for information."

    def __init__(self, search_engine: DDGS) -> None:
        self.search_engine = search_engine

    def run(self, state: DDGSearchState) -> dict[str, Any]:
        region = "ja-JP"
        words = state.parsed_query or ""
        results = self.search_engine.text(
            keywords=words,
            region=region,
            max_results=10,
        )
        search_result = []
        for result in results:
            search_result.append(SearchResultItem(content=result["body"]))
        state.search_result = SearchResult(success=True, content=search_result)
        return state.model_dump()
