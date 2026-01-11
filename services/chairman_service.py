from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI(title="LLM Council - Chairman")

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "mistral" 

class ChatRequest(BaseModel):
    messages: list[dict]

class ChatResponse(BaseModel):
    content: str

async def call_ollama(messages: list[dict]) -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["message"]["content"]

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    answer = await call_ollama(req.messages)
    return ChatResponse(content=answer)
