from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    query: str = Field(
        description="Search query for DuckDuckGo search, separated by comma.",
    )


class SearchResultItem(BaseModel):
    content: str = Field(
        description="The content of the search result.",
    )


class SearchResult(BaseModel):
    success: bool = Field(
        description="Whether the search was successful.",
    )
    error_message: str | None = Field(
        description="Error message if the search failed.",
        default_factory=lambda: None,
    )
    content: list[SearchResultItem] = Field(
        description="The search results.",
        default_factory=lambda: [],
    )


class DDGSearchState(BaseModel):
    query: str = Field(description="The user's query.")
    parsed_query: str | None = Field(
        description="The parsed query from the user's input.",
        default_factory=lambda: None,
    )
    search_result: SearchResult | None = Field(
        description="The current search result.",
        default_factory=lambda: None,
    )


class AgentInput(BaseModel):
    query: str = Field(description="The user's query.")


class AgentOutput(BaseModel):
    search_result: SearchResult = Field(
        description="The agent's response.",
    )
