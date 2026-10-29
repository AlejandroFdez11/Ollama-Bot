import asyncio
import httpx
from config import OLLAMA_URL, MODEL
from busqueda import buscar_web

TOOLS = [{
    "type": "function",
    "function": {
        "name": "buscar_web",
        "description": "Busca información actual en internet. Úsala para noticias, datos recientes, precios, resultados deportivos o cualquier cosa que puedas no saber.",
        "parameters": {
            "type": "object",
            "properties": {
                "consulta": {"type": "string", "description": "Texto de búsqueda"}
            },
            "required": ["consulta"],
        },
    },
}]

async def chat(messages):
    messages = list(messages)
    async with httpx.AsyncClient(timeout=300) as client:
        for _ in range(4):  # máximo 4 rondas de herramientas
            r = await client.post(f"{OLLAMA_URL}/api/chat", json={
                "model": MODEL,
                "messages": messages,
                "tools": TOOLS,
                "stream": False,
                "think": False,
                "keep_alive": "30m",
            })
            r.raise_for_status()
            msg = r.json()["message"]
            llamadas = msg.get("tool_calls")
            if not llamadas:
                return msg["content"]
            messages.append(msg)
            for c in llamadas:
                args = c["function"]["arguments"]
                resultado = await asyncio.to_thread(buscar_web, args.get("consulta", ""))
                messages.append({
                    "role": "tool",
                    "tool_name": c["function"]["name"],
                    "content": resultado,
                })
    return "No pude completar la búsqueda."