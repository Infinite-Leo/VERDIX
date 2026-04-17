from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .models.schemas import RunRequest
from .orchestrator import VerdixOrchestrator

load_dotenv()

app = FastAPI(title="VERDIX Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = VerdixOrchestrator()

@app.post("/api/run")
async def run_pipeline(request: RunRequest):
    try:
        result = await orchestrator.run_pipeline(request)
        return result.model_dump()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/api/history/{user_id}")
async def get_history(user_id: str):
    try:
        memory = orchestrator.memory_agent.load_memory(user_id)
        return {"user_id": user_id, "history": memory.past_purchases, "tx_history": memory.tx_history}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/api/memory/{user_id}")
async def get_memory(user_id: str):
    try:
        memory = orchestrator.memory_agent.load_memory(user_id)
        return memory.model_dump()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/health")
async def health_check():
    return {"status": "ok", "name": "VERDIX Backend"}
