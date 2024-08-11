import asyncio

from example_app.dataloader.duckduckgo.agent import DDGSearchAgent
from example_app.dataloader.duckduckgo.model import AgentInput


async def main():
    request = AgentInput(query="What is the capital of France?")
    ddg_search_agent = DDGSearchAgent()
    result = await ddg_search_agent.run(request)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
