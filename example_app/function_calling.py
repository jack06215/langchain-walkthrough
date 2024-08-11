from enum import Enum
from textwrap import dedent

import openai
from openai import OpenAI
from pydantic import BaseModel

from shared_module.config import EnvVar


class Table(str, Enum):
    orders = "orders"
    customers = "customers"
    products = "products"


class Column(str, Enum):
    id = "id"
    status = "status"
    expected_delivery_date = "expected_delivery_date"
    delivered_at = "delivered_at"
    shipped_at = "shipped_at"
    ordered_at = "ordered_at"
    canceled_at = "canceled_at"


class Operator(str, Enum):
    eq = "="
    gt = ">"
    lt = "<"
    le = "<="
    ge = ">="
    ne = "!="


class OrderBy(str, Enum):
    asc = "asc"
    desc = "desc"


class DynamicValue(BaseModel):
    column_name: str


class Condition(BaseModel):
    column: str
    operator: Operator
    value: str | int | DynamicValue


class Query(BaseModel):
    table_name: Table
    columns: list[Column]
    conditions: list[Condition]
    order_by: OrderBy


class PretrainedKnowledge(BaseModel):
    answer: str


client = OpenAI(api_key=EnvVar.openai_api_key)

SYSTEM_MESSAGE = dedent(
    """
You are a helpful assistant. The current date is August 6, 2024. Answer user's query using the provided tools.
- Query: Help users query for the data they are looking for.
- PretrainedKnowledge: A tool that provides ChatGPT pre-trained knowledge.
"""
)
completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_MESSAGE,
        },
        {
            "role": "user",
            "content": "hello there",
        },
    ],
    tools=[
        openai.pydantic_function_tool(Query),
        openai.pydantic_function_tool(PretrainedKnowledge),
    ],
    tool_choice="required",
)

print(completion.choices[0].message.model_dump())
