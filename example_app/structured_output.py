import json
import re
from typing import List, cast

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.pydantic_v1 import BaseModel, Field, SecretStr
from langchain_openai import ChatOpenAI

from shared_module.config import EnvVar

llm = ChatOpenAI(
    api_key=SecretStr(EnvVar.openai_api_key),
    model="gpt-4o-mini",
)


class Joke(BaseModel):
    """Joke to tell user."""

    setup: str = Field(description="The setup of the joke.")
    punchline: str = Field(description="The punchline of the joke.")
    rating: int | None = Field(
        description="How funny the joke is, from 1 to 10",
        default=None,
    )


class ConversationalResponse(BaseModel):
    """Response in a conversational manner. Be kind and helpful."""

    response: str = Field(description="A conversational response to user's query.")


class Response(BaseModel):
    output: Joke | ConversationalResponse


class Person(BaseModel):
    """Information about a person."""

    name: str = Field(description="The name of the person")
    height_in_meters: float = Field(
        description="The height of the person expressed in meters."
    )


class People(BaseModel):
    """Identifying information about all people in a text."""

    people: List[Person]


def extract_json(message: AIMessage) -> List[dict]:
    """Extracts JSON content from a string where JSON is embedded between ```json and ``` tags.

    Parameters:
        text (str): The text containing the JSON content.

    Returns:
        list: A list of extracted JSON strings.
    """
    text = cast(str, message.content)
    # Define the regular expression pattern to match JSON blocks
    pattern = r"```json(.*?)```"

    # Find all non-overlapping matches of the pattern in the string
    matches = re.findall(pattern, text, re.DOTALL)

    # Return the list of matched JSON strings, stripping any leading or trailing whitespace
    try:
        return [json.loads(match.strip()) for match in matches]
    except Exception:
        raise ValueError(f"Failed to parse: {message}")


def simple_structured_output() -> None:
    structured_llm = llm.with_structured_output(Response)
    message = structured_llm.invoke("Tell me a joke about cats.")
    print(message)
    message = structured_llm.invoke("How are you today?")
    print(message)


def choosing_between_multiple_schema() -> None:
    print(Response.schema_json(indent=2))


def custom_parsing() -> None:
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                "Answer the user query. Output your answer as JSON that  "
                "matches the given schema: ```json\n{schema}\n```. "
                "Make sure to wrap the answer in ```json and ``` tags",
            ),
            HumanMessagePromptTemplate.from_template("{query}"),
        ]
    ).partial(schema=People.schema())

    query = "Anna is 23 years old and she is 6 feet tall"
    # print(prompt.format_prompt(query=query).to_string())

    chain = prompt | llm | extract_json
    message = chain.invoke({"query": query})
    print(message[0])


if __name__ == "__main__":
    custom_parsing()
