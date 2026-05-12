from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field
from state import AgentState
from model import llm
import os
from dotenv import load_dotenv

load_dotenv()

# Research Agent with Web Search + Structured Output

# ── WEB SEARCH TOOL ───────────────────────────────────────────────────────────
# TavilySearch is optimized for LLM use — returns clean, summarized results.
# Alternative: DuckDuckGoSearchRun (free, no API key required)
_search_tool = None
_research_agent = None
_report_llm = None

def _initialize_search_tool():
    """Lazy initialize search tool - only if API key is available"""
    global _search_tool, _research_agent, _report_llm
    
    if _search_tool is not None:
        return
    
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    
    if tavily_api_key:
        _search_tool = TavilySearchResults(
            max_results=5,
            include_answer=True,     # Includes Tavily's own summary of results
            include_raw_content=False
        )
    else:
        # Fallback: Use DuckDuckGo which doesn't require API key
        from langchain_community.tools import DuckDuckGoSearchRun
        _search_tool = DuckDuckGoSearchRun()

# ── STRUCTURED RESEARCH OUTPUT ────────────────────────────────────────────────
class ResearchReport(BaseModel):
    """Structured output from the research agent."""
    topic: str = Field(description="The main topic researched")
    key_findings: list[str] = Field(description="List of 3-5 key findings")
    sources: list[str] = Field(description="List of source URLs used")
    confidence: str = Field(description="high, medium, or low confidence in findings")
    recommendation: str = Field(description="Actionable recommendation based on research")

# Two-phase research: first gather info with tools, then structure the output.
def _get_research_agent():
    """Lazy initialize research agent"""
    global _research_agent, _report_llm
    
    if _research_agent is None:
        _initialize_search_tool()
        _research_agent = create_react_agent(
            model=llm,
            tools=[_search_tool],
            state_modifier=(
                "You are a research agent. Search the web to find current, accurate information. "
                "After searching, synthesize findings into a clear, factual response. "
                "Always cite sources and note confidence level."
            )
        )
        _report_llm = llm.with_structured_output(ResearchReport)
    
    return _research_agent, _report_llm

async def research_node(state: AgentState) -> dict:
    """
    Research agent: performs web searches and returns structured findings.
    Two phases: (1) ReAct agent gathers info, (2) structured output extracts report.
    """
    research_agent, report_llm = _get_research_agent()
    
    # Phase 1: Use ReAct agent to search and gather information
    agent_result = await research_agent.ainvoke({"messages": state["messages"]})
    raw_answer = agent_result["messages"][-1].content

    # Phase 2: Structure the raw answer into a ResearchReport
    from langchain_core.messages import HumanMessage as HM
    report: ResearchReport = await report_llm.ainvoke([
        HM(content=f"Convert this research into a structured report:\n\n{raw_answer}")
    ])

    # Format the report as a readable message
    formatted = (
        f"**Research Report: {report.topic}**\n\n"
        f"**Key Findings:**\n" +
        "\n".join(f"• {f}" for f in report.key_findings) +
        f"\n\n**Confidence:** {report.confidence}\n"
        f"**Recommendation:** {report.recommendation}\n\n"
        f"**Sources:** {', '.join(report.sources)}"
    )

    return {
        "messages": [AIMessage(content=formatted, name="research_agent")],
        "action_log": [{"node": "research", "confidence": report.confidence}],
    }
def test_research_node(state: AgentState) :
    print("INVOKED RESEARCH NODE")