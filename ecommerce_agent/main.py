import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from langchain_core.messages import HumanMessage
from agents.operations_agent import initialize_ops_agent
from agents import compiled_graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to all external systems on startup."""
    await initialize_ops_agent()   # Connect to Spring Boot MCP server
    yield
    # Cleanup happens here on shutdown

app = FastAPI(title="Multi-Agent Orchestration", lifespan=lifespan)

class ChatRequest(BaseModel):
    sessionId: str
    message: str
    userId: str = "anonymous"

@app.post("/chat")
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

@app.get("/chat/stream")
async def stream_chat(sessionId: str, message: str):
    """
    Streaming version: returns tokens as SSE as the agent generates them.
    The browser sees the response appear word by word.
    """
    async def event_generator():
        async for event in compiled_graph.astream_events(
            {
                "messages": [HumanMessage(content=message)],
                "session_id": sessionId,
                "action_log": [],
            },
            config={"configurable": {"thread_id": sessionId}},
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

@app.get("/health")
async def health():
    return {"status": "ok", "agents": ["supervisor", "support", "operations", "research"]}



from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import tempfile
from rag.ingestion import ingest_document
from rag.retrieval import query_rag
import os

# ── INGESTION ENDPOINT ────────────────────────────────────────────────────────
@app.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    collection: str = Form(default="default"),
    tags: str = Form(default="")
):
    # Write uploaded bytes to a temp file so loaders (PyPDFLoader etc.) can open it
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f".{file.filename.split('.')[-1]}"
    ) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        result = ingest_document(tmp_path, file.filename, collection, tags)
        return result
    finally:
        os.unlink(tmp_path)   # Always clean up the temp file

# ── QUERY ENDPOINT ────────────────────────────────────────────────────────────
class QueryRequest(BaseModel):
    question: str
    collection: str = "default"
    topK: int = 4
    citeSources: bool = True

@app.post("/query")
async def query(req: QueryRequest):
    try:
        result = query_rag(req.question, req.collection, req.topK, req.citeSources)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_docs(collection: str = "default"):
    from langchain_chroma import Chroma
    from langchain_openai import OpenAIEmbeddings
    store = Chroma(
        collection_name=collection,
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-small"),
        persist_directory="./chroma_db"
    )
    # Get all stored metadata
    data = store.get()
    seen = set()
    files = []
    for meta in data["metadatas"]:
        src = meta.get("source_file", "unknown")
        if src not in seen:
            seen.add(src)
            files.append({"file": src, "collection": collection})
    return {"documents": files, "total_chunks": len(data["ids"])}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)