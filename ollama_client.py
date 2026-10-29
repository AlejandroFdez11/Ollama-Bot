import httpx
from config import OLLAMA_URL, MODEL

async def chat(messages):
    async with httpx.AsyncClient(timeout=300) as client:
        r = await client.post(f"{OLLAMA_URL}/api/chat", json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
        })
        r.raise_for_status()
        return r.json()["message"]["content"]