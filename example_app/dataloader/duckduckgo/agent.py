from langgraph.graph import END, StateGraph

from example_app.dataloader.duckduckgo.model import (
    AgentInput,
    AgentOutput,
    DDGSearchState,
    SearchResult,
)
from example_app.dataloader.duckduckgo.text_search import DuckDuckGoTextSearch


class DDGSearchAgent:
    """An agent that uses DuckDuckGo to search for information."""

    def init_graph(self) -> StateGraph:
        duckduckgo_search_tool = DuckDuckGoTextSearch()

        workflow = StateGraph(state_schema=DDGSearchState)
        workflow.add_node("search_duckduckgo", duckduckgo_search_tool.run)
        workflow.add_edge("search_duckduckgo", END)

        workflow.set_entry_point("search_duckduckgo")

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
        result = DDGSearchState(**res)
        output = AgentOutput(
            search_result=result.search_result,
        )
        return output
