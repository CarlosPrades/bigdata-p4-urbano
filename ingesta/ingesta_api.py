
import os
import json
import requests
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

# Directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("API_KEY")

# Endpoint de AEMET: sustituir por el conjunto de datos elegido
API_URL = (
    "https://opendata.aemet.es/opendata/api/"
    "valores/climatologicos/diarios/datos/"
    "fechaini/2026-10-15T00:00:00UTC/"
    "fechafin/2026-10-29T23:59:59UTC/"
    "estacion/8416Y"
)

# Carpeta donde se guardarán los datos originales
DATA_DIR = BASE_DIR / "data" / "raw"


def obtener_datos():
    """Descarga los datos desde la API de AEMET."""

    if not API_KEY:
        raise ValueError("No se ha encontrado API_KEY en .env")

    print("1. Conectando con AEMET...")

    response = requests.get(
        API_URL,
        params={"api_key": API_KEY},
        timeout=30
    )
    response.raise_for_status()

    resultado = response.json()

    # Comprobar la respuesta de la API
    if not isinstance(resultado, dict):
        raise ValueError("Respuesta inicial inesperada")

    if resultado.get("estado") != 200:
        raise ValueError(
            f"Error de AEMET: {resultado.get('descripcion')}"
        )

    # Obtener la URL temporal de descarga
    url_datos = resultado.get("datos")

    if not url_datos:
        raise ValueError("AEMET no ha proporcionado URL de datos")

    print("2. Descargando datos...")

    response = requests.get(url_datos, timeout=60)
    response.raise_for_status()

    return response.json()


def guardar_json(datos):
    """Guarda los datos originales en formato JSON."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    fecha = date.today().isoformat()
    archivo = DATA_DIR / f"dataset_{fecha}.json"

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

    print(f"Datos guardados en: {archivo}")


if __name__ == "__main__":
    try:
        datos = obtener_datos()
        guardar_json(datos)

        print("Ingesta completada correctamente.")

    except (requests.RequestException, ValueError) as e:
        print(f"Error durante la ingesta: {e}")
