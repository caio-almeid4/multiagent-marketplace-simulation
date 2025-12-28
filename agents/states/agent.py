from operator import add
from typing import Annotated, List

from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict

from schemas.message import Message


class AgentState(TypedDict):
    cash: Annotated[float, "Agent's total amount of money", add]
    apple: Annotated[float, "Agent's otal amount of apples", add]
    chip: Annotated[float, "Agent's total amount of chips", add]
    gold: Annotated[float, "Agent's Total amount of money", add]
    internal_monologue: Annotated[str, "Scratchpad to agent reasoning"]
    inbox: Annotated[List[Message], "List with messages from other agents"]
    messages: Annotated[
        List[AnyMessage], "List of messages that will be passed to the agent"
    ]
