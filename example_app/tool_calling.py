import json
import re
from typing import Annotated, List, cast

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.pydantic_v1 import BaseModel, Field, SecretStr
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from shared_module.config import EnvVar

llm = ChatOpenAI(
    api_key=SecretStr(EnvVar.openai_api_key),
    model="gpt-4o-mini",
)


@tool
def multiply_by_max(
    a: Annotated[int, "scalar factor"],
    b: Annotated[list[int], "list of integers over which to find the maximum"],
) -> int:
    """Multiply a by the maximum of b."""
    return a * max(b)


def too_calling_example() -> None:
    print(multiply_by_max.args_schema.schema())
    print(multiply_by_max.name)


if __name__ == "__main__":
    too_calling_example()
