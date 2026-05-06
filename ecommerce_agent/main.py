import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from agents import run_agent, run_stateful_agent

app = FastAPI(title="Agent Service")

class AgentRequest(BaseModel):
    message: str

@app.post("/agent/chat")
async def agent_chat(req: AgentRequest):
    response = run_agent(req.message)
    return {"response": response}


class StatefulRequest(BaseModel):
    session_id: str
    message: str

@app.post("/agent/stateful")
async def stateful_chat(req: StatefulRequest):
    response = run_stateful_agent(req.session_id, req.message)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)