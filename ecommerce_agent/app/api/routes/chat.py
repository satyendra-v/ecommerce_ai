from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from app.graph import compiled_graph

router = APIRouter(prefix="/multi-agent/chat")

class ChatRequest(BaseModel):
    sessionId: str
    message: str
    userId: str = "anonymous"

@router.post("/")
async def chat(req: ChatRequest):
    """
    Single-turn multi-agent chat.
    The supervisor routes to the right specialist, which responds, and the
    supervisor decides if FINISH or another round is needed.
    """
    result = await compiled_graph.ainvoke(
        {
            "messages": [HumanMessage(content=req.message)],
            "session_id": req.sessionId,
            "action_log": [],
        },
        config={"configurable": {"thread_id": req.sessionId}}
    )

    final_message = result["messages"][-1]
    agent_name = getattr(final_message, "name", "assistant")

    return {
        "response": final_message.content,
        "agent": agent_name,
        "action_log": result.get("action_log", []),
    }

@router.get("/stream")
async def stream_chat(session_id: str, message: str):
    """
    Streaming version: returns tokens as SSE as the agent generates them.
    The browser sees the response appear word by word.
    """
    async def event_generator():
        async for event in compiled_graph.astream_events(
            {
                "messages": [HumanMessage(content=message)],
                "session_id": session_id,
                "action_log": [],
            },
            config={"configurable": {"thread_id": session_id}},
            version="v2"
        ):
            # astream_events yields many event types.
            # We only care about token chunks from the LLM.
            if event["event"] == "on_chat_model_stream":
                chunk = event["data"]["chunk"].content
                if chunk:
                    yield f"data: {chunk}\n\n"   # SSE format

        yield "data: [DONE]\n\n"  # Signal stream end to the client

    return StreamingResponse(event_generator(), media_type="text/event-stream")