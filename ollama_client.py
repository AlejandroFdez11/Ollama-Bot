import asyncio
import json
import httpx
from config import API_KEY, API_URL, MODEL
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
    headers = {"Authorization": f"Bearer {API_KEY}"}
    async with httpx.AsyncClient(timeout=120) as client:
        for _ in range(4):  # máximo 4 rondas de herramientas
            r = await client.post(API_URL, headers=headers, json={
                "model": MODEL,
                "messages": messages,
                "tools": TOOLS,
            })
            if r.status_code >= 400:
                raise RuntimeError(f"{r.status_code}: {r.text[:300]}")
            msg = r.json()["choices"][0]["message"]
            llamadas = msg.get("tool_calls")
            if not llamadas:
                return msg.get("content") or "Sin respuesta."
            messages.append({
                "role": "assistant",
                "content": msg.get("content") or "",
                "tool_calls": llamadas,
            })
            for c in llamadas:
                try:
                    args = json.loads(c["function"]["arguments"] or "{}")
                except json.JSONDecodeError:
                    args = {}
                resultado = await asyncio.to_thread(buscar_web, args.get("consulta", ""))
                messages.append({
                    "role": "tool",
                    "tool_call_id": c["id"],
                    "name": c["function"]["name"],
                    "content": resultado,
                })
    return "No pude completar la búsqueda."