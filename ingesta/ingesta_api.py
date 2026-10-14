import os
import json
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://opendata.aemet.es/opendata/sh/a9a2d26d"
API_KEY = os.getenv("API_KEY")

def obtener_datos(page: int = 1, pageSize: int = 100) -> dict:
    """Obtiene una página de resultados de la API."""
    params = {"page": page, "pageSize": pageSize}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    resp = requests.get(API_URL, headers=headers, params=params, timeout=30)
    resp.raise_for_status()  # lanza excepción si el código HTTP no es 2xx
    return resp.json()

def ingesta_completa() -> list[dict]:
    """Recorre todas las páginas hasta agotar los resultados."""
    todos_los_registros = []
    page = 1
    while True:
        datos = obtener_datos(page=page)
        registros = datos.get("results", [])
        if not registros:
            break
        todos_los_registros.extend(registros)
        page += 1
    return todos_los_registros

if __name__ == "__main__":
    registros = ingesta_completa()
    fecha = date.today().isoformat()
    ruta_salida = f"data/raw/dataset_{fecha}.json"
    os.makedirs("data/raw", exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)
    print(f"Ingesta completada: {len(registros)} registros guardados en {ruta_salida}")