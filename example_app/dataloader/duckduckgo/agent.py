from duckduckgo_search import DDGS
from langgraph.graph import END, StateGraph

from example_app.dataloader.duckduckgo.model import (
    AgentInput,
    AgentOutput,
    DDGSearchState,
    SearchResult,
)
from example_app.dataloader.duckduckgo.query_builder import QueryBuilder
from example_app.dataloader.duckduckgo.text_search import DuckDuckGoTextSearch


class DDGSearchAgent:
    """An agent that uses DuckDuckGo to search for information."""

    def __init__(self, search_engine: DDGS) -> None:
        self.search_engine = search_engine

    def init_graph(self) -> StateGraph:
        query_builder = QueryBuilder()
        duckduckgo_search_tool = DuckDuckGoTextSearch(search_engine=self.search_engine)

        workflow = StateGraph(state_schema=DDGSearchState)
        workflow.add_node("query_builder", query_builder.run)
        workflow.add_node("search_duckduckgo", duckduckgo_search_tool.run)


        workflow.add_edge("query_builder", "search_duckduckgo")
        workflow.add_edge("search_duckduckgo", END)

        workflow.set_entry_point("query_builder")

        return workflow

    async def run(self, input: AgentInput) -> AgentOutput:
        graph = self.init_graph().compile()
        initial_state = DDGSearchState(query=input.query)
        res = await graph.ainvoke(input=initial_state)
        result = DDGSearchState(**res)
        output = AgentOutput(
            search_result=result.search_result,
        )
        return output
