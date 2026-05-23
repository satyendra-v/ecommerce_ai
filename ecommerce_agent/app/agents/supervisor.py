from langchain_core.messages import SystemMessage
from pydantic import BaseModel
from typing import Literal

from app.utils.model import llm
from app.state import AgentState
from app.prompts import supervisor_prompt

# ── ROUTING SCHEMA ────────────────────────────────────────────────────────────
# The supervisor's ONLY job is to read the user's message and decide
# which specialist agent should handle it. We use structured output
# to guarantee a valid routing decision (never "I'll route to the best one").
class RoutingDecision(BaseModel):
    """The supervisor's routing decision."""
    next: Literal["support", "operations", "research", "FINISH"]
    reasoning: str  # Why this route was chosen (for observability)

# Bind the routing schema — supervisor MUST output a valid RoutingDecision
supervisor_llm = llm.with_structured_output(RoutingDecision)

def supervisor_node(state: AgentState) -> dict:
    """
    The supervisor node. Reads the full message history and decides next agent.
    Returns a partial state update — only the fields that changed.
    """
    messages = [SystemMessage(content=supervisor_prompt)] + state["messages"]

    decision: RoutingDecision = supervisor_llm.invoke(messages)

    # Log the routing decision for observability
    log_entry = {
        "node": "supervisor",
        "routed_to": decision.next,
        "reasoning": decision.reasoning,
    }

    print(f"supervisor_node: log_entry: {log_entry}")
    print(f"supervisor_node: next node: {decision.next}")

    return {
        "next": decision.next,
        "action_log": [log_entry],
    }