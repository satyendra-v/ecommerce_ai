from fastapi import APIRouter
from langchain_core.messages import HumanMessage, ToolMessage

from app.utils.model import llm
from app.tools.ecommerce_tools import *

router = APIRouter(prefix="/tools")

class Input(BaseModel):
    query: str

@router.post("/details")
async def tool_details(request : Input) :

    model_with_tools = llm.bind_tools(get_tools())

    response = model_with_tools.invoke([HumanMessage(content=request.query)])

    result = {}

    if response.tool_calls and len(response.tool_calls) > 0 :
        tool_call = response.tool_calls[0]
        result["name"] = tool_call['name']
        result["args"] = tool_call['args']

    print(f"result : {result}")

    return result

# execute tool with tool map
@router.post("/execute")
def execute_tool(request: Input) :

    messages = [
        HumanMessage(content=request.query)
    ]
    model_with_tools = llm.bind_tools(get_tools())

    ai_response = model_with_tools.invoke(messages)

    print(f"ai_response : {ai_response}")
    messages.append(ai_response)

    for tool_call in ai_response.tool_calls:

        tool_name = tool_call['name']
        tool_args = tool_call['args']

        result = tools[tool_name].invoke(tool_args)

        print(f"result : {result}")

        messages.append(
            ToolMessage(content=str(result), tool_call_id=tool_call["id"])
        )

    print(f"messages : {messages}")

    final_response = model_with_tools.invoke(messages)

    print(f"final response : {final_response.content}")

    return final_response.content

#TODO: execute tool with agent