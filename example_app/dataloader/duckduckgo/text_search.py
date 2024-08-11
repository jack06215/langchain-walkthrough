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

    def run(self, state: DDGSearchState) -> dict[str, Any]:
        region = "ja-JP"
        words = "weather tomorrow"
        results = DDGS().text(
            keywords=words,
            region=region,
        )
        search_result = []
        for result in results:
            search_result.append(SearchResultItem(content=result["body"]))
        state.search_result = SearchResult(success=True, content=search_result)
        return state.model_dump()
