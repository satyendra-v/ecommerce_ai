from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from model import llm
from orchestration import AgentState

import os

_mcp_client = None
_ops_agent = None

# Operations Agent with MCP Tools

async def initialize_ops_agent():
    """
    Called once at startup. Connects to Spring Boot MCP server and builds the agent.
    The connection stays open for the lifetime of the service.
    If connection fails, the agent will be unavailable (but the service continues).
    """
    global _mcp_client, _ops_agent
    try:
        _mcp_client = MultiServerMCPClient({
            "ecommerce": {"url": "http://localhost:8080/sse", "transport": "sse"}
        })
        # Get tools without using context manager
        tools = await _mcp_client.get_tools()

        _ops_agent = create_react_agent(
            model=llm,
            tools=tools,
            state_modifier=(
                "You are an operations agent with access to order, inventory, and support tools. "
                "Use the available tools to fulfill the user's request. "
                "For refunds, always confirm the order exists first. "
                "After completing an action, summarize what you did clearly."
            )
        )
        print("✓ Operations agent connected to MCP server")
    except Exception as e:
        print(f"⚠ Warning: Could not connect to MCP server: {e}")
        print("  Operations agent will not be available")
        _ops_agent = None

async def operations_node(state: AgentState) -> dict:
    """
    Operations agent: uses MCP tools to perform actions on the Spring Boot system.
    Handles orders, refunds, tickets, inventory updates.
    """
    if _ops_agent is None:
        return {
            "messages": [AIMessage(
                content="Sorry, the operations agent is currently unavailable because the MCP server is not connected. Please ensure the Spring Boot backend is running on localhost:8080.",
                name="operations_agent"
            )],
            "action_log": [{"node": "operations", "status": "unavailable"}],
        }
    
    result = await _ops_agent.ainvoke({"messages": state["messages"]})
    final_answer = result["messages"][-1].content

    # Count how many tool calls were made (for observability)
    tool_calls = sum(
        1 for m in result["messages"]
        if hasattr(m, "tool_calls") and m.tool_calls
    )

    return {
        "messages": [AIMessage(content=final_answer, name="operations_agent")],
        "action_log": [{"node": "operations", "mcp_tool_calls": tool_calls}],
    }