import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.agents.ecommerce_agent import tools
from app.agents.operations_agent import initialize_ops_agent
from app.api.routes import rag, health, chat, tools

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to all external systems on startup."""
    await initialize_ops_agent()   # Connect to Spring Boot MCP server
    yield
    # Cleanup happens here on shutdown

app = FastAPI(title="Multi-Agent Orchestration", lifespan=lifespan)

app.include_router(rag.router)
app.include_router(health.router)
app.include_router(chat.router)
app.include_router(tools.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)