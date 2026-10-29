from ddgs import DDGS

def buscar_web(consulta: str) -> str:
    try:
        resultados = DDGS().text(consulta, max_results=5, region="es-es")
    except Exception as e:
        return f"Error al buscar: {e}"
    if not resultados:
        return "Sin resultados."
    return "\n\n".join(f"{r['title']}\n{r['href']}\n{r['body']}" for r in resultados)