from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state import AgentState
from agents.supervisor import supervisor_node
from agents.support_agent import support_node
from agents.operations_agent import operations_node, initialize_ops_agent
from agents.research_agent import research_node
from agents import test_support_node, test_research_node, test_operations_node



def build_graph():
    """
    Builds the full multi-agent LangGraph StateGraph.

    The graph has:
      - A supervisor node that routes to sub-agents
      - Three specialist nodes (support, operations, research)
      - Conditional edges: after each sub-agent, return to supervisor
      - Terminal condition: supervisor outputs FINISH
    """

    # StateGraph is LangGraph's core primitive.
    # It defines a directed graph where nodes are Python functions and
    # edges define the allowed transitions between them.
    graph = StateGraph(AgentState)

    # ── ADD NODES ─────────────────────────────────────────────────────────
    # Each node is a function: (state) → partial_state_update
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("support", support_node)
    graph.add_node("operations", operations_node)
    graph.add_node("research", research_node)

    # ── ENTRY POINT ───────────────────────────────────────────────────────
    # Every request starts at the supervisor
    graph.set_entry_point("supervisor")

    # ── CONDITIONAL EDGES FROM SUPERVISOR ────────────────────────────────
    # After the supervisor runs, look at state["next"] to decide where to go.
    # The lambda is a "routing function" — maps the current state to the next node name.
    graph.add_conditional_edges(
        "supervisor",                    # From this node
        lambda state: state["next"],     # Call this function to decide next node
        {
            "support": "support",
            "operations": "operations",
            "research": "research",
            "FINISH": END,               # END is a special LangGraph constant
        }
    )

    # ── EDGES BACK TO SUPERVISOR ──────────────────────────────────────────
    # After any specialist agent runs, always go back to the supervisor.
    # The supervisor then decides: route again OR output FINISH.
    # This enables multi-turn agent collaboration:
    # supervisor → support → supervisor → operations → supervisor → FINISH
    # graph.add_edge("support", "supervisor")
    # graph.add_edge("operations", "supervisor")
    # graph.add_edge("research", "supervisor")

    # ── COMPILE ───────────────────────────────────────────────────────────
    # compile() validates the graph structure and returns a runnable.
    # Use checkpointer for persistence across invocations.
    checkpointer = MemorySaver()

    return graph.compile(checkpointer=checkpointer)

compiled_graph = build_graph()