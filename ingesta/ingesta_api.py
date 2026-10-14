
import os
import json
import requests
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load API key
load_dotenv(BASE_DIR / ".env")

API_URL = "https://opendata.aemet.es/opendata/sh/a9a2d26d"
API_KEY = os.getenv("API_KEY")

# Output directory
DATA_DIR = BASE_DIR / "data" / "raw"


def obtener_datos():
    """Download JSON data from AEMET."""

    if not API_KEY:
        raise ValueError("API_KEY not found in .env")

    response = requests.get(
        API_URL,
        params={"api_key": API_KEY},
        timeout=30
    )
    response.raise_for_status()

    resultado = response.json()

    # AEMET endpoints may return a separate data URL
    if isinstance(resultado, dict) and "datos" in resultado:
        response = requests.get(
            resultado["datos"],
            timeout=60
        )
        response.raise_for_status()
        return response.json()

    return resultado


def guardar_json(datos):
    """Create and save the JSON dataset."""

    # Create directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Generate filename using today's date
    fecha = date.today().isoformat()
    archivo = DATA_DIR / f"dataset_{fecha}.json"

    # Write JSON file
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

    print(f"JSON file created successfully: {archivo}")


if __name__ == "__main__":
    try:
        datos = obtener_datos()
        guardar_json(datos)

    except (requests.RequestException, ValueError) as e:
        print(f"Error: {e}")
