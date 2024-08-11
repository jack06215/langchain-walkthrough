import asyncio

from duckduckgo_search import DDGS

from example_app.dataloader.duckduckgo.agent import DDGSearchAgent
from example_app.dataloader.duckduckgo.model import AgentInput


async def main():
    duckduckgo_search = DDGS()

    request = AgentInput(query="What is the capital of France?")
    ddg_search_agent = DDGSearchAgent(search_engine=duckduckgo_search)

    result = await ddg_search_agent.run(request)
    # print(result.search_result.content)


if __name__ == "__main__":
    asyncio.run(main())
