from collections import defaultdict

MAX_MENSAJES = 20
def _sistema():
    return {"role": "system", "content": (
        f"Hoy es {date.today().strftime('%d/%m/%Y')}. Eres un asistente útil. "
        "Responde en español de Jerez de la Frontera con acento Andaluz, de forma clara y con el tipico vacile de Jerez. Tienes la herramienta buscar_web: "
        "úsala siempre que la pregunta dependa de información actual o que no conozcas, "
        "y no digas que no tienes acceso a internet."
    )}
_historial = defaultdict(list)

def obtener(user_id):
    return [_sistema] + _historial[user_id]

def añadir(user_id, role, content):
    _historial[user_id].append({"role": role, "content": content})
    _historial[user_id] = _historial[user_id][-MAX_MENSAJES:]

def borrar(user_id):
    _historial[user_id].clear()