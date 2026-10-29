from collections import defaultdict

MAX_MENSAJES = 20
SISTEMA = {"role": "system", "content": "Eres un asistente útil. Responde en español con andaluz, de forma concisa y con un toque gracioso."}

_historial = defaultdict(list)

def obtener(user_id):
    return [SISTEMA] + _historial[user_id]

def añadir(user_id, role, content):
    _historial[user_id].append({"role": role, "content": content})
    _historial[user_id] = _historial[user_id][-MAX_MENSAJES:]

def borrar(user_id):
    _historial[user_id].clear()