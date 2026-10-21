"""Persistencia JSON con validación y reemplazo de archivo temporal."""
import json
import os
import tempfile
from pathlib import Path
from dominio import validar_coleccion


def cargar(ruta):
    ruta = Path(ruta)
    try:
        contenido = ruta.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    registros = json.loads(contenido)
    validar_coleccion(registros)
    return registros


def guardar(ruta, registros):
    validar_coleccion(registros)
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=ruta.parent, suffix=".tmp",
                                         delete=False) as archivo:
            temporal = Path(archivo.name)
            json.dump(registros, archivo, ensure_ascii=False, indent=2)
            archivo.flush()
            os.fsync(archivo.fileno())
        os.replace(temporal, ruta)
    finally:
        if temporal is not None and temporal.exists():
            temporal.unlink()
