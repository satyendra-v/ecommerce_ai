from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

import os
from dotenv import load_dotenv

from app.tools import *

load_dotenv()

ai_model = os.getenv("AI_MODEL")
ai_endpoint = os.getenv("AI_ENDPOINT")
ai_api_key = os.getenv("AI_API_KEY")

llm = ChatOpenAI(
            model=ai_model,
            base_url=ai_endpoint,
            api_key=ai_api_key,
            temperature=0
        )

tools = [search_products]

agent = create_react_agent(
    model=llm,
    tools=tools,
)

def run_agent(user_message: str) -> str :
    """
        Runs the full ReAct loop for a given user message.
        Returns the final text response.
    """
    print(f"user message: {user_message}")
    result = agent.invoke({
        "messages": [HumanMessage(content=user_message)]
    })

    final_message = result["messages"][-1]

    print(f"final message: {final_message}")

    return final_message.content


# MemorySaver stores the agent's state (full message history) between invocations.
# Use a database-backed checkpointer (SqliteSaver, PostgresSaver) in production.
memory = MemorySaver()

stateful_agent = create_react_agent(
    model=llm,
    tools=tools,
    checkpointer=memory,   # ← this enables memory across turns
)

def run_stateful_agent(session_id: str, user_message: str) -> str:
    # thread_id links multiple invocations into one conversation
    config = {"configurable": {"thread_id": session_id}}
    result = stateful_agent.invoke(
        {"messages": [HumanMessage(content=user_message)]},
        config=config
    )
    return result["messages"][-1].content