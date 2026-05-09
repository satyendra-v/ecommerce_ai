from typing import TypedDict, Annotated, Literal
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import operator

# AgentState defines what every node in the graph receives and returns.
# TypedDict means this is a typed dictionary — no class methods, just fields.
class AgentState(TypedDict):
    # messages: the conversation history
    # add_messages is a "reducer" — it appends new messages to the list
    # instead of replacing the whole list on each state update.
    messages: Annotated[list[BaseMessage], add_messages]

    # next: which agent the supervisor routes to
    next: Literal["support", "operations", "research", "FINISH"]

    # session_id: links to per-user conversation memory
    session_id: str

    # structured_log: list of actions taken (for observability)
    action_log: Annotated[list[dict], operator.add]