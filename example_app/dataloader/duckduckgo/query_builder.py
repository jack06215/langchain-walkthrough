from typing import Any, cast

import openai
from openai import OpenAI

from example_app.dataloader.duckduckgo.model import DDGSearchState, SearchQuery
from shared_module.config import EnvVar


class QueryBuilder:
    name: str = "query_builder"
    description: str = "Generates search query based on user's input."

    def __init__(self) -> None:
        pass

    def run(self, state: DDGSearchState) -> dict[str, Any]:
        client = OpenAI(api_key=EnvVar.openai_api_key)
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. When prompted, generate search query for DuckDuckGo search.",
                },
                {
                    "role": "user",
                    "content": f"Help me generate search query for DuckDuckGo search: {state.query}",
                },
            ],
            tools=[
                openai.pydantic_function_tool(SearchQuery),
            ],
            tool_choice="required",
        )
        message = completion.choices[0].message
        if message.tool_calls is not None:
            result = cast(
                SearchQuery,
                message.tool_calls[0].function.parsed_arguments,
            )

            # print(SearchQuery(**result["tool_calls"][0]["function"]["arguments"]))
            state.parsed_query = result.query

        return state.model_dump()
